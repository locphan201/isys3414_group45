import pygame as pg
from theme import *
from db_connector import check_login

def setup_txt_boxes(category_list, w, h):
    txt_boxes = [-1]
    for i in range(len(category_list)):
        txt_boxes.append([category_list[i], pg.Rect((w-175)/2, 180+(35+30)*i, 175, 35), ''])
    return txt_boxes

def draw_input_boxes(window, boxes):
    txt_size = 18
    h_font = pg.font.SysFont('Arial', txt_size)
    c_font = pg.font.SysFont('Arial', txt_size)
    
    for i in range(1, len(boxes)):
        window.blit(c_font.render(boxes[i][0], True, (0, 0, 0)), (boxes[i][1].x+5, boxes[i][1].y-txt_size))
        pg.draw.rect(window, (255, 255, 255), boxes[i][1])
        if i - 1 == boxes[0]:
            pg.draw.rect(window, (200, 0, 0), boxes[i][1], 2)
        else:
            pg.draw.rect(window, (0, 0, 0), boxes[i][1], 2)

        if boxes[i][0] == 'Password':
            text_surface = h_font.render('*'*len(boxes[i][2]), True, (0, 0, 0))
        else:
            text_surface = h_font.render(boxes[i][2], True, (0, 0, 0))
        window.blit(text_surface, (boxes[i][1].x+5, boxes[i][1].y+7))

def background(window):
    window.fill(BACKGROUND)

def draw_login_button(window, rect):
    font = pg.font.SysFont('Arial', 18)
    pg.draw.rect(window, GREY, rect)
    pg.draw.rect(window, (0, 0, 0), rect, 4)
    text_surface = font.render('Login', True, (0, 0, 0))
    window.blit(text_surface, (rect.x+5, rect.y+7))

def check_password(account, password):
    return check_login(account, password)

def show_error(error, window):
    if error:
        font = pg.font.SysFont('Arial', 18)
        txt = font.render('The password you entered is incorrect', True, (200, 0, 0))
        window.blit(txt, (95, 310))

def draw_header(window, w):
    pg.draw.rect(window, PINK, (0, 0, w, 100))
    h_font = pg.font.Font(font1,50)
    header = h_font.render("Nana's Bakery", True, BLACK)
    size = header.get_rect()
    window.blit(header, ((w-size[2])/2, (100-size[3])/2))

def login_main(window):
    running = True
    clock = pg.time.Clock()
    fps = 60
    isError = False
    isConnected = False
    surface = pg.display.get_surface()
    w, h = surface.get_width(), surface.get_height()
    login_button = pg.Rect((w-50)/2, 350, 50, 35)
    txt_boxes = setup_txt_boxes(['Employee ID', 'Password'], w, h)
    
    while running:
        clock.tick(fps)
        
        background(window)
        draw_header(window, w)
        draw_input_boxes(window, txt_boxes)
        draw_login_button(window, login_button)
        show_error(isError, window)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(1, len(txt_boxes)):
                    if txt_boxes[i][1].collidepoint(pg.mouse.get_pos()):
                        txt_boxes[0] = i-1
         
                if login_button.collidepoint(pg.mouse.get_pos()):
                    if check_password(txt_boxes[1][2], txt_boxes[2][2]):
                        running = False
                        isConnected = True
                        break
                    else:
                        isError = True
                        txt_boxes[2][2] = ''
                    
            if event.type == pg.KEYDOWN:
                current = txt_boxes[0]
                if current != -1:
                    if event.key == pg.K_RETURN:
                        txt_boxes[current+1][2] = ''
                    elif event.key == pg.K_BACKSPACE:
                        txt_boxes[current+1][2] = txt_boxes[current+1][2][:-1]
                    elif event.key == pg.K_TAB:
                        if current < len(txt_boxes)-1:
                            txt_boxes[0] += 1
                    elif event.key == pg.K_KP_ENTER:
                        if check_password(txt_boxes[1][2], txt_boxes[2][2]):
                            running = False
                            isConnected = True
                            break
                        else:
                            isError = True
                            txt_boxes[2][2] = ''
                    else:
                        if len(txt_boxes[current+1][2]) <= 20:
                            txt_boxes[current+1][2] += event.unicode
                                  
        pg.display.update()    
    pg.quit()
    return isConnected

def login_init():
    pg.init()
    WIDTH, HEIGHT = 432, 432
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Administration')
    return login_main(window)