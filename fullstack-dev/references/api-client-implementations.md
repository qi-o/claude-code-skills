# API Client Implementations

Complete code examples for different API client patterns.

## Typed Fetch Wrapper (Simple, No Dependencies)

```typescript
// lib/api-client.ts
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

class ApiError extends Error {
  constructor(public status: number, public body: any) {
    super(body?.detail || body?.message || `API error ${status}`);
  }
}

async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();  // from cookie / memory / context

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ApiError(res.status, body);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const apiClient = {
  get: <T>(path: string) => api<T>(path),
  post: <T>(path: string, data: unknown) => api<T>(path, { method: 'POST', body: JSON.stringify(data) }),
  put: <T>(path: string, data: unknown) => api<T>(path, { method: 'PUT', body: JSON.stringify(data) }),
  patch: <T>(path: string, data: unknown) => api<T>(path, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: <T>(path: string) => api<T>(path, { method: 'DELETE' }),
};
```

## React Query + Typed Client (Recommended for React)

```typescript
// hooks/use-orders.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

interface Order { id: string; total: number; status: string; }
interface CreateOrderInput { items: { productId: string; quantity: number }[] }

export function useOrders() {
  return useQuery({
    queryKey: ['orders'],
    queryFn: () => apiClient.get<{ data: Order[] }>('/api/orders'),
    staleTime: 1000 * 60,  // 1 min
  });
}

export function useCreateOrder() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateOrderInput) =>
      apiClient.post<{ data: Order }>('/api/orders', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });
}

// Usage in component:
function OrdersPage() {
  const { data, isLoading, error } = useOrders();
  const createOrder = useCreateOrder();
  if (isLoading) return <Skeleton />;
  if (error) return <ErrorBanner error={error} />;
  // ...
}
```

## tRPC (Same Team Owns Both Sides)

```typescript
// server: trpc/router.ts
export const appRouter = router({
  orders: router({
    list: publicProcedure.query(async () => {
      return db.order.findMany({ include: { items: true } });
    }),
    create: protectedProcedure
      .input(z.object({ items: z.array(orderItemSchema) }))
      .mutation(async ({ input, ctx }) => {
        return orderService.create(ctx.user.id, input);
      }),
  }),
});
export type AppRouter = typeof appRouter;

// client: automatic type safety, no code generation
const { data } = trpc.orders.list.useQuery();
const createOrder = trpc.orders.create.useMutation();
```

## OpenAPI Generated Client

```bash
npx openapi-typescript-codegen \
  --input http://localhost:3001/api/openapi.json \
  --output src/generated/api \
  --client axios
```
