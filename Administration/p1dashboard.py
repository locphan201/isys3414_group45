import pygame as pg
from db_connector import *
from theme import *
from datetime import datetime

DAY = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ORDERS, TOP5 = [],  []
MONTHLY_ORDERS = []
AVG = 0

def get_time():  
    now = datetime.now()
    date = []
    date.append(now.strftime('%d'))
    date.append(now.strftime('%m'))
    date.append(now.strftime('%Y'))
    day = DAY[now.weekday()]
    return date, day

def update_orders():
    global ORDERS
    ORDERS = get_all_orders()

def get_avg_spent():
    global AVG
    AVG = get_avg()

def update_top5():
    global TOP5
    TOP5 = get_best_sellers()

def update_monthly_orders():
    global MONTHLY_ORDERS
    MONTHLY_ORDERS = get_monthly_numOrders()
    
def update():
    update_orders()
    get_avg_spent()
    update_top5()
    update_monthly_orders()

DATE, WEEKDAY = get_time()
update()

def show(window, font, text, x, y, color=BLACK, align=-1):
    txt = font.render(text, True, color)
    if align == -1:
        window.blit(txt, (x, y))
    elif align == 0:
        rect = txt.get_rect(center=(x, y))
        window.blit(txt, (rect.x, rect.y))

def draw_date(window):
    global DATE
    
    font = pg.font.Font(font4, 30)
    date = WEEKDAY + ' ' + str(DATE[0]) + ' ' + MONTHS[int(DATE[1]) - 1] + ' ' + str(DATE[2])
    
    window.blit(font.render(date, True, BLACK), (225, 30))
    pg.draw.line(window, BLACK, (225, 75), (455, 75), 2)

def draw_order_status(window):
    global ORDERS
    
    header = pg.font.Font(font1, 40)
    font = pg.font.Font(font4, 25)
    status = ['COMPLETED', 'INCOMPLETED', 'CANCELLED']
    show(window, header, 'Orders', 175, 130, DARK_BLUE, 0)
    pg.draw.line(window, DARK_BLUE, (125, 155), (225, 155), 2)
    
    for i in range(len(ORDERS)):
        pg.draw.rect(window, LIGHT_GREY, (125+250*i, 180, 200, 200))
        pg.draw.rect(window, LIGHT_RED, (125+250*i, 180, 200, 200), 2)
        color = DARK_RED
        if i == 0:
            color = DARK_GREEN
        elif i == 1:
            color = DARK_BLUE
        show(window, font, status[i], 225+250*i, 220, color, 0)
        show(window, font, str(ORDERS[i]), 225+250*i, 300, BLACK, 0)

def draw_avg_spent(window):
    global AVG
    
    header = pg.font.Font(font1, 40)
    font = pg.font.Font(font4, 25)
    
    show(window, header, 'Average Spent per Order', 1200, 130, DARK_BLUE, 0)
    pg.draw.line(window, DARK_BLUE, (1050, 155), (1350, 155), 2)
    
    pg.draw.rect(window, LIGHT_GREEN, (1100, 200, 200, 50))
    pg.draw.circle(window, LIGHT_GREEN, (1100, 225), 25)
    pg.draw.circle(window, LIGHT_GREEN, (1300, 225), 25)
    show(window, font, '$' + str(AVG), 1200, 225, BLACK, 0)

def draw_numOrders_by_month(window):
    global MONTHLY_ORDERS
    header = pg.font.Font(font1, 40)
    font = pg.font.Font(font4, 18)
    BASE = 800
    
    show(window, header, 'Number of Orders by Month', 300, BASE-350, DARK_BLUE, 0)
    pg.draw.line(window, DARK_BLUE, (125, BASE-325), (475, BASE-325), 2)

    BASE = 800

    MAX = max(MONTHLY_ORDERS)
    for i in range(6):
        if i > 0:
            pg.draw.line(window, BLACK, (120, BASE-i*50), (130, BASE-i*50), 2)
        if (MAX/5*i) % 1 == 0:
            show(window, font, str(int(MAX/5*i)), 90, BASE-i*50-10)
        else:
            show(window, font, str(round(MAX/5*i, 2)), 90, BASE-i*50-10)

    for i in range(12):
        show(window, font, str(i+1), 180+i*50, BASE+25, BLACK, 0)
        length = 250 * MONTHLY_ORDERS[i] / MAX
        color = LIGHT_BLUE
        if (i+1) % 2 == 0:
            color = LIGHT_ORANGE
        pg.draw.rect(window, color, (165+i*50, BASE-length, 30, length+1))
        pg.draw.rect(window, BLACK, (165+i*50, BASE-length, 30, length+1), 2)
        if MONTHLY_ORDERS[i] > 0:
           show(window, font, str(MONTHLY_ORDERS[i]), 180+i*50, BASE-length-10, BLACK, 0)
           
    pg.draw.line(window, BLACK, (125, BASE-300), (125, BASE), 2)
    pg.draw.line(window, BLACK, (125, BASE), (800, BASE), 2)

def draw_best_product(window):
    global TOP5
    header = pg.font.Font(font1, 40)
    col = pg.font.Font(font4, 25)
    font = pg.font.Font(font4, 20)
    
    show(window, header, 'Top 5 Products', 1200, 450, DARK_BLUE, 0)
    pg.draw.line(window, DARK_BLUE, (1100, 475), (1300, 475), 2)
    
    pg.draw.rect(window, BLACK, (1000, 500, 400, 300), 2)
    pg.draw.line(window, BLACK, (1000, 550), (1400, 550), 2)
    pg.draw.line(window, BLACK, (1250, 500), (1250, 800), 2)
    show(window, col, 'Product', 1025, 510)
    show(window, col, 'Sold', 1325, 525, BLACK, 0)
    
    for i in range(len(TOP5)):
        show(window, font, TOP5[i][0], 1025, 565+i*50)
        show(window, font, str(TOP5[i][1]), 1325, 575+i*50, BLACK, 0)

def draw_dashboard(window):
    draw_date(window)
    draw_order_status(window)
    draw_avg_spent(window)
    draw_numOrders_by_month(window)
    draw_best_product(window)