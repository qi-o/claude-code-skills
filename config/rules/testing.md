# Testing Rules

## Minimum Coverage: 80%

Required test types:
- Unit Tests: Individual functions/components
- Integration Tests: API endpoints, database operations
- E2E Tests: Critical user flows (Playwright)

## TDD Workflow (Mandatory)

1. Write test first (RED)
2. Run test - must fail
3. Write minimal implementation (GREEN)
4. Run test - must pass
5. Refactor (IMPROVE)
6. Verify 80%+ coverage

## Anti-Patterns (禁止)

完整禁止项列表见 [anti-patterns.md](./anti-patterns.md)。

测试领域关键禁止项：
- 没有断言的测试
- Mock 内部实现
- 测试覆盖无意义代码
- 硬编码测试数据
- 测试之间共享状态

## Troubleshooting

1. Use tdd-guide agent
2. Check test isolation
3. Verify mocks are correct
4. Fix implementation, not tests (unless tests are wrong)
