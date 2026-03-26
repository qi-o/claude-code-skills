# GPU Physics Simulation

## Spring System

```glsl
vec3 springForce(vec3 pos, vec3 anchor, float k, float rest) {
    vec3 d = anchor - pos;
    return k * (length(d) - rest) * normalize(d);
}

// Per-frame update
vec3 updateParticle(vec3 pos, vec3 vel, vec3 anchor, float k, float rest, float dt) {
    vec3 force = springForce(pos, anchor, k, rest);
    vel += force * dt;
    vel *= 0.99; // damping
    pos += vel * dt;
    return pos;
}
```

## N-Body Gravity

```glsl
vec3 gravity(vec3 pos, vec3 vel, vec3 others[], int n, float G, float dt) {
    vec3 acc = vec3(0.0);
    for(int i = 0; i < n; i++) {
        vec3 r = others[i] - pos;
        float dist = length(r);
        if(dist > 0.1) acc += G * r / (dist * dist * dist);
    }
    vel += acc * dt;
    pos += vel * dt;
}
```
