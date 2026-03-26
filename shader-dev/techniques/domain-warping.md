# Domain Warping

## Basic Warp

```glsl
float warp(vec3 p) {
    vec3 q = vec3(
        fbm(p + vec3(0.0, 0.0, 0.0)),
        fbm(p + vec3(5.2, 1.3, 2.1)),
        fbm(p + vec3(2.7, 4.8, 3.9))
    );
    return fbm(p + q);
}
```

## Turbulence

```glsl
float turbulence(vec3 p) {
    float sum = 0.0, amp = 1.0;
    for(int i = 0; i < 5; i++) {
        sum += abs(noise(p)) * amp;
        p *= 2.0;
        amp *= 0.5;
    }
    return sum;
}
```

## Double Warp

```glsl
// Two-level domain warping (Inigo Quilez technique)
float dwarp(vec3 p) {
    vec3 q = vec3(fbm(p), fbm(p + vec3(3.0)), fbm(p + vec3(7.0)));
    return fbm(p + 4.0 * vec3(fbm(q + vec3(1.7, 9.2, 3.4))));
}
```
