# Sound Synthesis in GLSL

## Oscillators

```glsl
float sine(float freq, float time) {
    return sin(6.2831 * freq * time);
}
float saw(float freq, float time) {
    return fract(freq * time) * 2.0 - 1.0;
}
float square(float freq, float time) {
    return step(fract(freq * time), 0.5) * 2.0 - 1.0;
}
```

## Envelope

```glsl
float envelope(float t, float attack, float decay, float sustain, float release) {
    if (t < attack) return t / attack;
    if (t < attack + decay) return mix(1.0, sustain, (t - attack) / decay);
    if (t < 1.0 - release) return sustain;
    return sustain * (1.0 - (t - (1.0 - release)) / release);
}
```

## FM Synthesis

```glsl
float fm(float carrier, float modulator, float index, float time) {
    return sin(6.2831 * carrier * time + index * sin(6.2831 * modulator * time));
}
```
