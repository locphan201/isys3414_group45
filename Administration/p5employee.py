import pygame as pg
from db_connector import *
from theme import *

EMPLOYEE_INFO = [['ID', pg.Rect(555, 140, 500, 50), ''],
                 ['Name', pg.Rect(555, 220, 500, 50), ''], 
                 ['Phone', pg.Rect(555, 300, 500, 50), ''], 
                 ['Salary', pg.Rect(555, 380, 500, 50), ''], 
                 ['Email', pg.Rect(555, 460, 500, 50), ''], 
                 ['Position', pg.Rect(555, 540, 500, 50), ''], 
                 ['Password', pg.Rect(555, 620, 500, 50), '']]
UPDATE, CREATE, DELETE = pg.Rect(860, 710, 150, 50), pg.Rect(665, 710, 150, 50), pg.Rect(470, 710, 150, 50)
FIND = pg.Rect(1100, 140, 100, 50)
active_txt = 0
update = False

def get_info():
    global EMPLOYEE_INFO
    return EMPLOYEE_INFO

def show(window, font, text, x, y, color=BLACK, align=-1):
    txt = font.render(text, True, color)
    if align == -1:
        window.blit(txt, (x, y))
    elif align == 0:
        rect = txt.get_rect(center=(x, y))
        window.blit(txt, (rect.x, rect.y))

def reset_txt():
    global EMPLOYEE_INFO
    for i in range(1, len(EMPLOYEE_INFO)):
        EMPLOYEE_INFO[i][2] = ''

def process(type):
    global EMPLOYEE_INFO, update
    if EMPLOYEE_INFO[0][2] == '' or not EMPLOYEE_INFO[0][2].isdigit():
        return
    
    if type == 'update':
        update_employee(EMPLOYEE_INFO[0][2], EMPLOYEE_INFO[1][2], EMPLOYEE_INFO[2][2], EMPLOYEE_INFO[3][2], EMPLOYEE_INFO[4][2], EMPLOYEE_INFO[5][2], EMPLOYEE_INFO[6][2])
        update = True
    elif type == 'delete':
        delete_employee(EMPLOYEE_INFO[0][2])
    elif type == 'find':
        result = get_employee(EMPLOYEE_INFO[0][2])
        if result != None:
            for i in range(1, len(result)):
                EMPLOYEE_INFO[i][2] = str(result[i])
        else:
            reset_txt()
    elif type == 'create':
        add_employee(EMPLOYEE_INFO[1][2], EMPLOYEE_INFO[2][2], EMPLOYEE_INFO[3][2], EMPLOYEE_INFO[4][2], EMPLOYEE_INFO[5][2], EMPLOYEE_INFO[6][2])
        update = True

def input_txt_employee(c):
    global EMPLOYEE_INFO, active_txt, update
    if c == -1:
        EMPLOYEE_INFO[active_txt][2] = EMPLOYEE_INFO[active_txt][2][:-1]
        update = False
    elif active_txt != -1:
        EMPLOYEE_INFO[active_txt][2] += c
        update = False

def check_event_employee(pos):
    global UPDATE, CREATE, DELETE, FIND, active_txt
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
    elif CREATE.collidepoint(pos):
        process('create')

def draw_employee(window):
    global UPDATE, CREATE, DELETE, active_txt, update
    
    info = get_info()
    title = pg.font.Font(font4, 30)
    header = pg.font.Font(font4, 25)
    contxt = pg.font.Font(font4, 20)
    
    show(window, title, 'Employee Information', 800, 75, LIGHT_RED, 0)
    pg.draw.line(window, LIGHT_RED, (650, 90), (950, 90), 4)
    
    for i in range(len(info)):
        show(window, header, info[i][0], 425, 150+80*i)
        if update:
            pg.draw.rect(window, LIGHT_GREEN, info[i][1], 2)
        elif i == active_txt:
            pg.draw.rect(window, LIGHT_RED, info[i][1], 2)
        else:
            pg.draw.rect(window, GREY, info[i][1], 2)
        show(window, contxt, str(info[i][2]), 570, 155+80*i)
        
    pg.draw.rect(window, LIGHT_GREEN, UPDATE)
    pg.draw.rect(window, BLACK, UPDATE, 2)
    show(window, header, 'Update', UPDATE.x+UPDATE.w/2, UPDATE.y+UPDATE.h/2, BLACK, 0)
    
    pg.draw.rect(window, LIGHT_BLUE, CREATE)
    pg.draw.rect(window, BLACK, CREATE, 2)
    show(window, header, 'Create', CREATE.x+CREATE.w/2, CREATE.y+CREATE.h/2, BLACK, 0)
    
    pg.draw.rect(window, PINK, DELETE)
    pg.draw.rect(window, BLACK, DELETE, 2)
    show(window, header, 'Delete', DELETE.x+DELETE.w/2, DELETE.y+DELETE.h/2, BLACK, 0)
    
    pg.draw.rect(window, LIGHT_BLUE, FIND)
    pg.draw.rect(window, BLACK, FIND, 2)
    show(window, header, 'Find', FIND.x+FIND.w/2, FIND.y+FIND.h/2, BLACK, 0)