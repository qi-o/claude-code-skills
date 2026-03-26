# WebGL Pitfalls

## Common GLSL Errors

### Division by Zero
```glsl
// BAD
return a / b;
// GOOD: guard with epsilon
return a / max(b, 0.001);
```

### Undefined Variables
GLSL requires all variables to be initialized before use. Always initialize.

### Texture LOD
`textureLod` requires explicit LOD in WebGL1. Use `texture` in WebGL2.

### Integer Division
```glsl
// BAD: truncates to 0
int x = a / b;
// GOOD: cast to float first
float x = float(a) / float(b);
```

## ShaderToy → WebGL2 Conversion

| ShaderToy | WebGL2 |
|-----------|--------|
| `gl_FragColor` | `out vec4 fragColor;` |
| `fragCoord` | `gl_FragCoord.xy` |
| `iResolution` | `uResolution` uniform |
| `iTime` | `uTime` uniform |
| `texture2D()` | `texture()` |
| `varying` (vert) | `out` |
| `varying` (frag) | `in` |
| `attribute` | `in` |

## Performance Issues

- Avoid `discard` in fragment shader (breaks early-Z)
- Minimize branching in loops
- Use `float` not `double` (WebGL2 has no double)
- Pack data into vec4 where possible
