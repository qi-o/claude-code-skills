# Particle Systems

## Stateless Particles (GPU)

```glsl
// Instanced rendering — position computed per-instance
vec3 particlePos(float i, float time) {
    float angle = i * 6.28 * 0.1 + time;
    float radius = 1.0 + 0.5 * sin(time + i);
    return vec3(radius * cos(angle), sin(time * 0.7 + i), radius * sin(angle));
}
```

## Stateful Particles

```glsl
// Ping-pong buffer for state
// Buffer A: position
// Buffer B: velocity
vec4 updatePos(ivec2 px, float time) {
    vec4 pos = texelFetch(uPos, px, 0);
    vec4 vel = texelFetch(uVel, px, 0);
    pos.xyz += vel.xyz * uDeltaTime;
    pos.w = 1.0; // lifetime
    return pos;
}
```

## Fire Effect

```glsl
vec3 fire(vec2 uv, float time) {
    float t = time * 2.0;
    float dx = fbm(vec2(uv.x * 3.0, uv.y * 5.0 - t));
    float dy = -t + fbm(vec2(uv.x * 2.0 + dx, uv.y * 4.0 - t));
    vec2 p = uv + vec2(dx * 0.3, dy * 0.3);
    float heat = max(0.0, 1.0 - 2.0 * length(uv - vec2(0.0, 0.3)));
    return vec3(1.0, heat * heat, heat * heat * heat) * heat;
}
```
