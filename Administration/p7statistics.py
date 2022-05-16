import pygame as pg
from db_connector import *
from theme import *

MONTHLY = []
NUM_CUS, INCOME = 0, 0
img = pg.image.load('Resources\\Images\\customerpng.png')
img = pg.transform.scale(img, (50, 50))

def update_monthly():
    global MONTHLY
    MONTHLY = get_monthly_revenue()

def update_customers():
    global NUM_CUS
    NUM_CUS = get_total_customers()

def update_income():
    global INCOME
    INCOME = get_total_income()

def update():
    update_monthly()
    update_customers()
    update_income()

update()

def show(window, font, text, x, y, color=BLACK, align=-1):
    txt = font.render(text, True, color)
    if align == -1:
        window.blit(txt, (x, y))
    elif align == 0:
        rect = txt.get_rect(center=(x, y))
        window.blit(txt, (rect.x, rect.y))

def draw_revenue_by_month(window):
    global MONTHLY
    header = pg.font.Font(font1, 40)
    font = pg.font.Font(font4, 18)
    
    BASE = 400
    
    show(window, header, 'Revenue / Expense', 250, BASE-350, DARK_BLUE, 0)
    pg.draw.line(window, DARK_BLUE, (140, BASE-325), (370, BASE-325), 2)

    MAX = max(MONTHLY[0])
    MAX2 = max(MONTHLY[1])
    if MAX < MAX2:
        MAX = MAX2
    for i in range(6):
        if i > 0:
            pg.draw.line(window, BLACK, (135, BASE-i*50), (145, BASE-i*50), 2)
        show(window, font, str(int(MAX/5*i)), 105, BASE-i*50-10)

    for i in range(12):
        show(window, font, str(i+1), 195+i*100, BASE+25, BLACK, 0)
        length1 = int(250 * MONTHLY[0][i] / MAX)
        pg.draw.rect(window, LIGHT_BLUE, (155+i*100, BASE-length1, 40, length1))
        pg.draw.rect(window, BLACK, (155+i*100, BASE-length1, 40, length1+1), 2)
        if MONTHLY[0][i] > 0:
           show(window, font, str(int(MONTHLY[0][i])), 175+i*100, BASE-length1-10, BLACK, 0)
           
        length2 = int(250 * MONTHLY[1][i] / MAX)
        pg.draw.rect(window, LIGHT_ORANGE, (195+i*100, BASE-length2, 40, length2))
        pg.draw.rect(window, BLACK, (195+i*100, BASE-length2, 40, length2+1), 2)
        if MONTHLY[1][i] > 0:
           show(window, font, str(int(MONTHLY[1][i])), 215+i*100, BASE-length2-10, BLACK, 0)

    pg.draw.line(window, BLACK, (140, BASE-300), (140, BASE), 2)
    pg.draw.line(window, BLACK, (140, BASE), (1400, BASE), 2)
    
    pg.draw.rect(window, LIGHT_BLUE, (200, BASE+75, 25, 25))
    pg.draw.rect(window, BLACK, (200, BASE+75, 25, 25), 2)
    show(window, font, 'Revenue', 235, BASE+78)
    
    pg.draw.rect(window, LIGHT_ORANGE, (400, BASE+75, 25, 25))
    pg.draw.rect(window, BLACK, (400, BASE+75, 25, 25), 2)
    show(window, font, 'Expense', 435, BASE+78)

def draw_total_customers(window):
    global NUM_CUS, img
    
    header = pg.font.Font(font1, 40)
    font = pg.font.Font(font4, 25)
    
    show(window, header, 'Number of Customers', 300, 550, DARK_BLUE, 0)
    pg.draw.line(window, DARK_BLUE, (175, 575), (430, 575), 2)
    
    window.blit(img, (250, 600))
    show(window, font, str(NUM_CUS), 305, 610)

def draw_total_income(window):
    global INCOME
    
    header = pg.font.Font(font1, 40)
    font = pg.font.Font(font4, 25)
    
    show(window, header, 'Total Income', 700, 550, DARK_BLUE, 0)
    pg.draw.line(window, DARK_BLUE, (625, 575), (775, 575), 2)
    
    show(window, font, '$'+str(INCOME), 700, 625, BLACK, 0)

def draw_statistics(window):
    draw_revenue_by_month(window)
    draw_total_customers(window)
    draw_total_income(window)