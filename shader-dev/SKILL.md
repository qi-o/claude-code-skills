---
name: shader-dev
description: Comprehensive GLSL shader development — ray marching, SDF modeling, fluid simulation, particle systems, terrain rendering, procedural generation, and post-processing. 36 techniques. Trigger when user mentions shaders, GLSL, WebGL, ray tracing, particle effects, fluid dynamics, or procedural graphics.
type: skill
github_url: https://github.com/MiniMax-AI/skills
github_hash: b4c7c3fcd4d8c1f6e2a3d7b9c5e1f4a8d2b7c3e9
version: 1.0.0
---

# Shader Development (GLSL / WebGL2)

GLSL shader techniques for creating stunning visual effects. All shaders target WebGL2 with ShaderToy-compatible mainImage() pattern.

## Core Techniques

### Geometry & SDF
- [sdf-2d](techniques/sdf-2d.md) — 2D signed distance functions
- [sdf-3d](techniques/sdf-3d.md) — 3D signed distance functions
- [csg-boolean-operations](techniques/csg-boolean-operations.md) — CSG union/subtract/intersect
- [domain-repetition](techniques/domain-repetition.md) — Infinite repetition and folding
- [domain-warping](techniques/domain-warping.md) — Noise-based domain distortion
- [sdf-tricks](techniques/sdf-tricks.md) — Optimization and advanced SDF techniques

### Ray Casting & Lighting
- [ray-marching](techniques/ray-marching.md) — Sphere tracing core algorithm
- [analytic-ray-tracing](techniques/analytic-ray-tracing.md) — Closed-form ray intersections
- [path-tracing-gi](techniques/path-tracing-gi.md) — Monte Carlo global illumination
- [lighting-model](techniques/lighting-model.md) — Phong, Blinn-Phong, PBR, toon
- [shadow-techniques](techniques/shadow-techniques.md) — Hard/soft shadow mapping
- [ambient-occlusion](techniques/ambient-occlusion.md) — SDF-based and screen-space AO
- [normal-estimation](techniques/normal-estimation.md) — Finite-difference and tetrahedron normals

### Simulation & Physics
- [fluid-simulation](techniques/fluid-simulation.md) — Navier-Stokes fluid solver
- [simulation-physics](techniques/simulation-physics.md) — GPU physics (springs, cloth, N-body)
- [particle-system](techniques/particle-system.md) — Stateless and stateful particles
- [cellular-automata](techniques/cellular-automata.md) — Game of Life, reaction-diffusion

### Natural Phenomena
- [water-ocean](techniques/water-ocean.md) — Gerstner waves, FFT ocean, caustics
- [terrain-rendering](techniques/terrain-rendering.md) — Heightfield ray marching, FBM terrain
- [atmospheric-scattering](techniques/atmospheric-scattering.md) — Rayleigh/Mie scattering
- [volumetric-rendering](techniques/volumetric-rendering.md) — Volume ray marching (clouds, fog, fire)

### Procedural Generation
- [procedural-noise](techniques/procedural-noise.md) — Value, Perlin, Simplex, Worley, FBM
- [procedural-2d-pattern](techniques/procedural-2d-pattern.md) — Brick, hexagon, truchet patterns
- [voronoi-cellular-noise](techniques/voronoi-cellular-noise.md) — Voronoi diagrams, Worley noise
- [fractal-rendering](techniques/fractal-rendering.md) — Mandelbrot, Julia, Mandelbulb
- [color-palette](techniques/color-palette.md) — Cosine palettes, HSL/Oklab color mapping

### Post-Processing & Infrastructure
- [post-processing](techniques/post-processing.md) — Bloom, tone mapping, vignette, glitch
- [multipass-buffer](techniques/multipass-buffer.md) — Ping-pong FBO, state persistence
- [texture-sampling](techniques/texture-sampling.md) — Bilinear, bicubic, mipmap techniques
- [matrix-transform](techniques/matrix-transform.md) — Camera look-at, rotation matrices
- [polar-uv-manipulation](techniques/polar-uv-manipulation.md) — Polar coordinates, kaleidoscope
- [anti-aliasing](techniques/anti-aliasing.md) — SSAA, FXAA, TAA techniques
- [camera-effects](techniques/camera-effects.md) — DOF, motion blur, lens distortion
- [texture-mapping-advanced](techniques/texture-mapping-advanced.md) — Triplanar, ray differentials
- [sound-synthesis](techniques/sound-synthesis.md) — Procedural audio in GLSL
- [webgl-pitfalls](techniques/webgl-pitfalls.md) — Common errors and ShaderToy→WebGL2 conversion

## Performance Budget

| Resource | Budget |
|----------|--------|
| Ray march main loop | 128 steps max |
| Volume sampling inner loop | 32 steps max |
| FBM octaves | 6 layers max |
| Total nested iterations/pixel | 1000 max |

## WebGL2 Setup

```html
<canvas id="c"></canvas>
<script>
const gl = canvas.getContext('webgl2');
const vs = `#version 300 es
in vec2 a_pos;
void main(){gl_Position=vec4(a_pos,0,1);}`;
const fs = `#version 300 es
precision highp float;
out vec4 fragColor;
uniform float uTime;
uniform vec2 uResolution;
void mainImage(out vec4 c,vec2 p){
  vec2 uv=(p-.5*uResolution)/uResolution.y;
  c=vec4(uv,0,1);
}
void main(){mainImage(fragColor,gl_FragCoord.xy);}`;
</script>
```

## Debug Visualization

| What | Code |
|------|------|
| Normals | `col = nor * 0.5 + 0.5;` |
| Step count | `col = vec3(float(steps)/float(MAX_STEPS));` |
| Depth | `col = vec3(t/MAX_DIST);` |
| UV | `col = vec3(uv, 0.0);` |
| SDF bands | `col = vec3(cos(150.0*d));` |
| Shadow | `col = vec3(shadow);` |
