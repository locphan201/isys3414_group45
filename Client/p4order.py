import pygame as pg
from db_connector import get_order_info, get_previous_orders, get_next_orders
from theme import *

cID = 0
ORDER_INFO, ITEMS = None, None
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def setup():
    pg.init()
    font = pg.font.SysFont(font2, 35)
    txt = font.render('<', True, BLACK)
    back = txt.get_rect(center=(30, 130))
    txt = font.render('>', True, BLACK)
    nxt = txt.get_rect(center=(400, 130))
    return back, nxt

back, nxt = setup()

def get_order(customer):
    global ORDER_INFO, ITEMS, cID
    cID = customer
    ORDER_INFO, ITEMS = get_order_info(customer)

def check_order_events(x, y):
    global ORDER_INFO, ITEMS, back, nxt, cID
    if back.collidepoint(x, y):
        order, items = get_previous_orders(cID, ORDER_INFO[0])
        if order != None:
            ORDER_INFO, ITEMS = order, items
    elif nxt.collidepoint(x, y):
        order, items = get_next_orders(cID, ORDER_INFO[0])
        if order != None:
            ORDER_INFO, ITEMS = order, items

def show(window, font, text, x, y, color=BLACK, align=-1):
    txt = font.render(text, True, color)
    if align == -1:
        window.blit(txt, (x, y))
    elif align == 0:
        rect = txt.get_rect(center=(x, y))
        window.blit(txt, (rect.x, rect.y))

def draw_order_page(window):
    global ORDER_INFO, ITEMS
    
    font = pg.font.SysFont(font2, 28)
    button = pg.font.SysFont(font2, 35)
    
    show(window, button, '<', back.x+back.w/2, back.y+back.h/2, BLACK, 0)
    show(window, font, 'Order Information', 216, 135, BLACK, 0)
    show(window, button, '>', nxt.x+nxt.w/2, nxt.y+nxt.h/2, BLACK, 0)
    
    if ORDER_INFO != None:
        date = str(ORDER_INFO[1]).split('-')
        date = date[2] + ' ' + MONTHS[int(date[1])] + ' ' + date[0]
    
        show(window, font, 'ID #'+str(ORDER_INFO[0]), 100, 175)
        show(window, font, date, 250, 175)
    
        if ORDER_INFO[3] == 'CANCELLED':
            show(window, font, ORDER_INFO[3], 216, 225, RED, 0)
        elif ORDER_INFO[3] == 'INCOMPLETED':
            show(window, font, 'ONGOING', 216, 225, BLACK, 0)
        elif ORDER_INFO[3] == 'COMPLETED':
            show(window, font, 'DELIVERED', 216, 225, GREEN, 0)
        
        show(window, font, 'Items', 30, 250, LIGHT_RED)
        pg.draw.line(window, LIGHT_RED, (30, 275), (80, 275), 4)
    
        for i in range(len(ITEMS)):
            show(window, font, str(ITEMS[i][1]) + ' x ' + str(ITEMS[i][0]), 50, 300+i*40)
            show(window, font, '$' + str(ITEMS[i][1]*ITEMS[i][2]), 350, 300+i*40)
    
        pg.draw.rect(window, (230, 230, 230), (20, 310+len(ITEMS)*40, 390, 50))
        show(window, font, 'Total', 30, 325+len(ITEMS)*40, LIGHT_RED)
        show(window, font, '$'+str(ORDER_INFO[2]), 337, 325+len(ITEMS)*40, LIGHT_RED)
    else:
        show(window, font, 'Order is empty.', 216, 350, BLACK, 0)