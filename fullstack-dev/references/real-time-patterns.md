# Real-Time Patterns

## SSE Setup

```typescript
// Server
app.get('/events', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    const interval = setInterval(() => {
        res.write(`data: ${JSON.stringify({ time: Date.now() })}\n\n`);
    }, 1000);
    req.on('close', () => clearInterval(interval));
});
```

## WebSocket Setup

```typescript
// ws library
import { WebSocketServer } from 'ws';
const wss = new WebSocketServer({ server });
wss.on('connection', (ws) => {
    ws.on('message', (data) => {
        wss.clients.forEach(client => client.send(data));
    });
});
```

## Scaling Consideration

SSE and WebSocket require sticky sessions or central pub/sub (Redis) when scaling to multiple instances.
