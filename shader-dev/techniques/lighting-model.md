# Lighting Models

## Lambertian

```glsl
float lambert(vec3 n, vec3 l) { return max(0.0, dot(n, l)); }
```

## Phong

```glsl
vec3 phong(vec3 ro, vec3 p, vec3 n, vec3 l, vec3 lightCol,
           vec3 albedo, float specular, float shininess) {
    vec3 vd = normalize(ro - p);
    vec3 r = reflect(-l, n);
    vec3 diff = albedo * lambert(n, l) * lightCol;
    vec3 spec = vec3(pow(max(0.0, dot(vd, r)), shininess)) * lightCol * specular;
    return diff + spec;
}
```

## PBR (Cook-Torrance)

```glsl
float D_GGX(float NdH, float roughness) {
    float a = roughness * roughness;
    float a2 = a * a;
    float d = NdH * NdH * (a2 - 1.0) + 1.0;
    return a2 / (3.14159 * d * d);
}
float G_Smith(float NdV, float NdL, float roughness) {
    float r = roughness + 1.0;
    float k = (r * r) / 8.0;
    float g1 = NdV / (NdV * (1.0 - k) + k);
    float g2 = NdL / (NdL * (1.0 - k) + k);
    return g1 * g2;
}
vec3 F_Schlick(vec3 F0, float VdH) {
    return F0 + (1.0 - F0) * pow(1.0 - VdH, 5.0);
}
```

## Toon Shading

```glsl
float toon(float d, float threshold, float softness) {
    return smoothstep(threshold - softness, threshold + softness, d);
}
```
