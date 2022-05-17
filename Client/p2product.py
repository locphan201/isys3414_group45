import pygame as pg
from theme import *
from db_connector import get_product_infos

def product_imgs():
    items = []
    item_infos = get_product_infos()
    for i in item_infos:
        product = i[0].lower().replace(' ','_') + '.jpg'
        image = pg.image.load('Resources\\Images\\Products\\' + product)
        image = pg.transform.scale(image, (100, 100))
        items.append([i[0], image, 0, i[1]])
    return items

items = product_imgs()

def check_hit_product(scroll_y, x, y):
    global items
    for i in range(len(items)):
        if (30 < x and x < 402) and (scroll_y+150 + i*125 < y and y < scroll_y+250 + i*125):
            items[i][2] += 1
            return [items[i][0], items[i][2]*items[i][3]]
    return []

def update_one(index, quantity):
    global items
    items[index][2] += quantity

def remove_quantities():
    global items
    for i in items:
        i[2] = 0

def draw_product_page(window, scroll_y):
    global items
    
    font = pg.font.SysFont(font2, 28)
    
    for i in range(len(items)):
        window.blit(items[i][1], (30, scroll_y+150 + i*125))
        window.blit(font.render(items[i][0], True, BLACK), (165, scroll_y+175 + i*120))
        window.blit(font.render('$ ' + str(items[i][3]), True, BLACK), (325, scroll_y+175 + i*120 + 40))
        
        if items[i][2] > 0:
            pg.draw.circle(window, LIGHT_RED, (35, scroll_y+155 + i*125), 15)
            quantity = font.render(str(items[i][2]), True, WHITE)
            rect = quantity.get_rect(center=(35, scroll_y+155 + i*125))
            window.blit(quantity, (rect.x, rect.y))  