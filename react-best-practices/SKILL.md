---
name: react-best-practices
description: |
  React/Next.js 性能优化最佳实践。包含 70 条规则，覆盖异步优化、Bundle 优化、服务端性能、客户端数据获取、重渲染优化等 8 大类别。
  触发词：React 优化、Next.js 性能、代码审查、性能优化、bundle 优化、重渲染
  Do NOT use for non-React/Vue frameworks or backend code optimization.
github_url: https://github.com/vercel-labs/agent-skills
github_hash: 47863b24f8e22966bfcf8470debc7ba8c2c3b99c
version: 1.5.0
source: https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
author: Vercel
tags: [react, nextjs, performance, optimization, best-practices]
license: MIT
metadata:
  category: code-quality
---

# Vercel React Best Practices

React 和 Next.js 应用性能优化指南，来自 Vercel 工程团队。包含 70 条规则，按优先级分为 8 大类别。

## 触发条件

当用户进行以下操作时使用此 skill：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码性能问题
- 重构现有 React/Next.js 代码
- 优化 bundle 大小或加载时间

## 规则类别（按优先级排序）

### 1. 消除瀑布流 (CRITICAL) - `async-` 前缀

| 规则 | 说明 |
|------|------|
| `async-cheap-condition-before-await` | 在 await flag/远程值前先检查廉价的同步条件 |
| `async-defer-await` | 将 await 移到实际使用值的分支中 |
| `async-parallel` | 对独立异步操作使用 `Promise.all()` |
| `async-dependencies` | 对部分依赖的操作使用 better-all |
| `async-api-routes` | API 路由中尽早启动 promise，延迟 await |
| `async-suspense-boundaries` | 使用 Suspense 边界流式传输内容 |

**示例：**
```typescript
// ❌ 错误：串行请求
const user = await getUser(id);
const posts = await getPosts(id);

// ✅ 正确：并行请求
const [user, posts] = await Promise.all([
  getUser(id),
  getPosts(id)
]);
```

### 2. Bundle 大小优化 (CRITICAL) - `bundle-` 前缀

| 规则 | 说明 |
|------|------|
| `bundle-barrel-imports` | 直接从源文件导入，避免 barrel 文件 |
| `bundle-analyzable-paths` | 优先使用可静态分析的导入路径和文件系统路径，避免过大的 bundle 和 trace |
| `bundle-dynamic-imports` | 对重型组件使用 `next/dynamic` |
| `bundle-defer-third-party` | 在 hydration 后加载分析/日志 |
| `bundle-conditional` | 仅在功能激活时加载模块 |
| `bundle-preload` | 在 hover/focus 时预加载资源 |

**示例：**
```typescript
// ❌ 错误：从 barrel 文件导入
import { Button } from '@/components';

// ✅ 正确：直接导入
import { Button } from '@/components/Button';

// ✅ 动态导入重型组件
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false
});
```

### 3. 服务端性能 (HIGH) - `server-` 前缀

| 规则 | 说明 |
|------|------|
| `server-auth-actions` | 像 API 路由一样验证 server actions |
| `server-cache-react` | 使用 `React.cache()` 进行请求内去重 |
| `server-cache-lru` | 使用 LRU 缓存进行跨请求缓存 |
| `server-dedup-props` | 避免 RSC props 中的重复序列化 |
| `server-serialization` | 最小化传递给客户端组件的数据 |
| `server-parallel-fetching` | 重构组件以并行化获取 |
| `server-after-nonblocking` | 使用 `after()` 进行非阻塞操作 |
| `server-hoist-static-io` | 将静态 I/O（字体、logo）提升到模块级别 |
| `server-no-shared-module-state` | 在 RSC/SSR 中避免模块级可变请求状态 |
| `server-parallel-nested-fetching` | 对嵌套获取链使用 `Promise.all` 逐项并行 |

