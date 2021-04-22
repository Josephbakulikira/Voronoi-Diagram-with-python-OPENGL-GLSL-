VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 vPos;

void main()
{
    gl_Position = vec4(vPos, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
#define fragCoord gl_FragCoord.xy

#ifdef GL_ES
precision mediump float;
#endif

const float PI = 3.14159265359;
const float PI2 = 6.283185;

uniform vec2  iMouse;
uniform float iTime;
uniform vec2  iResolution;

out vec4 fragColor;

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
}

void main() {
    vec2 st = fragCoord/iResolution.xy;
    st.x *= iResolution.x/iResolution.y;
    vec3 color = vec3(.0);

    // Scale
    st *= 8.;

    vec2 i_st = floor(st);
    vec2 f_st = fract(st);

    float m_dist = 1;

    for (int y= -1; y <= 1; y++) {
        for (int x= -1; x <= 1; x++) {
            vec2 neighbor = vec2(float(x),float(y));

            vec2 point = random2(i_st + neighbor);

            point = 0.5 + 0.5*sin(iTime  + PI2*point)/2.0 ;

            vec2 diff = neighbor + point - f_st;

            // Distance to the point
            float dist = length(diff);
            m_dist = min(m_dist, dist);
        }
    }

    color += m_dist;

    // Draw the point center
    color += 1.-step(.02, m_dist);


    fragColor = vec4(color,1.0);
}
"""
