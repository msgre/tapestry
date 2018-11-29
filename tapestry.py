import argparse
import json
import os
import pygame
import pygame.locals
import signal
from time import sleep

from tapestry.config import MenuConfig
from tapestry.detective import check_file, get_entries, source_exist
from tapestry.display import Display
from tapestry.gallery import Gallery
from tapestry.menu import Menu
from tapestry.states import STATE_MISSING_SOURCE, STATE_QUIT
from tapestry.video import Video


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    pygame.display.quit()
    pygame.quit()
    raise OSError("Couldn't open device!")

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)


SLEEP = 3

# CLI args initialization
parser = argparse.ArgumentParser()
parser.add_argument('dirpath', type=str)
args = parser.parse_args()
print('Starting tapestry. Source dirpath={}'.format(args.dirpath), flush=True)

# main loop
state = None
last_menu_position = 0
while state != STATE_QUIT:
    print('Entering main loop', flush=True)

    # get menu configuration
    mc = MenuConfig(args.dirpath)
    status, menu_config = mc.process()
    print('Menu configuration: {}'.format(json.dumps(menu_config)), flush=True)

    # initialize display
    display = Display(menu_config)
    display.init_screen()
    print('Display initialized', flush=True)
    
    # source directory detection
    # if there are no data on USB disk, we need to display message and wait until it will be mounted
    if not source_exist(args.dirpath):
    #if 1:
        display.render_no_source()
        while not source_exist(args.dirpath):
            print("Source doesn't exists.", flush=True)
            sleep(SLEEP)
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


