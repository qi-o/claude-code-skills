# Matrix Transform

## Camera Look-At

```glsl
mat3 setCamera(vec3 ro, vec3 ta, float cr) {
    vec3 cw = normalize(ta - ro);
    vec3 cp = vec3(sin(cr), cos(cr), 0.0);
    vec3 cu = normalize(cross(cw, cp));
    vec3 cv = cross(cu, cw);
    return mat3(cu, cv, cw);
}
```

## Rotation Matrices

```glsl
mat2 rot2D(float a) {
    float s = sin(a), c = cos(a);
    return mat2(c, -s, s, c);
}
mat3 rotateY(float a) {
    float s = sin(a), c = cos(a);
    return mat3(c,0,s, 0,1,0, -s,0,c);
}
```

## Orbit Camera

```glsl
vec3 orbitCamera(vec2 mouse, float dist) {
    float theta = mouse.x * 6.28;
    float phi = mouse.y * 3.14 + 0.01;
    return vec3(
        dist * sin(phi) * cos(theta),
        dist * cos(phi),
        dist * sin(phi) * sin(theta)
    );
}
```
