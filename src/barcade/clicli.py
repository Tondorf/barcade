import select
import sys
import termios
import time
import tty

import barcade
from barcade import Scancode


def _read_char(*, timeout):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        if not select.select([sys.stdin], [], [], timeout)[0]:
            return None

        if (c := sys.stdin.read(1)) == "\x03":  # Ctrl-C
            raise KeyboardInterrupt
        else:
            return c
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _move_cursor_up(n=1):
    sys.stdout.write(f"\033[{n}A")


def _clear_line():
    sys.stdout.write("\033[2K")


def _flush():
    sys.stdout.flush()


def _println(msg="", *, flush=False):
    sys.stdout.write(msg + "\n")

    if flush:
        _flush()


def main(fps=40):
    _println("Loading...\n", flush=True)

    game = barcade.Snake()

    action = None
    running = True
    while running:
        match _read_char(timeout=1 / fps):
            case "w":
                action = Scancode.W
            case "a":
                action = Scancode.A
            case "s":
                action = Scancode.S
            case "d":
                action = Scancode.D
            case "q" | "\x1b":
                running = False

        game.add_action(action)
        running &= game.tick(time.perf_counter())

        _move_cursor_up(2)

        _clear_line()
        _println("|" + "".join(barcade.BRAILLE[b] for b in game.screen) + "|")

        _clear_line()
        _println(f"Score: {game.score}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        _println(flush=True)
