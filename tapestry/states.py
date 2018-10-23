import pygame

STATE_BACK = 'back'
STATE_NEXT = 'next'
STATE_PREV = 'prev'
STATE_ACTION = 'action'
STATE_MISSING_SOURCE = 'missing'
STATE_QUIT = 'quit'


def get_state():
    state = None
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            state = STATE_QUIT
        elif event.type == pygame.USEREVENT:
            state = STATE_NEXT
        elif event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.K_0:
                state = STATE_NEXT
            elif event.key == pygame.K_9:
                state = STATE_PREV
            elif event.key == pygame.K_SPACE:
                state = STATE_ACTION
            elif event.key == pygame.K_ESCAPE:
                state = STATE_QUIT
            elif event.key == pygame.K_q:
                state = STATE_BACK
        if state is not None:
            break
    return state
