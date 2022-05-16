import pygame as pg
from db_connector import *
from theme import *

PRODUCT_INFO = [['ID', pg.Rect(555, 270, 500, 50), ''], 
                ['Name', pg.Rect(555, 350, 500, 50), ''], 
                ['Price', pg.Rect(555, 430, 500, 50), '']]
UPDATE, DELETE = pg.Rect(840, 530, 150, 50), pg.Rect(622, 530, 150, 50)
FIND = pg.Rect(1100, 270, 100, 50)
active_txt = -1
update = False

def get_info():
    global PRODUCT_INFO
    return PRODUCT_INFO

def show(window, font, text, x, y, color=BLACK, align=-1):
    txt = font.render(text, True, color)
    if align == -1:
        window.blit(txt, (x, y))
    elif align == 0:
        rect = txt.get_rect(center=(x, y))
        window.blit(txt, (rect.x, rect.y))

def reset_txt():
    global PRODUCT_INFO
    for i in range(1, len(PRODUCT_INFO)):
        PRODUCT_INFO[i][2] = ''

def process(type):
    global PRODUCT_INFO, update
    if PRODUCT_INFO[0][2] == '' or not PRODUCT_INFO[0][2].isdigit():
        return
    
    if type == 'update':
        update_product(PRODUCT_INFO[0][2], PRODUCT_INFO[1][2], PRODUCT_INFO[2][2])
        update = True
    elif type == 'delete':
        delete_product(PRODUCT_INFO[0][2])
    elif type == 'find':
        result = get_product(PRODUCT_INFO[0][2])
        if result != None:
            for i in range(1, len(result)):
                PRODUCT_INFO[i][2] = str(result[i])
        else:
            reset_txt()

def input_txt_product(c):
    global PRODUCT_INFO, active_txt, update
    if c == -1:
        PRODUCT_INFO[active_txt][2] = PRODUCT_INFO[active_txt][2][:-1]
        update = False
    elif active_txt != -1:
        PRODUCT_INFO[active_txt][2] += c
        update = False

def check_event_product(pos):
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

def draw_product(window):
    global UPDATE, CREATE, DELETE, FIND, update
    
    info = get_info()
    title = pg.font.Font(font4, 30)
    header = pg.font.Font(font4, 25)
    contxt = pg.font.Font(font4, 20)
    
    show(window, title, 'Product Information', 800, 200, LIGHT_RED, 0)
    pg.draw.line(window, LIGHT_RED, (655, 215), (948, 215), 4)
    
    for i in range(len(info)):
        show(window, header, info[i][0], 425, 280+80*i)
        if update:
            pg.draw.rect(window, LIGHT_GREEN, info[i][1], 2)
        elif i == active_txt:
            pg.draw.rect(window, LIGHT_RED, info[i][1], 2)
        else:
            pg.draw.rect(window, GREY, info[i][1], 2)
        show(window, contxt, str(info[i][2]), 570, 285+80*i)
        
    pg.draw.rect(window, LIGHT_GREEN, UPDATE)
    pg.draw.rect(window, BLACK, UPDATE, 2)
    show(window, header, 'Update', UPDATE.x+UPDATE.w/2, UPDATE.y+UPDATE.h/2, BLACK, 0)
    
    pg.draw.rect(window, PINK, DELETE)
    pg.draw.rect(window, BLACK, DELETE, 2)
    show(window, header, 'Delete', DELETE.x+DELETE.w/2, DELETE.y+DELETE.h/2, BLACK, 0)
    
    pg.draw.rect(window, LIGHT_BLUE, FIND)
    pg.draw.rect(window, BLACK, FIND, 2)
    show(window, header, 'Find', FIND.x+FIND.w/2, FIND.y+FIND.h/2, BLACK, 0)