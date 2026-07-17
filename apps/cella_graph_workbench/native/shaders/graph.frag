#version 450

layout(location = 0) in vec4 color;
layout(location = 1) in float vSide;
layout(location = 2) in float vAlong;

layout(push_constant) uniform PushConstants {
    mat4 mvp;
    vec2 itemSize;
    float opacity;
    float halfWidth;
    float time;
    float glowIntensity;
    float flowSpeed;
    float flowAmount;
} pc;

layout(location = 0) out vec4 outColor;

void main()
{
    // Soft cross-line falloff: bright core, fading halo toward the quad edges.
    float d = abs(vSide);
    float core = 1.0 - smoothstep(0.0, 1.0, d);
    float falloff = pow(core, 1.5);
    // Optional travelling brightness along the edge (flowAmount 0 => static).
    float flow = 1.0 + pc.flowAmount * (0.5 + 0.5 * sin(vAlong * 30.0 - pc.time * pc.flowSpeed));
    float alpha = clamp(color.a * falloff * flow, 0.0, 1.0);
    // Additive blend (dst = ONE) multiplies rgb by this alpha, so glowIntensity brightens.
    outColor = vec4(color.rgb * pc.glowIntensity, alpha);
}
