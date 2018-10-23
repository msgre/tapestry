import os
import pygame
import pygame.locals


SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)


class Display:
    size = None
    screen = None
    font = None
    pause = None

    def __init__(self, config):
        self.config = config
        self.fontpath = self.get_asset_path('roboto_condensed.ttf')
        self.pausepath = self.get_asset_path('pause.png')

    def init_screen(self, complete=True):
        """
        Basic initialization, mostly related to PyGame and framebuffer.
        """
        if complete:
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            pygame.init()
        self.size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.font = self.load_font(self.config['fontsize'])
        self.pause = self.load_pause()

    def render_no_source(self):
        """
        Common render screen with information that source directory (most probably on USB) disappear
        (someone could remove it).
        """
        self.screen.fill(self.config['screen_background'])
        msg = 'Čekám na připojení USB klíčenky s daty pro projekci.'
        text = self.font.render(msg, True, self.config['screen_color'])
        text_size = text.get_rect().size
        text_x = self.size[0] / 2 - text_size[0] / 2
        text_y = self.size[1] / 2 - text_size[1] / 2
        self.screen.blit(text, (text_x, text_y))
        pygame.display.update()

    def get_asset_path(self, filename):
        """
        Return path to requested asset file (those are stored next to python scripts).
        """
        path = os.path.abspath(os.path.join(SCRIPT_DIR, filename))
        if not os.path.exists(path) or not os.path.isfile(path):
            raise RuntimeError
        return path

    def load_font(self, size):
        """
        Return Font instance of given size.
        """
        return pygame.font.Font(self.fontpath, size)

    def load_pause(self):
        """
        Return dict structure with pause image and center position on screen.
        """
        img = pygame.image.load(self.pausepath)
        img_size = img.get_rect().size
        x = self.size[0] / 2 - img_size[0] / 2
        y = self.size[1] / 2 - img_size[1] / 2
        return {'img': img, 'x': x, 'y': y}
