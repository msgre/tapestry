import os
import re
import pygame
import pygame.locals
import subprocess

from .detective import get_entries, check_file
from .states import STATE_BACK
from .view import View


class Video(View):
    """
    Play first video in provided directory through mplayer.
    """
    filename_re = re.compile(r'^[^.].+\.(mp4|avi|mpg|mpeg)$', re.IGNORECASE)

    def run(self):
        files = self.filter_files(get_entries(self.dirpath, condition=check_file))
        if len(files):
            self.display.screen.fill((0, 0, 0))
            pygame.display.quit()

            # take first video file in directory and play it
            videofile = os.path.join(self.dirpath, files[0])
            subprocess.run(['mplayer', '-fs', '-vo', 'fbdev', videofile])
        
        return STATE_BACK
