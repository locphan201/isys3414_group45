import pygame as pg
from theme import *

def detail_txt():
    detail = []
    detail.append('In Nana\'s Bakery, we only sell the world\'s class product. In')
    detail.append('2010, our founder, Nana started a small bakery with only 500$')
    detail.append('and a great passion. After 10 years of hard-working, Nana\'s Bakery is now one of')
    detail.append('the most famous bakery in the country. Our aim is to deliver to our customer')
    detail.append('the best experience, spread the flavour of cake to everyone.')
    detail.append('In our bakery, customer will have a wide range of option, from western')
    detail.append('to oriental cuisine, we also serve special product in special seasion.')
    detail.append('Just give us a try, we will make you surprise.')
    detail.append('And remember, a cake make a day!!!')
    return detail

def draw_about_us(window):
    # Set fonts
    header = pg.font.Font(font4, 34)
    paragraph = pg.font.Font(font1,20)
    
    # Setup text
    about_us = header.render('ABOUT US', True, BLACK)
    about_us = pg.transform.rotate(about_us, 90)
    about_us2 = header.render('Nana\'s Bakery', True,BLACK)
    about_us2 = pg.transform.rotate(about_us2, -90)
    detail =  detail_txt()
    
    # Load and resize images
    bakery_img=pg.image.load('Resources\\Images\\About_us\\thumb0.jpg')
    bakery_img=pg.transform.scale(bakery_img, (390,256))
    bakery_img2=pg.image.load('Resources\\Images\\About_us\\thumb1.jpg')
    bakery_img2=pg.transform.scale(bakery_img2, (390,256))
    
    # Header image
    pg.draw.rect(window,PURPLE, (0, 100, 432, 256))
    window.blit(bakery_img, (50, 100))
    window.blit(about_us, (0, 130))
    
    # Text
    for i in range(len(detail)):
        x = 0
        if i == 0 or i == 6:
            x = 50
        elif i == 8:
            x = 80
        elif i == 9:
            x = 100
        window.blit(paragraph.render(detail[i], True, BLACK), (x, 356+i*24))

    # Footer image
    pg.draw.rect(window, BLUE, (0, 612, 432, 256))
    window.blit(bakery_img2, (0, 612))
    window.blit(about_us2, (390, 640))