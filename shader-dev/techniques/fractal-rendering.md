# Fractal Rendering

## Mandelbrot Set

```glsl
float mandelbrot(vec2 c) {
    vec2 z = vec2(0.0);
    for(int i = 0; i < 256; i++) {
        z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
        if(dot(z,z) > 4.0) return float(i) / 256.0;
    }
    return 1.0;
}
```

## Julia Set

```glsl
float julia(vec2 z, vec2 c) {
    for(int i = 0; i < 256; i++) {
        z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
        if(dot(z,z) > 4.0) return float(i) / 256.0;
    }
    return 1.0;
}
```

## 3D Fractals (Mandelbulb)

```glsl
float mandelbulb(vec3 pos, int iterations) {
    vec3 z = pos;
    float dr = 1.0, r = 0.0;
    for(int i = 0; i < iterations; i++) {
        r = length(z);
        if(r > 2.0) break;
        float theta = acos(z.z / r), phi = atan(z.y, z.x);
        dr = pow(r, 8.0 - 1.0) * 8.0 * dr + 1.0;
        float zr = pow(r, 8.0);
        theta *= 8.0; phi *= 8.0;
        z = zr * vec3(sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta)) + pos;
    }
    return 0.5 * log(r) * r / dr;
}
```