**示例：**
```typescript
// ✅ 使用 React.cache() 去重
import { cache } from 'react';

const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } });
});
```

### 4. 客户端数据获取 (MEDIUM-HIGH) - `client-` 前缀

| 规则 | 说明 |
|------|------|
| `client-swr-dedup` | 使用 SWR 自动请求去重 |
| `client-event-listeners` | 去重全局事件监听器 |
| `client-passive-event-listeners` | 对滚动事件使用 passive 监听器 |
| `client-localstorage-schema` | 版本化并最小化 localStorage 数据 |

**示例：**
```typescript
// ✅ 使用 SWR 自动去重和缓存
import useSWR from 'swr';

function Profile() {
  const { data, error } = useSWR('/api/user', fetcher);
  // 多个组件调用相同 key 只发一次请求
}
```

### 5. 重渲染优化 (MEDIUM) - `rerender-` 前缀

| 规则 | 说明 |
|------|------|
| `rerender-defer-reads` | 不要订阅仅在回调中使用的状态 |
| `rerender-memo` | 将昂贵工作提取到 memo 组件 |
| `rerender-memo-with-default-value` | 提升默认非原始 props |
| `rerender-dependencies` | 在 effects 中使用原始依赖 |
| `rerender-derived-state` | 订阅派生布尔值，而非原始值 |
| `rerender-derived-state-no-effect` | 在渲染期间派生状态，而非 effects |
| `rerender-functional-setstate` | 使用函数式 setState 获得稳定回调 |
| `rerender-lazy-state-init` | 对昂贵值传递函数给 `useState` |
| `rerender-simple-expression-in-memo` | 避免对简单原始值使用 memo |
| `rerender-move-effect-to-event` | 将交互逻辑放在事件处理器中 |
| `rerender-transitions` | 对非紧急更新使用 `startTransition` |
| `rerender-use-ref-transient-values` | 对频繁变化的瞬态值使用 refs |
| `rerender-no-inline-components` | 不要在组件内部定义组件 |
| `rerender-split-combined-hooks` | 拆分有独立依赖的自定义 hooks |
| `rerender-use-deferred-value` | 使用 `useDeferredValue` 延迟昂贵渲染，保持输入响应 |

**示例：**
```typescript
// ❌ 错误：每次渲染创建新对象
<Component style={{ color: 'red' }} />

// ✅ 正确：提升到组件外
const style = { color: 'red' };
<Component style={style} />

// ✅ 使用 startTransition 处理非紧急更新
import { startTransition } from 'react';

function handleSearch(query: string) {
  startTransition(() => {
    setSearchResults(filterResults(query));
  });
}
```

### 6. 渲染性能 (MEDIUM) - `rendering-` 前缀

| 规则 | 说明 |
|------|------|
| `rendering-animate-svg-wrapper` | 动画 div 包装器，而非 SVG 元素 |
| `rendering-content-visibility` | 对长列表使用 content-visibility |
| `rendering-hoist-jsx` | 将静态 JSX 提取到组件外 |
| `rendering-svg-precision` | 减少 SVG 坐标精度 |
| `rendering-hydration-no-flicker` | 使用内联脚本处理仅客户端数据 |
| `rendering-hydration-suppress-warning` | 抑制预期的不匹配警告 |
| `rendering-activity` | 使用 Activity 组件处理显示/隐藏 |
| `rendering-conditional-render` | 使用三元运算符，而非 && |
| `rendering-usetransition-loading` | 优先使用 useTransition 处理加载状态 |
| `rendering-resource-hints` | 使用 React DOM resource hints 预加载资源 |
| `rendering-script-defer-async` | 在 script 标签上使用 defer 或 async |

**示例：**
```css
/* ✅ 对长列表使用 content-visibility */
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px;
}
```

### 7. JavaScript 性能 (LOW-MEDIUM) - `js-` 前缀

