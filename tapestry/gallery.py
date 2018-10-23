import math
import os
import pygame
import pygame.locals
import re
import time

from config import GalleryConfig, TitlesConfig
from detective import get_entries, check_file
from states import get_state, STATE_ACTION, STATE_BACK, STATE_MISSING_SOURCE, STATE_NEXT, STATE_PREV, STATE_QUIT
from view import View


class Gallery(View):
    filename_re = re.compile(r'^[^.].+\.(jpg|jpeg|gif|png|bmp)$', re.IGNORECASE)

    def load_config(self):
        gc = GalleryConfig(self.dirpath)
        status, config = gc.process()

        self.autoplay = config['autoplay']
        self.y_spacing = config['margin'] * 2 + config['fontsize']
        self.font = self.display.load_font(config['fontsize'])

        if not status:
            print('No configuration file found.')
        
        config_msg = []
        for k, v in config.items():
            config_msg.append('{k}={v}'.format(k=k, v=v))
        print("Configuration: {}".format(', '.join(config_msg)))

        return config

    def load_titles(self):
        tc = TitlesConfig(self.dirpath)
        status, config = tc.process()

        if not status:
            print('No titles file found.')

        return config

    def get_optimal_size(self, img_width, img_height):
        """
        Calculate optimal image size for given size.
        """
        display_width, display_height = self.display.size
        display_height -= self.y_spacing

        if display_width < img_width:
            width = display_width
            height = display_width / img_width * img_height
        elif display_height < img_height:
            height = display_height
            width = display_height / img_height * img_width
        elif display_width > img_width and display_height > img_height:
            width = display_width
            height = display_width / img_width * img_height
        else:
            width = display_width
            height = display_height

        if height > display_height:
            height = display_height
            width = display_height / img_height * img_width

        return (int(width), int(height))

    def get_state(self):
        """
        Return current state according to events on keyboard (and timer).
        """
        state = get_state()
        if state == STATE_ACTION:
            self.autoplay = not self.autoplay
        if state is not None:
            if state == STATE_ACTION and not self.autoplay:
                pygame.time.set_timer(pygame.USEREVENT, 0)
            else:
                self.autoplay = True
                pygame.time.set_timer(pygame.USEREVENT, 0)
                pygame.time.set_timer(pygame.USEREVENT, self.config['delay'])

        return state

    def render_screen(self, imgpath, title):
        """
        Render provided image on screen.
        """
        display_width, display_height = self.display.size

        # open and resize source image
        print(imgpath)
        img = pygame.image.load(imgpath)
        img_size = img.get_rect().size
        optimal_size = self.get_optimal_size(img_size[0], img_size[1])
        img = pygame.transform.smoothscale(img, optimal_size)

        # put image on screen (centered, bg color)
        self.display.screen.fill(self.config['screen_background'])
        x = math.ceil((display_width - optimal_size[0]) / 2)
        #y = math.ceil((display_height - optimal_size[1]) / 2)
        y = 0
        self.display.screen.blit(img, (x, y))

        # pause symbol on screen
        if not self.autoplay:
            pause = self.display.pause
            self.display.screen.blit(pause['img'], (pause['x'], pause['y']))

        # optional title
        print(title)
        if title:
            text = self.font.render(title, True, self.config['screen_color'])
            text_size = text.get_rect().size
            text_x = display_width / 2 - text_size[0] / 2
            text_y = display_height - self.y_spacing + round(self.config['fontsize'] * 0.1)
            print(text_x)
            print(text_y)
            self.display.screen.blit(text, (text_x, text_y))
            # self.display.screen.blit(text, (1000, 0))

        pygame.display.update()

    def run(self):
        # get images 
        files = get_entries(self.dirpath, condition=check_file)
        files = self.filter_files(files)
        if not files:
            return STATE_MISSING_SOURCE

        # load configuration files
        self.config = self.load_config()
        titles = self.load_titles()
        print(titles)

        # initialize main loop
        clock = pygame.time.Clock()
        idx = 0
        old_filepath = None
        old_autoplay = None
        files_len = len(files)
        state = None

        if self.autoplay:
            # USEREVENT is same as STATE_NEXT state
            pygame.time.set_timer(pygame.USEREVENT, self.config['delay'])

        # main loop
        while state not in [STATE_QUIT, STATE_MISSING_SOURCE, STATE_BACK]:
            clock.tick(self.fps)
            state = self.get_state()

            if state == STATE_NEXT:
                idx += 1
                if idx > files_len - 1:
                    idx = files_len - 1
            elif state == STATE_PREV:
                idx -= 1
                if idx < 0:
                    idx = 0

            if state or old_filepath is None:
                filepath = os.path.join(self.dirpath, files[idx])
                if os.path.exists(filepath):
                    if old_filepath != filepath or self.autoplay != old_autoplay:
                        self.render_screen(filepath, titles.get(files[idx]))
                    old_filepath = filepath
                    old_autoplay = self.autoplay
                else:
                    state = STATE_MISSING_SOURCE

        self.display.screen.fill(self.config['screen_background'])
        pygame.time.set_timer(pygame.USEREVENT, 0)
        # pygame.display.quit()  # TODO: ???

        return state
