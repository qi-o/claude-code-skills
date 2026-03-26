# Ray Marching (Sphere Tracing)

## Basic Algorithm

```glsl
#define MAX_STEPS 128
#define MAX_DIST 100.0
#define SURF_DIST 0.001

float map(vec3 p); // scene SDF

float rayMarch(vec3 ro, vec3 rd) {
    float t = 0.0;
    for(int i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + rd * t;
        float d = map(p);
        if(d < SURF_DIST) return t;
        if(t > MAX_DIST) break;
        t += d;
    }
    return -1.0;
}
```

## Camera Setup

```glsl
vec3 getRayDir(vec2 uv, vec3 ro, vec3 lookAt, float zoom) {
    vec3 f = normalize(lookAt - ro);
    vec3 r = normalize(cross(vec3(0,1,0), f));
    vec3 u = cross(f, r);
    return normalize(f * zoom + uv.x * r + uv.y * u);
}
```

## Soft Shadows

```glsl
float softShadow(vec3 ro, vec3 rd, float mint, float maxt, float k) {
    float res = 1.0;
    float t = mint;
    for(int i = 0; i < 32; i++) {
        float h = map(ro + rd * t);
        res = min(res, k * h / t);
        t += clamp(h, 0.01, 0.2);
        if(h < 0.001 || t > maxt) break;
    }
    return clamp(res, 0.0, 1.0);
}
```
