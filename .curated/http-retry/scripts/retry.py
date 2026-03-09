#!/usr/bin/env python3
"""
HTTP Retry Library

提供指数退避、熔断器和 429 限流处理的 HTTP 请求重试功能。
"""

import time
import functools
import logging
from typing import Callable, Any, List, Optional, TypeVar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

# 默认重试的状态码
DEFAULT_RETRY_STATUS = [429, 500, 502, 503, 504]


class CircuitBreaker:
    """熔断器实现"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60,
        expected_exception: type = Exception
    ):
        """
        初始化熔断器

        Args:
            failure_threshold: 连续失败次数阈值，达到后打开熔断器
            recovery_timeout: 熔断器恢复超时（秒）
            expected_exception: 期望捕获的异常类型
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half_open

    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        通过熔断器执行函数

        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            函数返回值

        Raises:
            Exception: 熔断器打开时抛出 RuntimeError
        """
        if self.state == "open":
            # 检查是否超过恢复超时
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "half_open"
                logger.info("Circuit breaker: opening (half-open)")
            else:
                raise RuntimeError("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            # 成功时重置状态
            if self.state == "half_open":
                self.state = "closed"
                self.failure_count = 0
                logger.info("Circuit breaker: closed (recovered)")
            return result
        except self.expected_exception as e:
            self._record_failure()
            raise e

    def _record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker: opened after {self.failure_count} failures")

    def reset(self):
        """重置熔断器"""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"


class RetryHandler:
    """重试处理器"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1,
        max_delay: float = 60,
        backoff_factor: float = 2.0,
        retry_on_status: Optional[List[int]] = None,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: float = 60,
        exceptions: tuple = (Exception,)
    ):
        """
        初始化重试处理器

        Args:
            max_attempts: 最大重试次数
            initial_delay: 初始延迟（秒）
            max_delay: 最大延迟（秒）
            backoff_factor: 退避因子
            retry_on_status: 需要重试的 HTTP 状态码列表
            circuit_breaker_threshold: 熔断器失败阈值
            circuit_breaker_timeout: 熔断器恢复超时（秒）
            exceptions: 需要重试的异常类型元组
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.retry_on_status = retry_on_status or DEFAULT_RETRY_STATUS
        self.exceptions = exceptions

        self.circuit_breaker = CircuitBreaker(
            failure_threshold=circuit_breaker_threshold,
            recovery_timeout=circuit_breaker_timeout
        )

    def _calculate_delay(self, attempt: int) -> float:
        """计算延迟时间（指数退避）"""
        delay = self.initial_delay * (self.backoff_factor ** (attempt - 1))
        return min(delay, self.max_delay)

    def _should_retry(self, exception: Exception, response=None) -> bool:
        """判断是否应该重试"""
        # 如果有响应对象，检查状态码
        if response is not None:
            if hasattr(response, 'status_code'):
                if response.status_code in self.retry_on_status:
                    return True

        # 检查异常类型
        return isinstance(exception, self.exceptions)

    def _get_retry_after(self, response) -> Optional[float]:
        """从响应中获取 Retry-After 值"""
        if hasattr(response, 'headers'):
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                try:
                    return float(retry_after)
                except ValueError:
                    pass
        return None

    def execute(self, func: Callable[..., T], *args, **kwargs) -> T:
        """
        执行带重试的函数

        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            函数返回值

        Raises:
            Exception: 所有重试都失败后抛出最后一个异常
        """
        last_exception = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                result = self.circuit_breaker.call(func, *args, **kwargs)
                return result
            except self.exceptions as e:
                last_exception = e

                # 获取响应对象（如果可用）
                response = None
                if hasattr(e, 'response'):
                    response = e.response

                # 检查是否应该重试
                if not self._should_retry(e, response):
                    raise e

                # 检查是否是最后一次尝试
                if attempt >= self.max_attempts:
                    logger.error(f"All {self.max_attempts} attempts failed")
                    raise e

                # 计算延迟
                delay = self._calculate_delay(attempt)

                # 优先使用 Retry-After（如果有 429 响应）
                if response and hasattr(response, 'status_code') and response.status_code == 429:
                    retry_after = self._get_retry_after(response)
                    if retry_after:
                        delay = retry_after
                        logger.info(f"Using Retry-After: {delay}s")
                    else:
                        logger.warning("429 response without Retry-After, using backoff")

                logger.warning(
                    f"Attempt {attempt}/{self.max_attempts} failed: {e}. "
                    f"Retrying in {delay:.2f}s..."
                )
                time.sleep(delay)

        raise last_exception


def retry(
    max_attempts: int = 3,
    initial_delay: float = 1,
    max_delay: float = 60,
    backoff_factor: float = 2.0,
    retry_on_status: Optional[List[int]] = None,
    circuit_breaker_threshold: int = 5,
    circuit_breaker_timeout: float = 60,
    exceptions: tuple = (Exception,)
):
    """
    重试装饰器

    Args:
        max_attempts: 最大重试次数
        initial_delay: 初始延迟（秒）
        max_delay: 最大延迟（秒）
        backoff_factor: 退避因子
        retry_on_status: 需要重试的 HTTP 状态码列表
        circuit_breaker_threshold: 熔断器失败阈值
        circuit_breaker_timeout: 熔断器恢复超时（秒）
        exceptions: 需要重试的异常类型元组

    Returns:
        装饰器函数

    Example:
        @retry(max_attempts=3, initial_delay=1)
        def fetch(url):
            return requests.get(url)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            handler = RetryHandler(
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                max_delay=max_delay,
                backoff_factor=backoff_factor,
                retry_on_status=retry_on_status,
                circuit_breaker_threshold=circuit_breaker_threshold,
                circuit_breaker_timeout=circuit_breaker_timeout,
                exceptions=exceptions
            )
            return handler.execute(func, *args, **kwargs)
        return wrapper
    return decorator


# CLI 入口（可选）
if __name__ == "__main__":
    import argparse
    import requests

    parser = argparse.ArgumentParser(description="HTTP Retry CLI")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--attempts", "-n", type=int, default=3, help="Max attempts")
    parser.add_argument("--delay", "-d", type=float, default=1, help="Initial delay (seconds)")
    parser.add_argument("--max-delay", "-m", type=float, default=60, help="Max delay (seconds)")
    parser.add_argument("--backoff", "-b", type=float, default=2, help="Backoff factor")

    args = parser.parse_args()

    @retry(
        max_attempts=args.attempts,
        initial_delay=args.delay,
        max_delay=args.max_delay,
        backoff_factor=args.backoff,
        exceptions=(requests.RequestException,)
    )
    def fetch_url(url):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    try:
        result = fetch_url(args.url)
        print(f"Success! Fetched {len(result)} bytes")
    except Exception as e:
        print(f"Failed: {e}")
        exit(1)
