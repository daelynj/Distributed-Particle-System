import grpc
import os
import pygame
import sys
import threading
import time

from queue import Queue
from pygame.locals import *

import proto.particle_system_pb2 as ps
import proto.particle_system_pb2_grpc as rpc

FPS = 30

WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768

WHITE = (255, 255, 255)
DARK_GREY = (105, 105, 105)
GREY = (169, 169, 169)
LIGHT_GREY = (211, 211, 211)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
SKY_BLUE = (135, 206, 235) 

COLORS = {
  'dark-grey': DARK_GREY,
  'grey': GREY,
  'light-grey': LIGHT_GREY,
  'yellow': YELLOW,
  'orange': ORANGE
}

class Client:
  def __init__(self, address='localhost', port=50051):
    channel = grpc.insecure_channel(address + ':' + str(port))
    self.stub = rpc.GenerateStub(channel)

    self.frame_buffer = Queue()

    self.generate_thread = threading.Thread(target=self.generate_particles)
    self.generate_thread.start()

    global CLOCK, DISPLAY

    pygame.init()

    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Particles!')

    self.render_thread = threading.Thread(target=self.render_particles)
    self.render_thread.start()
    

  def generate_particles(self):
    instructions = ps.RenderInstructions()
    instructions.frame_count = 300
    for frame in self.stub.GenerateParticles(instructions):
      particles = map(
        lambda p : {'x': p.x, 'y': p.y, 'size': p.size, 'color': COLORS[p.color]}, 
        frame.particles
      )

      self.frame_buffer.put(particles)

  def render_particles(self):
    global CLOCK, DISPLAY

    while True:
      try:

        # gracefully handle quiting
        self.checkForKeyPress()

        # wait briefly for a frame in the buffer
        for i in range(10):
          if i == 9:
            return
          elif self.frame_buffer.empty():
            time.sleep(0.1)
          else:
            break
  
        frame = self.frame_buffer.get()
        
        # clear the previous frame
        DISPLAY.fill(SKY_BLUE)

        for particle in frame:

          # create a surface with transparancy 
          surface = pygame.Surface((250, 250))
          surface.set_colorkey((0, 0, 0))
          surface.set_alpha(100)

          # draw the smoke partile to the surface
          pygame.draw.circle(surface, particle['color'], (125, 125), int(particle['size']))

          # adjust the position in the screen
          position = (particle['x'] + int(WINDOW_WIDTH / 2.6), particle['y'] + WINDOW_HEIGHT - 150)
          
          # blit the surface to the display
          DISPLAY.blit(surface, (position))

        # update the display and tick the clock
        pygame.display.update()
        CLOCK.tick(FPS)

      except Exception as e:
        self.terminate()
      
  def checkForKeyPress(self):
    print('here')
    if len(pygame.event.get(QUIT)) > 0:
      self.terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return
    
    if keyUpEvents[0].key in [K_ESCAPE, K_q]:
      self.terminate()
  
  def terminate(self):
    pygame.quit()
    self.render_thread.join()
    self.generate_thread.join()
    sys.exit()

if __name__ == '__main__':
  client = Client()