import pygame as pg
from p1homepage import *
from p2product import *
from p3cart import *
from p4order import *
from p5about_us import *
from db_connector import *
from theme import *

USER_INFO = []
ORDER_UPDATE = False

def user_information(account):
    global USER_INFO
    USER_INFO = get_user_info(account)

def draw_page(window, pages, active, scroll_y, back, nxt):
    global ORDER_UPDATE
    window.fill(BACKGROUND)
    INDENT = 55
    
    if active == 0:
        draw_homepage(window)
    elif active == 1:
        draw_product_page(window, scroll_y)
    elif active == 2:
        draw_cart(window)
    elif active == 3:
        if not ORDER_UPDATE:
            ORDER_UPDATE = True
            get_order(USER_INFO[0])
        draw_order_page(window)
    elif active == 4:
        draw_about_us(window)

    pg.draw.rect(window, LIGHT_RED, (0, 0, 432, 65))
    pg.draw.rect(window, GREY, (0, 65, 432, 35))
    h_font = pg.font.Font(font1,50)
    header = h_font.render('Nana\'s Bakery', True, BLACK)
    window.blit(header, (100,0))
    
    font = pg.font.SysFont('Arial', 20)
    ft = pg.font.SysFont('Arial', 15)
    window.blit(ft.render('ID #' + str(USER_INFO[0]), True, BLACK), (10, 50))
    #Previous page
    if active >= 1:
        txt = font.render(pages[active-1], True, (50, 50, 50))
        back = txt.get_rect(center=(40, 25))
        back = pg.Rect(INDENT, 70, back.w, back.h)
        window.blit(txt, (INDENT, 70))

    #Current page
    txt = font.render(pages[active], True, (0, 0, 0))
    window.blit(txt, (INDENT+125, 70))

    #Next page
    if active < len(pages)-1:
        txt = font.render(pages[active+1], True, (50, 50, 50))
        nxt = txt.get_rect(center=(40, 25))
        nxt = pg.Rect(INDENT+250, 70, nxt.w, nxt.h)
        window.blit(txt, (INDENT+250, 70))

    return back, nxt, scroll_y


def customer_main(window):
    global ORDER_UPDATE
    running = True
    clock = pg.time.Clock()
    fps = 60
    back, nxt = pg.Rect(40, 0, 100, 50), pg.Rect(290, 0, 100, 50)
    pages = ['Homepage', 'Products', 'Cart', 'Order', 'About us']
    active = 0
    scroll_y = 0
    
    while running:
        clock.tick(fps)

        back, nxt, scroll_y = draw_page(window, pages, active, scroll_y, back, nxt)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                disconnect_db()
                break
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if active == 0:
                    if check_event_homepage(event.pos[0], event.pos[1]):
                        active = 1
                
                elif active == 1:
                    if event.button == 1:
                        item = check_hit_product(scroll_y, event.pos[0], event.pos[1])
                        if item != []:    
                            add_item(item[0], item[1])
                    if event.button == 4: scroll_y = min(scroll_y + 15, 0)
                    if event.button == 5: scroll_y = max(scroll_y - 15, -768)
                
                elif active == 2:
                    button, i = check_hit_button(event.pos[0], event.pos[1])
                    if button == -1:
                        update_one(i, -1)
                    elif button == 1:
                        update_one(i, 1)
                    elif button == 2:
                        items = get_items()
                        if items[1] != 0:
                            cart_checkout(items, USER_INFO[0])
                            remove_all()
                            remove_quantities()
                            update_best_sellers()
                            active = 3
                            ORDER_UPDATE = False
                
                elif active == 3:
                    check_order_events(event.pos[0], event.pos[1])
                
                if event.button == 1:
                    if back.collidepoint(event.pos):
                        active = max(active - 1, 0)
                        scroll_y = 0
                    if nxt.collidepoint(event.pos):
                        active = min(active + 1, len(pages)-1)
                        scroll_y = 0
        pg.display.update()   
    pg.quit()

def customer_init(info):
    pg.init()
    user_information(info)
    WIDTH, HEIGHT = 432, 768
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Nana\'s Bakery')
    customer_main(window)