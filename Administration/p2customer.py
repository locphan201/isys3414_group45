import pygame as pg
from db_connector import *
from theme import *

CUSTOMER_INFO = [['ID', pg.Rect(555, 170, 500, 50), ''],
                 ['Name', pg.Rect(555, 250, 500, 50), ''],
                 ['Phone', pg.Rect(555, 330, 500, 50), ''],
                 ['Address', pg.Rect(555, 410, 500, 50), ''],
                 ['Email', pg.Rect(555, 490, 500, 50), ''],
                 ['Password', pg.Rect(555, 570, 500, 50), '']]
UPDATE, DELETE = pg.Rect(840, 675, 150, 50), pg.Rect(622, 675, 150, 50)
FIND = pg.Rect(1100, 170, 100, 50)
active_txt = -1
update = False

def get_info():
    global CUSTOMER_INFO
    return CUSTOMER_INFO

def reset_txt():
    global CUSTOMER_INFO
    for i in range(1, len(CUSTOMER_INFO)):
        CUSTOMER_INFO[i][2] = ''

def process(type):
    global CUSTOMER_INFO, update
    if CUSTOMER_INFO[0][2] == '' or not CUSTOMER_INFO[0][2].isdigit():
        return
    
    if type == 'update':
        update_customer(CUSTOMER_INFO[0][2], CUSTOMER_INFO[1][2], CUSTOMER_INFO[2][2], CUSTOMER_INFO[3][2], CUSTOMER_INFO[4][2], CUSTOMER_INFO[5][2])
        update = True
    elif type == 'delete':
        delete_customer(CUSTOMER_INFO[0][2])
    elif type == 'find':
        result = get_customer(CUSTOMER_INFO[0][2])
        if result != None:
            for i in range(1, len(result)):
                CUSTOMER_INFO[i][2] = result[i]
        else:
            reset_txt()

def input_txt_customer(c):
    global CUSTOMER_INFO, active_txt, update
    if c == -1:
        CUSTOMER_INFO[active_txt][2] = CUSTOMER_INFO[active_txt][2][:-1]
        update = False
    elif active_txt != -1:
        CUSTOMER_INFO[active_txt][2] += c
        update = False

def check_event_customer(pos):
    global UPDATE, DELETE, FIND, active_txt
    info = get_info()
    for i in range(len(info)):
        if info[i][1].collidepoint(pos):
            active_txt = i
            return
    
    if UPDATE.collidepoint(pos):
        process('update')
    elif DELETE.collidepoint(pos):
        process('delete')
    elif FIND.collidepoint(pos):
        process('find')

def show(window, font, text, x, y, color=BLACK, align=-1):
    txt = font.render(text, True, color)
    if align == -1:
        window.blit(txt, (x, y))
    elif align == 0:
        rect = txt.get_rect(center=(x, y))
        window.blit(txt, (rect.x, rect.y))

def draw_customer(window):
    global UPDATE, DELETE, FIND, active_txt, update
    info = get_info()
    title = pg.font.Font(font4, 30)
    header = pg.font.Font(font4, 25)
    contxt = pg.font.Font(font4, 20)
    
    show(window, title, 'Customer Information', 800, 100, LIGHT_RED, 0)
    pg.draw.line(window, LIGHT_RED, (655, 115), (948, 115), 4)
    
    for i in range(len(info)):
        show(window, header, info[i][0], 425, 180+80*i)
        if update:
            pg.draw.rect(window, LIGHT_GREEN, info[i][1], 2)
        elif i == active_txt:
            pg.draw.rect(window, LIGHT_RED, info[i][1], 2)
        else:
            pg.draw.rect(window, GREY, info[i][1], 2)
        show(window, contxt, info[i][2], 570, 185+80*i)
        
    pg.draw.rect(window, LIGHT_GREEN, UPDATE)
    pg.draw.rect(window, BLACK, UPDATE, 2)
    show(window, header, 'Update', UPDATE.x+UPDATE.w/2, UPDATE.y+UPDATE.h/2, BLACK, 0)
    
    pg.draw.rect(window, PINK, DELETE)
    pg.draw.rect(window, BLACK, DELETE, 2)
    show(window, header, 'Delete', DELETE.x+DELETE.w/2, DELETE.y+DELETE.h/2, BLACK, 0)
    
    pg.draw.rect(window, LIGHT_BLUE, FIND)
    pg.draw.rect(window, BLACK, FIND, 2)
    show(window, header, 'Find', FIND.x+FIND.w/2, FIND.y+FIND.h/2, BLACK, 0)