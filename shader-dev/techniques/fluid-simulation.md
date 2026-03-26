# Fluid Simulation (Navier-Stokes)

## Simplified 2D Fluid

```glsl
// Advection
float advect(float f, vec2 vel, vec2 uv, float dt) {
    vec2 prev = uv - vel * dt;
    return texture2D(uVelocity, prev).x;
}

// Pressure projection
// Jacobi iteration for pressure solve
float pressureSolve(float pCurr, float pLeft, float pRight, float pUp, float pDown, float div) {
    return (pLeft + pRight + pUp + pDown - div) * 0.25;
}
```

## 3D Smoke Sim

```glsl
// Semi-Lagrangian advection
vec3 advect(vec3 pos, vec3 vel, float dt) {
    return pos - vel * dt;
}

// Buoyancy force
vec3 buoyancy(vec3 vel, float density, float temp) {
    return vec3(0.0, density * -0.98 + temp * 0.5, 0.0);
}
```
