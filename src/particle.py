# Reference:
# https://stackoverflow.com/questions/14885349/how-to-implement-a-particle-engine

import random

# Basic particle class


class Particle():
    def __init__(self, color, size, *stratagies):
        self.x, self.y = 0, 0
        self.age = 0
        self.color = color
        self.size = size
        self.stratagies = stratagies

    def kill(self):
        self.age = -1

    def move(self):
        for stratagie in self.stratagies:
            stratagie(self)

# ---- Smoke specific functions ---- #

# make the smoke particle ascend


def ascending(speed):
    def _ascending(particle):
        particle.y -= speed
    return _ascending

# kill the smoke particle when outside bounds


def kill_at(max_x, max_y):
    def _kill_at(particle):
        if particle.x < -max_x or particle.x > max_x or particle.y < -max_y or particle.y > max_y:
            particle.kill()
    return _kill_at

# keep track of the particles age


def age(amount):
    def _age(particle):
        particle.age += amount
    return _age

# make the particle larger as it rises


def grow(amount):
    def _grow(particle):
        if random.randint(0, 100) < particle.age / 20:
            particle.size += amount
    return _grow

# spread the smoke out


def fan_out(modifier):
    def _fan_out(particle):
        d = particle.age / modifier
        d += 1
        particle.x += random.randint(int(-d), int(d))
    return _fan_out

# blow the smoke in a direction


def wind(direction, strength):
    def _wind(particle):
        if random.randint(0, 100) < strength:
            particle.x += direction
    return _wind

# factory to create smoke particles


def smoke_machine():
    colors = {
        0: 'light-grey',
        1: 'grey',
        2: 'dark-grey',
        3: 'yellow',
        4: 'orange'
    }

    color_probabilities = ([0] * 32) + ([1] * 32) + \
        ([2] * 32) + ([3] * 2) + ([4] * 2)

    def create():
        for _ in range(random.choice([0, 0, 0, 0, 0, 0, 0, 1, 2, 3])):
            c = colors[random.choice(color_probabilities)]
            s = random.randint(4, 8) if c in [
                'yellow', 'orange'] else random.randint(10, 15)
            behaviour = ascending(1), kill_at(1000, 1000), fan_out(
                400), wind(1, 15), age(1), grow(0.5)
            p = Particle(c, s, *behaviour)
            yield p

    while True:
        yield create()


class Emitter(object):
    def __init__(self, pos=(0, 0)):
        self.particles = []
        self.factories = []
        self.pos = pos

    def add_factory(self, factory, pre_fill=300):
        self.factories.append(factory)
        tmp = []
        for _ in range(pre_fill):
            n = next(factory)
            tmp.extend(n)
            for p in tmp:
                p.move()
        self.particles.extend(tmp)

    def update(self):
        for f in self.factories:
            self.particles.extend(next(f))

        for p in self.particles[:]:
            p.move()
            if p.age == -1:
                self.particles.remove(p)

    def log(self):
        for p in self.particles:
            print(f"{p.x} {p.y} {p.size} {p.color}")
