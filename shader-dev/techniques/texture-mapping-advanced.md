# Advanced Texture Mapping

## Triplanar Mapping

```glsl
vec3 triplanar(vec3 p, vec3 n, sampler2D tex) {
    vec3 blend = abs(n);
    blend /= (blend.x + blend.y + blend.z);
    vec3 x = texture(tex, p.yz).rgb;
    vec3 y = texture(tex, p.xz).rgb;
    vec3 z = texture(tex, p.xy).rgb;
    return x * blend.x + y * blend.y + z * blend.z;
}
```

## Ray Differential Texturing

```glsl
// For proper mipmap selection on distorted surfaces:
// Trace rays in screen space to estimate footprint
```
