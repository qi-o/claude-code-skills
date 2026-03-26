# Architecture Patterns

## Feature-Based Organization

```
src/
├── features/
│   ├── users/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── schemas/
│   ├── products/
│   │   └── ...
│   └── shared/
│       ├── errors/
│       ├── logging/
│       └── validation/
├── middleware/
└── routes/
```

## Repository Pattern

```typescript
interface UserRepository {
    findById(id: string): Promise<User | null>;
    findByEmail(email: string): Promise<User | null>;
    create(data: CreateUserInput): Promise<User>;
}
```

## Service Layer

```typescript
class UserService {
    constructor(private repo: UserRepository) {}

    async createUser(data: CreateUserInput): Promise<User> {
        const existing = await this.repo.findByEmail(data.email);
        if (existing) throw new ConflictError('User already exists');
        return this.repo.create(data);
    }
}
```
