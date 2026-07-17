#version 450

layout(location = 0) in vec2 inPosition;
layout(location = 1) in vec4 inMeta;   // dirX, dirY, side(-1|+1), along(0..1)
layout(location = 2) in vec4 inColor;

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

layout(location = 0) out vec4 color;
layout(location = 1) out float vSide;
layout(location = 2) out float vAlong;

void main()
{
    vec2 localPosition = inPosition * pc.itemSize;
    // Perpendicular in pixel space so line width is uniform regardless of item aspect.
    vec2 dirPx = inMeta.xy * pc.itemSize;
    float len = length(dirPx);
    dirPx = len > 1e-5 ? dirPx / len : vec2(1.0, 0.0);
    vec2 perp = vec2(-dirPx.y, dirPx.x);
    vec2 expanded = localPosition + perp * inMeta.z * pc.halfWidth;
    gl_Position = pc.mvp * vec4(expanded, 0.0, 1.0);
    color = vec4(inColor.rgb, inColor.a * pc.opacity);
    vSide = inMeta.z;
    vAlong = inMeta.w;
}
