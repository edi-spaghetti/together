import random


increment = 0.001
max_size = 50


class Game:

    def __init__(self):
        self.things = list()
        print('Loaded Game')

    def update(self):
        for thing in self.things:
            if thing.autonomous:
                thing.x += self.compare(random.random(), 0.5) * increment
                thing.y += self.compare(random.random(), 0.5) * increment

    def add_random_thing(self):
        self.add_thing(
            random.random(),
            random.random(),
            int(random.random() * max_size)
        )

    def add_thing(self, x, y, size, autonomous=True):
        self.things.append(GameObject(x, y, size, autonomous))

    def compare(self, a, b):
        return (a >= b) - (a <= b)


class GameObject:

    def __init__(self, x, y, size, autonomous=True):
        self.x = x
        self.y = y
        self.size = size
        self.autonomous = autonomous

    def __repr__(self):
        if self.autonomous:
            return f'Thing({round(self.x, 2)}, {round(self.y, 2)}, {self.size})'
        else:
            return f'Puppet({round(self.x, 2)}, {round(self.y, 2)}, {self.size})'
