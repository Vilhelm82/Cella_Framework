#version 450

layout(binding = 0) uniform sampler2D hdrTex;

layout(push_constant) uniform Tonemap {
    mat4 mvp;
    vec2 itemSize;
    float exposure;
    float pad;
} pc;

layout(location = 0) in vec2 vUv;
layout(location = 0) out vec4 outColor;

void main()
{
    vec3 hdr = texture(hdrTex, vUv).rgb * pc.exposure;
    // Per-channel Reinhard: accumulated brightness rolls toward the colour's own
    // hue and asymptotes to 1.0, so dense cores glow coloured instead of white.
    vec3 mapped = hdr / (1.0 + hdr);
    float coverage = clamp(max(mapped.r, max(mapped.g, mapped.b)), 0.0, 1.0);
    outColor = vec4(mapped, coverage);
}
