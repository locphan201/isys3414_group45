import pygame as pg
from theme import *

items = []
add, sub = [], []
button = pg.Rect(55, 705, 322, 50)

def sum():
    global items
    total = 0
    for i in range(len(items)):
        total += items[i][1] * items[i][2]
    return total

def show(window, font, text, x, y, color=BLACK):
    txt = font.render(text, True, color)
    rect = txt.get_rect(center=(x, y))
    window.blit(txt, (rect.x, rect.y))

def add_item(name, price):
    global items, add, sub
    
    for i in range(len(items)):
        if items[i][0] == name:
            items[i][1] += 1
            return
    
    items.append([name, 1, price])
    sub.append(pg.Rect(235, 180+50*(len(items)-1), 10, 10))
    add.append(pg.Rect(275, 180+50*(len(items)-1), 10, 10))

def remove(index):
    global items, add, sub
    items.pop(index)
    add, sub = [], []
    for i in range(len(items)):
        sub.append(pg.Rect(235, 180+50*i, 10, 10))
        add.append(pg.Rect(275, 180+50*i, 10, 10))

def remove_all():
    global items, add, sub
    items, add, sub = [], [], []

def get_items():
    global items
    return [items, sum()]

def check_hit_button(x, y):
    global add, sub, button
    
    for i in range(len(add)):
        if add[i].collidepoint(x, y):
            items[i][1] += 1
            return 1, i
        
        if sub[i].collidepoint(x, y):
            items[i][1] -= 1
            if items[i][1] == 0:
                remove(i)
            return -1, i
    
    if button.collidepoint(x, y):
        if len(items) <= 0:
            return 0, 1
        return 2, 0
    
    return 0, 1

def draw_cart(window):
    global items, button, add, sub
    
    # Fonts
    item_font = pg.font.SysFont('Arial', 21)
    amount_font = pg.font.SysFont('Arial', 18)
    TAG = pg.font.SysFont('Arial', 22)

    window.blit(TAG.render("Item", True, BLACK), (30, 125))
    window.blit(TAG.render("Amount", True, BLACK), (225, 125))
    window.blit(TAG.render("Price", True, BLACK), (350, 125))
    pg.draw.line(window, BLACK, (0, 150), (500, 150), 2)

    if len(items) > 0:
        for i in range(len(items)):
            window.blit(item_font.render(str(items[i][0]), True, BLACK), (30, 175+50*i))
            show(window, amount_font, str(items[i][1]), 260, 185+50*i)
            show(window, amount_font, '$' + str(items[i][1]*items[i][2]), 375, 185+50*i)
    
        for i in range(len(add)):
            pg.draw.rect(window, BLACK, add[i])
            show(window, amount_font, "+", add[i].x+5, add[i].y+3, WHITE)
            pg.draw.rect(window, BLACK, sub[i])
            show(window, amount_font, "-", sub[i].x+5, sub[i].y+3, WHITE)
    else:
        show(window, TAG, "Cart is empty", 216, 350)
    
    show(window, item_font, "Total", 50, 670)
    show(window, amount_font, '$' + str(sum()), 380, 670)
    
    pg.draw.rect(window, LIGHT_RED, button)
    pg.draw.circle(window, LIGHT_RED, (button.x, button.y+button.h/2), button.h/2)
    pg.draw.circle(window, LIGHT_RED, (button.x+button.w, button.y+button.h/2), button.h/2)
    show(window, TAG, 'Checkout', button.x+button.w/2, button.y+button.h/2, WHITE)