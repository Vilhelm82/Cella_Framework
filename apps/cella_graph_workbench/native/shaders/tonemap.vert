#version 450

layout(push_constant) uniform Tonemap {
    mat4 mvp;
    vec2 itemSize;
    float exposure;
    float pad;
} pc;

layout(location = 0) out vec2 vUv;

void main()
{
    // Two-triangle quad in item-local space; the scene mvp applies zoom/pan.
    vec2 corners[6] = vec2[](vec2(0.0, 0.0), vec2(1.0, 0.0), vec2(0.0, 1.0),
                             vec2(0.0, 1.0), vec2(1.0, 0.0), vec2(1.0, 1.0));
    vec2 c = corners[gl_VertexIndex];
    vUv = c;
    gl_Position = pc.mvp * vec4(c * pc.itemSize, 0.0, 1.0);
}
