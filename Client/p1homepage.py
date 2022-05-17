import pygame as pg
from theme import *
from db_connector import get_best_seller

BEST_SELLERS = get_best_seller()
BUTTON = pg.Rect(300, 270, 80, 30)

def get_open_time():
    return ['Time: ', '8am - 9pm ', 'from Monday to Saturday']

def get_location():
    location = ['Location: ']
    location.append('123 Ly Thuong Kiet')
    location.append('A District, Ho Chi Minh city')
    return location

def get_contact():
    contact = ['Contact us: ', ]
    contact.append('Phone number: 012345678')
    contact.append('Email: Nanabakery@gmail.com')
    return contact

def draw_best_sellers(window):
    global BEST_SELLERS
    
    for i in range(len(BEST_SELLERS)):
        img = pg.image.load('Resources\\Images\\Products\\' + BEST_SELLERS[i][0].lower().replace(' ', '_') + '.jpg')
        img = pg.transform.scale(img, (150,150))
        if i <= 1:
            window.blit(img, (i*194+44, 313))
        else:
            window.blit(img, ((i-2)*194+44, 507))

def check_event_homepage(x, y):
    if BUTTON.collidepoint(x, y):
        return True

def draw_button(window):
    global BUTTON
    pg.draw.rect(window, LIGHT_RED, BUTTON)
    pg.draw.circle(window, LIGHT_RED, (BUTTON.x, BUTTON.y+BUTTON.h/2), 15)
    pg.draw.circle(window, LIGHT_RED, (BUTTON.x+BUTTON.w, BUTTON.y+BUTTON.h/2), 15)
    
    font = pg.font.SysFont('Arial', 17)
    txt = font.render('See more', True, WHITE)
    window.blit(txt, (BUTTON.x+BUTTON.w/2-txt.get_width()/2, BUTTON.y+BUTTON.h/2-txt.get_height()/2))

def update_best_sellers():
    global BEST_SELLERS
    BEST_SELLERS = get_best_seller()

def draw_homepage(window):
    # Set fonts
    title = pg.font.Font(font2, 25)
    header = pg.font.Font(font3, 25)
    paragraph =  pg.font.Font(font2, 20)
    fcontact = pg.font.SysFont('Arial', 18)
    
    # Setup texts
    best_seller = header.render('Best seller:', True, BLACK)
    welcome = title.render('Welcome to Nana\'s Bakery', True, BLACK)
    slogan = paragraph.render('Bake with love', True, BLACK)
    time = get_open_time()
    location = get_location()
    contact  = get_contact()

    # Load and resize image
    cake_img = pg.image.load('Resources\\Images\\Homepage\\thumb0.jpg')
    cake_img = pg.transform.scale(cake_img, (150,150))
    
    # Welcome and Infomation
    pg.draw.rect(window,PINK,(0,100,432,150))
    window.blit(cake_img, (0, 100))
    window.blit(welcome, (160,100))
    window.blit(slogan, (230, 130))
    
    for i in range(len(time)):
        if i == 0:
            window.blit(paragraph.render(time[i], True, BLACK), (180, 160))
        else:
            window.blit(paragraph.render(time[i], True, BLACK), (230, 160+(i-1)*20))
    
    for i in range(len(location)):
        if i == 0:
            window.blit(paragraph.render(location[i], True, BLACK), (150, 200))
        else:
            window.blit(paragraph.render(location[i], True, BLACK), (220, 200+(i-1)*20))  
    
    # Recomendation
    window.blit(best_seller, (20, 270))
    draw_button(window)
    draw_best_sellers(window)
    
    # Contact us
    pg.draw.rect(window,PINK,(0,700,432,70))
    for i in range(len(contact)):
        window.blit(fcontact.render(contact[i], True, BLACK), (0, 700+i*25))