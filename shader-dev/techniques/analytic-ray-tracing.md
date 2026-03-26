# Analytic Ray Tracing

## Ray-Sphere Intersection

```glsl
vec2 raySphere(vec3 ro, vec3 rd, vec3 center, float radius) {
    vec3 oc = ro - center;
    float b = dot(oc, rd);
    float c = dot(oc, oc) - radius * radius;
    float h = b*b - c;
    if(h < 0.0) return vec2(-1.0);
    h = sqrt(h);
    return vec2(-b - h, -b + h);
}
```

## Ray-Box Intersection

```glsl
vec2 rayBox(vec3 ro, vec3 rd, vec3 boxMin, vec3 boxMax) {
    vec3 tMin = (boxMin - ro) / rd;
    vec3 tMax = (boxMax - ro) / rd;
    vec3 t1 = min(tMin, tMax);
    vec3 t2 = max(tMin, tMax);
    float tNear = max(max(t1.x, t1.y), t1.z);
    float tFar = min(min(t2.x, t2.y), t2.z);
    if(tNear > tFar || tFar < 0.0) return vec2(-1.0);
    return vec2(tNear, tFar);
}
```

## Ray-Plane

```glsl
float rayPlane(vec3 ro, vec3 rd, vec3 n, float h) {
    float denom = dot(rd, n);
    if(abs(denom) < 1e-6) return -1.0;
    float t = -(dot(ro, n) + h) / denom;
    return t > 0.0 ? t : -1.0;
}
```
