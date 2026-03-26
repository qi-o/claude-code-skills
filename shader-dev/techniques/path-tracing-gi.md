# Path Tracing (Monte Carlo GI)

## Cosine Sampling

```glsl
vec3 cosineSampleHemisphere(vec2 u, vec3 n) {
    float r = sqrt(u.x);
    float theta = 2.0 * 3.14159 * u.y;
    float x = r * cos(theta);
    float y = r * sin(theta);
    float z = sqrt(max(0.0, 1.0 - u.x));
    vec3 h = normalize(vec3(x, y, z));
    return dot(h, n) > 0.0 ? h : -h;
}
```

## Simple Path Trace

```glsl
vec3 pathtrace(vec3 ro, vec3 rd) {
    vec3 col = vec3(0.0);
    vec3 throughput = vec3(1.0);
    for(int bounce = 0; bounce < 4; bounce++) {
        float t = rayMarch(ro, rd);
        if(t < 0.0) { col += throughput * vec3(0.5, 0.7, 1.0); break; }
        vec3 p = ro + rd * t;
        vec3 n = getNormal(p);
        vec3 albedo = getMaterial(p);
        throughput *= albedo;
        rd = cosineSampleHemisphere(random2(), n);
        ro = p + n * 0.001;
    }
    return col;
}
```
