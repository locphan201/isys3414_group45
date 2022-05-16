import pygame as pg
from p1dashboard import *
from p2customer import *
from p3product import *
from p4order import *
from p5employee import *
from p6accounting import *
from p7statistics import *
from theme import *

def setup_button(lst):
    tabs = []
    for i in range(len(lst)):
        tabs.append([lst[i], pg.Rect(30, 150+50*i, 200, 50)])
    return tabs
    
def background(window):
    window.fill(BACKGROUND)

def draw_pages(window, active):
    if active == 0:
        draw_dashboard(window)
    elif active == 1:
        draw_customer(window)
    elif active == 2:
        draw_product(window)
    elif active == 3:
        draw_orders(window)
    elif active == 4:
        draw_employee(window)
    elif active == 5:
        draw_accounting(window)
    elif active == 6:  
        draw_statistics(window)

def draw_tabs(window, tabs, h, isOpened, active):
    INDENT = 10
    h_font = pg.font.Font(font1, 40)
    tab = pg.font.Font(font4, 20)
    if isOpened:
        header = h_font.render("Nana's Bakery", True, WHITE)
        size = header.get_rect()
        width = INDENT*2+size[2]
        rect = pg.Rect(0, 0, width, 75)
        pg.draw.rect(window, TABS, (0, 0, width, h))
        pg.draw.line(window, WHITE, (10, 75), (width-10, 75))
        window.blit(header, (INDENT, (75-size[3])/2))
    
        for i in range(len(tabs)):
            if active == i:
                pg.draw.rect(window, PINK, (5, tabs[i][1].y+5, width-10, 40))
            text = tab.render(tabs[i][0], True, WHITE)
            window.blit(text, (tabs[i][1].x, tabs[i][1].y+((tabs[i][1].height-text.get_rect()[3])/2)))
        return rect
    else:
        header = h_font.render("N", True, WHITE)
        size = header.get_rect()
        width = size[2]+INDENT*2
        rect = pg.Rect(0, 0, width, 75)
        pg.draw.rect(window, TABS, (0, 0, width, h))
        pg.draw.line(window, WHITE, (10, 75), (width-10, 75))
        window.blit(header, (INDENT, (75-size[3])/2))
        
        rct = tabs[active][1]
        pg.draw.rect(window, PINK, (10, rct.y+10, width-20, 30))
        text = tab.render(tabs[active][0][:3], True, WHITE)
        window.blit(text, ((width-text.get_rect()[2])/2, rct.y+((rct.h-text.get_rect()[3])/2)))
        return rect
    
def draw_exit(window, button):
    pg.draw.rect(window, RED, button)
   
def main(window):
    running = True
    clock = pg.time.Clock()
    fps = 60
    surface = pg.display.get_surface()
    w, h = surface.get_width(), surface.get_height()
    
    header_button = pg.Rect(0, 0, w, 75)
    lst = ['Dashboard', 'Customers', 'Products', 'Orders',  'Employees', 'Accounting', 'Statistics']
    tabs = setup_button(lst)
    exit_button = pg.Rect(w-50, 0, 50, 50)
    
    tabOpened = True
    active = 0
    
    while running:
        clock.tick(fps)
        
        background(window)
        draw_pages(window, active)
        header_button = draw_tabs(window, tabs, h, tabOpened, active)
        draw_exit(window, exit_button)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                disconnect_db()
                break
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if tabOpened:
                    for i in range(len(tabs)):
                        if tabs[i][1].collidepoint(pg.mouse.get_pos()):
                            active = i
                if exit_button.collidepoint(pg.mouse.get_pos()):
                    running = False
                    break
                
                if header_button.collidepoint(pg.mouse.get_pos()):
                    tabOpened = not tabOpened
                
                if active == 1:
                    check_event_customer(pg.mouse.get_pos())
                elif active == 2:
                    check_event_product(pg.mouse.get_pos())
                elif active == 3:
                    check_event_orders(pg.mouse.get_pos())
                elif active == 4:
                    check_event_employee(pg.mouse.get_pos())
                elif active == 5:    
                    check_event_accounting(pg.mouse.get_pos())
            
            if event.type == pg.KEYDOWN:
                if active == 1:
                    if event.key == pg.K_BACKSPACE:
                        input_txt_customer(-1)
                    elif event.key == pg.K_SPACE:
                        input_txt_customer(' ')
                    else:
                        if event.unicode.isalnum() or event.unicode in '@.':
                            input_txt_customer(event.unicode)
                elif active == 2:
                    if event.key == pg.K_BACKSPACE:
                        input_txt_product(-1)
                    elif event.key == pg.K_SPACE:
                        input_txt_product(' ')
                    else:
                        if event.unicode.isalnum() or event.unicode in '@.':
                            input_txt_product(event.unicode)
                elif active == 4:
                    if event.key == pg.K_BACKSPACE:
                        input_txt_employee(-1)
                    elif event.key == pg.K_SPACE:
                        input_txt_employee(' ')
                    else:
                        if event.unicode.isalnum() or event.unicode in '@.':
                            input_txt_employee(event.unicode)
                elif active == 5:
                    if event.key == pg.K_BACKSPACE:
                        input_txt_accounting(-1)
                    elif event.key == pg.K_SPACE:
                        input_txt_accounting(' ')
                    else:
                        if event.unicode.isalnum() or event.unicode in '@.':
                            input_txt_accounting(event.unicode)
            
        pg.display.update()
    pg.quit()

def admin_init():
    pg.init()
    WIDTH, HEIGHT = 1920, 1080
    window = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
    pg.display.set_caption('Administration')
    main(window)