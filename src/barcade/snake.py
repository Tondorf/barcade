import random

from barcade import Scancode, Screen


class Snake:
    def __init__(self):
        self._t_last = 0
        self._alive = True

        self._screen = Screen()

        self._snake = [(0, 1), (1, 1)]
        self._head_idx = -1
        self._vx, self._vy = 1, 0
        self._apple = None

        for x, y in self._snake:
            self._screen.set(x, y)

    @property
    def screen(self):
        return self._screen.serialize()

    @property
    def score(self):
        return len(self._snake)

    def tick(self, t):
        if t - self._t_last < 0.25:
            return self._alive

        self._t_last = t

        x, y = self._snake[self._head_idx]
        new_x = (x + self._vx) % self._screen.width
        new_y = (y + self._vy) % self._screen.height

        will_grow = (new_x, new_y) == self._apple

        tail_idx = (self._head_idx + 1) % len(self._snake)
        if (new_x, new_y) in self._snake and (
            will_grow or (new_x, new_y) != self._snake[tail_idx]
        ):
            self._alive = False
            return False

        self._head_idx = tail_idx
        if (new_x, new_y) == self._apple:
            self._apple = None
            self._snake.insert(self._head_idx, (new_x, new_y))
        else:
            self._screen.unset(*self._snake[self._head_idx])
            self._screen.set(new_x, new_y)
            self._snake[self._head_idx] = (new_x, new_y)

        if self._apple is None:
            a = random.randint(0, self._screen.width - 1)
            b = random.randint(0, self._screen.height - 1)
            if not any(
                self._cyclic_chebychev_distance((x, y), (a, b)) < 2
                for x, y in self._snake
            ):
                self._apple = a, b
                self._screen.set(a, b)

        return True

    def add_action(self, scancode):
        match scancode:
            case Scancode.W | Scancode.UP if self._vy == 0:
                self._vx = 0
                self._vy = 1
            case Scancode.S | Scancode.DOWN if self._vy == 0:
                self._vx = 0
                self._vy = -1
            case Scancode.A | Scancode.LEFT if self._vx == 0:
                self._vx = -1
                self._vy = 0
            case Scancode.D | Scancode.RIGHT if self._vx == 0:
                self._vx = 1
                self._vy = 0

    def _cyclic_chebychev_distance(self, xy, ab):
        x, y = xy
        a, b = ab

        dx = abs(x - a)
        dy = abs(y - b)

        dx = min(dx, self._screen.width - dx)
        dy = min(dy, self._screen.height - dy)

        return max(dx, dy)
