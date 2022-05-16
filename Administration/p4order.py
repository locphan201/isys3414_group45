import pygame as pg
from db_connector import *
from theme import *

ORDERS, ITEMS = [], []
active_ord = -1
img = pg.image.load('Resources\\Images\\refresh.png')
img = pg.transform.scale(img, (50, 50))

def update_orders():
    global ORDERS, ITEMS
    ORDERS, ITEMS = get_incompleted_orders()

update_orders()

def show(window, font, text, x, y, color=BLACK, align=-1):
    txt = font.render(text, True, color)
    if align == -1:
        window.blit(txt, (x, y))
    elif align == 0:
        rect = txt.get_rect(center=(x, y))
        window.blit(txt, (rect.x, rect.y))

def draw_card(window, x, y, info, active):
    font = pg.font.Font(font3, 20)
    pg.draw.rect(window, LIGHT_GREY, (x, y, 180, 180))
    pg.draw.rect(window, LIGHT_BLUE, (x, y, 180, 45))
    if active:
        pg.draw.rect(window, LIGHT_RED, (x, y, 180, 180), 3)
    else:
        pg.draw.rect(window, GREY, (x, y, 180, 180), 2)
    show(window, font, '#'+str(info[0]), x+15, y+10)
    show(window, font, info[1], x+90, y+70, BLACK, 0)
    show(window, font, info[2], x+90, y+120, BLACK, 0)
    show(window, font, '$'+str(info[3]), x+100, y+150)

def check_event_orders(pos):
    global active_ord, ORDERS
    x, y = pos[0] - 100, pos[1] - 120
    
    if 100 <= pos[0] <= 150 and 25 <= pos[1] <= 75:
        update_orders()
        active_ord = -1
    
    if x < 0 or y < 0:
        return
    
    if len(ORDERS) > 0:
        if 1164 < pos[0] < 1304 and 680 < pos[1] < 720:
            update_order_status(ORDERS[active_ord][0], 'CANCELLED')
            update_orders()
            active_ord = -1
        elif 1318 < pos[0] < 1458 and 680 < pos[1] < 720:
            update_order_status(ORDERS[active_ord][0], 'DELIVERED')
            update_orders()
            active_ord = -1
        
    index_x = int(x / 200)
    index_y = int(y / 230)
    
    if x - index_x * 200 < 180 or y - index_y * 230 < 180:
        active_ord = index_x + index_y * 5

def draw_current_order(window):
    global ORDERS, ITEMS, active_ord
    
    ft1 = pg.font.Font(font3, 30)
    ft2 = pg.font.Font(font3, 20)
    
    show(window, ft1, 'On Going Orders', 160, 30)
    pg.draw.line(window, BLACK, (160, 70), (380, 70), 3)
    
    pg.draw.rect(window, LIGHT_GREY, (1150, 150, 324, 576))
    pg.draw.rect(window, BLACK, (1150, 150, 324, 576), 2)
    show(window, ft1, 'Order #', 1160, 160)
    pg.draw.line(window, BLACK, (1150, 200), (1473, 200), 2)
    
    if ORDERS != None:
        if not (0 <= active_ord < len(ORDERS)):
            show(window, ft2, 'Choose an order', 1312, 438, BLACK, 0)
            active_ord = -1
        else:
            current = ITEMS[active_ord]
            show(window, ft1, str(ORDERS[active_ord][0]), 1275, 160, RED)
    
            for i in range(len(current)):
                show(window, ft2, str(current[i][1]) + ' x ' + str(current[i][0]), 1200, 220+i*40)   
    
    pg.draw.circle(window, LIGHT_RED, (1184, 700), 20)
    pg.draw.rect(window, LIGHT_RED, (1184, 680, 100, 40))
    pg.draw.circle(window, LIGHT_RED, (1284, 700), 20)
    show(window, ft2, 'Cancel', 1234, 700, BLACK, 0)
    
    pg.draw.circle(window, LIGHT_GREEN, (1338, 700), 20)
    pg.draw.rect(window, LIGHT_GREEN, (1338, 680, 100, 40))
    pg.draw.circle(window, LIGHT_GREEN, (1438, 700), 20)
    show(window, ft2, 'Delivered', 1388, 700, BLACK, 0)
    
def draw_orders(window):
    global ORDERS, active_ord, img
    
    window.blit(img, (100, 25))
    
    draw_current_order(window)
    
    for i in range(len(ORDERS)):
        active = (i == active_ord)
        if int(i / 5) == 0:
            draw_card(window, 100+i*200, 120, ORDERS[i], active)
        elif int(i / 5) == 1:
            draw_card(window, 100+(i-5)*200, 350, ORDERS[i], active)
        elif int(i / 5) == 2:
            draw_card(window, 100+(i-10)*200, 580, ORDERS[i], active)