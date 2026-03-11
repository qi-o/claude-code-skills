# Coding Style Rules

## Immutability First
- Prefer const over let
- Use spread operator for object/array updates
- Avoid mutating function parameters

## File Organization
- One component per file
- Group related files in directories
- Keep files under 300 lines

## Naming Conventions
- Components: PascalCase
- Functions: camelCase
- Constants: UPPER_SNAKE_CASE
- Files: kebab-case or PascalCase for components

## Anti-Patterns (禁止)

完整禁止项列表见 [anti-patterns.md](./anti-patterns.md)。

编码领域关键禁止项：
- `var` 声明变量
- Magic numbers
- 深层嵌套
- 函数过长
- 重复代码
- 负面命名
