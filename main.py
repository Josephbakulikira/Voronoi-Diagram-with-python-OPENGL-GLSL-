from __future__ import division
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL import shaders
from sys import exit as exitsystem
from numpy import array

from shaderVoronoi import *

class Main(object):
    def __init__(self):
        pygame.init()
        self.resolution = 1000, 1000
        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('Voronoi diagram')

        # setting my Shaders
        self.vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        self.fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)


        self.shader = shaders.compileProgram(self.vertex_shader, self.fragment_shader)

        # Get the uniform locations
        self.uni_mouse = glGetUniformLocation(self.shader, 'iMouse')
        self.uni_ticks = glGetUniformLocation(self.shader, 'iTime')

        glUseProgram(self.shader)   # Need to be enabled before sending uniform variables
        # Resolution doesn't change. Send it once
        glUniform2f(glGetUniformLocation(self.shader, 'iResolution'), *self.resolution)

        #to create a quad
        self.vertices = array([-1.0, -1.0, 0.0,
                                1.0, -1.0, 0.0,
                                1.0,  1.0, 0.0,
                               -1.0,  1.0, 0.0], dtype='float32')
        #generate VBO and VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        self.clock = pygame.time.Clock()

    def mainloop(self):
        while 1:
            delta = self.clock.tick(8192)

            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            for event in pygame.event.get():
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    exitsystem()

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:
                        pass

            glUseProgram(self.shader)

            # Map mouse coordinates between -1 and 1 range
            mx, my = pygame.mouse.get_pos()
            mx = (1.0 / self.resolution[0] * mx) * 2.0 - 1.0
            my = (1.0 / self.resolution[1] * my) * 2.0 - 1.0

            glUniform2f(self.uni_mouse, mx, my)
            glUniform1f(self.uni_ticks, pygame.time.get_ticks() / 1000.0)

            # Bind the vao (which stores the VBO with all the vertices)
            glBindVertexArray(self.vao)
            glDrawArrays(GL_QUADS, 0, 4)

            pygame.display.set_caption("FPS: {}".format(self.clock.get_fps()))
            pygame.display.flip()



if __name__ == '__main__':
    Main().mainloop()
