#!/usr/bin/env python3
import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

    while True:
        play(stdscr)

def play(stdscr):
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()

    # Game area with border
    H, W = sh - 4, sw - 2
    off_y, off_x = 3, 1

    # Draw border
    stdscr.attron(curses.color_pair(5))
    stdscr.border()
    stdscr.attroff(curses.color_pair(5))

    # Title
    title = " SNAKE "
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, (sw - len(title)) // 2, title)
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

    snake = [
        [H // 2 + off_y, W // 2 + off_x],
        [H // 2 + off_y, W // 2 + off_x - 1],
        [H // 2 + off_y, W // 2 + off_x - 2],
    ]
    direction = curses.KEY_RIGHT
    score = 0
    best = 0
    speed = 0.12

    def spawn_food():
        while True:
            f = [random.randint(off_y, off_y + H - 1), random.randint(off_x, off_x + W - 1)]
            if f not in snake:
                return f

    food = spawn_food()

    def draw_ui():
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(1, 2, f"Score: {score}   Best: {best}   Speed: {int(1/speed)} ")
        stdscr.addstr(2, 2, "↑↓←→ or WASD to move | Q to quit")
        stdscr.attroff(curses.color_pair(4))

    stdscr.nodelay(True)
    stdscr.timeout(int(speed * 1000))

    while True:
        # Draw food
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(food[0], food[1], '●')
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

        # Draw snake head
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(snake[0][0], snake[0][1], '█')
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Draw snake body
        stdscr.attron(curses.color_pair(1))
        for seg in snake[1:]:
            stdscr.addstr(seg[0], seg[1], '▓')
        stdscr.attroff(curses.color_pair(1))

        draw_ui()
        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord('q'), ord('Q')):
            curses.endwin()
            exit(0)

        # Direction (no reversing)
        if key in (curses.KEY_UP, ord('w'), ord('W')) and direction != curses.KEY_DOWN:
            direction = curses.KEY_UP
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')) and direction != curses.KEY_UP:
            direction = curses.KEY_DOWN
        elif key in (curses.KEY_LEFT, ord('a'), ord('A')) and direction != curses.KEY_RIGHT:
            direction = curses.KEY_LEFT
        elif key in (curses.KEY_RIGHT, ord('d'), ord('D')) and direction != curses.KEY_LEFT:
            direction = curses.KEY_RIGHT

        # Move
        head = snake[0][:]
        if direction == curses.KEY_UP:    head[0] -= 1
        elif direction == curses.KEY_DOWN:  head[0] += 1
        elif direction == curses.KEY_LEFT:  head[1] -= 1
        elif direction == curses.KEY_RIGHT: head[1] += 1

        # Collision: walls
        if head[0] < off_y or head[0] >= off_y + H or head[1] < off_x or head[1] >= off_x + W:
            break
        # Collision: self
        if head in snake:
            break

        snake.insert(0, head)

        if head == food:
            score += 1
            if score > best:
                best = score
            # Speed up every 5 points
            if score % 5 == 0 and speed > 0.05:
                speed = max(0.05, speed - 0.01)
                stdscr.timeout(int(speed * 1000))
            food = spawn_food()
        else:
            # Erase tail
            tail = snake.pop()
            stdscr.addstr(tail[0], tail[1], ' ')

    # Game over screen
    stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
    msg = f" GAME OVER  Score: {score} "
    stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg)
    stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

    stdscr.attron(curses.color_pair(4))
    sub = " Press R to restart or Q to quit "
    stdscr.addstr(sh // 2 + 1, (sw - len(sub)) // 2, sub)
    stdscr.attroff(curses.color_pair(4))
    stdscr.refresh()

    stdscr.nodelay(False)
    while True:
        k = stdscr.getch()
        if k in (ord('r'), ord('R')):
            return
        if k in (ord('q'), ord('Q')):
            curses.endwin()
            exit(0)

curses.wrapper(main)
