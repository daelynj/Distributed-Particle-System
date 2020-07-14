import pygame, os, sys
from pygame.locals import *

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

def main():
  global CLOCK, DISPLAY

  pygame.init()

  CLOCK = pygame.time.Clock()
  DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.display.set_caption('Particles!')

  frames = process_data()

  render(frames)

def process_data():
  global CLOCK, DISPLAY

  font = pygame.font.Font('freesansbold.ttf', 20)
  text = font.render('Processing Data...', True, WHITE)
  rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

  DISPLAY.blit(text, rect)

  pygame.display.update()
  CLOCK.tick(FPS)

  frame = []
  frames = []
  file = open(os.path.join('src', 'particle_timeline_data', 'particle_timeline_1.txt'), 'r')
  
  for line in file:
    if 'frame' in line:
      frames.append(frame)
      frame = []
    else:
      properties = line.split()

      particle = {}
      particle['x'] = int(properties[0])
      particle['y'] = int(properties[1])
      particle['size'] = int(float(properties[2]))
      particle['color'] = COLORS[properties[3]]

      frame.append(particle)

  return frames
  

def render(frames):
  global CLOCK, DISPLAY

  for f in frames:
    # gracefully handle quiting
    checkForKeyPress()

    # clear the previous frame
    DISPLAY.fill(SKY_BLUE)

    for particle in f:
      # create a surface with transparancy 
      surface = pygame.Surface((250, 250))
      surface.set_colorkey((0, 0, 0))
      surface.set_alpha(100)

      # draw the smoke partile to the surface
      pygame.draw.circle(surface, particle['color'], (125, 125), particle['size'])

      # adjust the position in the screen
      position = (particle['x'] + int(WINDOW_WIDTH / 2.6), particle['y'] + WINDOW_HEIGHT - 150)
      
      # blit the surface to the display
      DISPLAY.blit(surface, (position))

    # update the display and tick the clock
    pygame.display.update()
    CLOCK.tick(FPS)

def checkForKeyPress():
  if len(pygame.event.get(QUIT)) > 0:
    terminate()

  keyUpEvents = pygame.event.get(KEYUP)
  if len(keyUpEvents) == 0:
      return
  
  if keyUpEvents[0].key in [K_ESCAPE, K_q]:
    terminate()

def terminate():
  pygame.quit()
  sys.exit()

if __name__ == '__main__':
	main()