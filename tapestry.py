import argparse
import os
import pygame
import pygame.locals

from tapestry.config import MenuConfig
from tapestry.detective import check_file, get_entries, source_exist
from tapestry.display import Display
from tapestry.gallery import Gallery
from tapestry.menu import Menu
from tapestry.states import STATE_MISSING_SOURCE, STATE_QUIT
from tapestry.video import Video


SLEEP = 3

# CLI args initialization
parser = argparse.ArgumentParser()
parser.add_argument('dirpath', type=str)
args = parser.parse_args()

# main loop
state = None
last_menu_position = 0
while state != STATE_QUIT:

    # get menu configuration
    mc = MenuConfig(args.dirpath)
    status, menu_config = mc.process()

    # initialize display
    display = Display(menu_config)
    display.init_screen()
    
    # source directory detection
    # if there are no data on USB disk, we need to display message and wait until it will be mounted
    if not source_exist(args.dirpath):
        display.render_no_source()
        while not source_exist():
            sleep(SLEEP)
        continue  # ie. go back to menu config and display init

    # menu
    menu = Menu(args.dirpath, display, menu_config, position=last_menu_position, sleep=SLEEP)
    state = menu.run()
    if state == STATE_MISSING_SOURCE:
        continue
    elif state == STATE_QUIT:
        break
    last_menu_position = menu.get_position()

    # react to user selection in menu
    if state is not None:
        # item in menu was choosen
        choosen_path = os.path.join(args.dirpath, menu.get_choice())
        files = get_entries(choosen_path, condition=check_file)

        # find appropriate view according to directory content
        View = None
        for cls in [Video, Gallery]:
            fn = getattr(cls, 'filter_files')
            if len(fn(files)):
                View = cls
                break
        if View is None:
            continue

        # pass control to gallery or video view
        p = View(choosen_path, display)
        state = p.run()

# close pygame
pygame.display.quit()
pygame.quit()
