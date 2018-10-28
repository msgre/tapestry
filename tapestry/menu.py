import os
from .states import get_state, STATE_ACTION, STATE_QUIT, STATE_MISSING_SOURCE, STATE_NEXT, STATE_PREV

import pygame
import pygame.locals
import time
from .detective import get_entries, check_dir, source_exist


class Menu:
    def __init__(self, dirpath, display, config, position=0, fps=50, sleep=3):
        self.dirpath = os.path.abspath(dirpath)
        self.screen = display.screen
        self.font = display.font
        self.size = display.size
        self.config = config
        self.fps = fps
        self.sleep = sleep
        self.initial_position = position

    def get_position(self):
        """
        Return 0 based index of selected menu item.
        """
        return self.position

    def get_choice(self):
        """
        Return value of selected menu item.
        """
        return self.choices[self.position]

    def set_position(self, idx):
        """
        Set index of selected menu item.
        """
        if idx < 0:
            self.position = 0
        elif idx >= len(self.choices) - 1:
            self.position = len(self.choices) - 1
        else:
            self.position = idx

    def render_choices(self):
        """
        Render individual titles from choices. They are not drawed on screen, just rendered to memory.

        Return (titles, max_w, max_h), where
            titles is list of rendered objects with individual choices
            max_w is widest title in choices
            max_h is tallest title in choices
        """
        max_w = 0
        max_h = 0
        titles = []

        for idx, title in enumerate(self.choices):
            if idx == self.get_position():
                color = self.config['cursor_color']
            else:
                color = self.config['screen_color']
            text = self.font.render(title, True, color)
            titles.append(text)

            # find biggest title
            text_size = text.get_rect().size
            if text_size[0] > max_w:
                max_w = text_size[0]
            if text_size[1] > max_h:
                max_h = text_size[1]

        return titles, max_w, max_h

    def render(self):
        """
        Render screen with menu.
        """
        # render titles
        titles, max_w, max_h = self.render_choices()

        # calculate initial position
        x = (self.size[0] - max_w) / 2
        y = (self.size[1] - (max_h + self.config['y_spacing']) * len(self.choices) - self.config['y_spacing']) / 2

        # render screen
        self.screen.fill(self.config['screen_background'])
        for idx, title in enumerate(self.choices):
            # render bar
            if idx == self.get_position():
                rect = [x - self.config['x_padding'],
                        y - self.config['y_padding'],
                        max_w + 2 * self.config['x_padding'],
                        max_h + 2 * self.config['y_padding']]
                self.screen.fill(self.config['cursor_background'], rect=rect)
            self.screen.blit(titles[idx], (x, y))
            y += max_h + self.config['y_spacing']

        pygame.display.update()

    def move_up(self):
        """
        Helper method, move cursor up and render whole menu screen.
        """
        self.set_position(self.get_position() - 1)
        self.render()

    def move_down(self):
        """
        Helper method, move cursor down and render whole menu screen.
        """
        self.set_position(self.get_position() + 1)
        self.render()

    def run(self):
        """
        Main method, take care about menu controls.
        """
        self.choices = get_entries(self.dirpath, condition=check_dir)
        if not self.choices:
            return STATE_MISSING_SOURCE

        # initial render of menu screen
        self.set_position(self.initial_position)
        self.render()

        # main loop
        state = None
        clock = pygame.time.Clock()
        counter = 0
        while state not in [STATE_QUIT, STATE_MISSING_SOURCE, STATE_ACTION]:
            clock.tick(self.fps)

            # control menu
            state = get_state()
            if state == STATE_NEXT:
                self.move_down()
            elif state == STATE_PREV:
                self.move_up()

            # check presence of source dir
            if counter == self.sleep * self.fps:
                if not source_exist(self.dirpath):
                    return STATE_MISSING_SOURCE
                counter = 0
            else:
                counter += 1

        return state