| 规则 | 说明 |
|------|------|
| `js-batch-dom-css` | 通过 classes 或 cssText 批量 CSS 更改 |
| `js-index-maps` | 为重复查找构建 Map |
| `js-cache-property-access` | 在循环中缓存对象属性 |
| `js-cache-function-results` | 在模块级 Map 中缓存函数结果 |
| `js-cache-storage` | 缓存 localStorage/sessionStorage 读取 |
| `js-combine-iterations` | 将多个 filter/map 合并为一个循环 |
| `js-length-check-first` | 在昂贵比较前先检查数组长度 |
| `js-early-exit` | 从函数提前返回 |
| `js-hoist-regexp` | 将 RegExp 创建提升到循环外 |
| `js-min-max-loop` | 使用循环而非 sort 获取 min/max |
| `js-set-map-lookups` | 使用 Set/Map 进行 O(1) 查找 |
| `js-tosorted-immutable` | 使用 `toSorted()` 保持不可变性 |
| `js-flatmap-filter` | 使用 flatMap 在一次遍历中完成 map 和 filter |
| `js-request-idle-callback` | 将非关键工作延迟到浏览器空闲时间执行 |

**示例：**
```typescript
// ❌ 错误：多次遍历
const filtered = items.filter(x => x.active);
const mapped = filtered.map(x => x.name);

// ✅ 正确：单次遍历
const result = [];
for (const item of items) {
  if (item.active) result.push(item.name);
}

// ✅ 使用 Set 进行 O(1) 查找
const activeIds = new Set(activeItems.map(x => x.id));
const isActive = activeIds.has(item.id);
```

### 8. 高级模式 (LOW) - `advanced-` 前缀

| 规则 | 说明 |
|------|------|
| `advanced-no-effect-event-in-deps` | 不要把 Effect Event 放入依赖数组 |
| `advanced-event-handler-refs` | 在 refs 中存储事件处理器 |
| `advanced-init-once` | 每个应用加载只初始化一次 |
| `advanced-use-latest` | useLatest 用于稳定回调引用 |

---

## 快速参考

```typescript
// 并行请求
const [a, b] = await Promise.all([fetchA(), fetchB()]);

// 动态导入
const Heavy = dynamic(() => import('./Heavy'), { ssr: false });

// React.cache 去重
const getData = cache(async (id) => fetch(`/api/${id}`));

// SWR 客户端缓存
const { data } = useSWR(key, fetcher);

// startTransition 非紧急更新
startTransition(() => setState(newValue));

// content-visibility 长列表
.item { content-visibility: auto; }
```

## 与其他 Skills 配合

| Skill | 配合方式 |
|-------|----------|
| `frontend-design` | 设计 → 本 skill 优化实现 |
| `web-design-guidelines` | 本 skill 性能规则 + 可访问性规则 |

## 资源

- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
- [React 官方文档](https://react.dev)
- [Next.js 官方文档](https://nextjs.org/docs)

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 审查范围确认 | 用户未指定文件或目录时 | 确认要审查的文件/目录范围，避免扫描 node_modules 或无关文件 |
| 破坏性重构建议 | 建议涉及更改公共组件 API、调整数据获取模式或重构状态管理时 | 展示变更影响范围（受影响的组件列表），确认用户接受连锁修改 |
| 依赖引入建议 | 建议引入新库（如 SWR、React Query）解决性能问题时 | 确认项目允许新增依赖，或提供无依赖的替代方案 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 规则源获取失败 | GitHub raw URL 不可达或返回非 200 | 使用 skill 内置的 70 条规则缓存进行离线审查，告知用户规则可能不是最新版本 |
| 项目框架不匹配 | 审查发现项目非 React/Next.js（如 Vue、Svelte） | 停止审查并建议用户使用对应框架的最佳实践 skill |
| 规则误报 | 用户反馈某条规则不适用于其项目场景 | 记录豁免规则及原因，在后续审查中跳过该规则 |
