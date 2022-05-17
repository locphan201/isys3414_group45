import pygame as pg
from theme import *
from db_connector import *

def setup_boxes(category_list, y):
    boxes = [-1]
    for i in range(len(category_list)):
        boxes.append([category_list[i], pg.Rect(138, y+120+65*i, 175, 35), ''])
    return boxes

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

        if boxes[i][0] == 'Password' or boxes[i][0] == 'Confirm Password':
            text_surface = h_font.render('*'*len(boxes[i][2]), True, (0, 0, 0))
        else:
            text_surface = h_font.render(boxes[i][2], True, (0, 0, 0))
        window.blit(text_surface, (boxes[i][1].x+5, boxes[i][1].y+7))

def background(window):
    img = pg.image.load('Resources\\Images\\Login\\background.jpg')
    img = pg.transform.scale(img, (432, 768))
    window.blit(img, (0, 0))

def draw_login_button(window, rect):
    font = pg.font.SysFont('Arial', 18)
    pg.draw.rect(window, GREY, rect)
    pg.draw.rect(window, (0, 0, 0), rect, 4)
    text_surface = font.render('Login', True, (0, 0, 0))
    window.blit(text_surface, (rect.x+15, rect.y+7))

def check_password(info):
    return check_login(info[1][2], info[2][2])

def show_msg(window, y, msg):
    font = pg.font.SysFont('Arial', 18)
    txt = font.render(msg, True, (200, 0, 0))
    rect = txt.get_rect()
    window.blit(txt, (226-rect.w/2, 230+y))

def draw_signup_button(window, rect):
    pg.draw.line(window, BLACK, (rect.x, rect.y), (rect.x+rect.w, rect.y), 2)
    font = pg.font.SysFont('Arial', 18)
    pg.draw.rect(window, GREY, rect)
    pg.draw.rect(window, (0, 0, 0), rect, 4)
    text_surface = font.render('Sign Up', True, (0, 0, 0))
    window.blit(text_surface, (rect.x+8, rect.y+7))

def draw_login(window, y, inputs, log, sign):
    background(window)
    h_font = pg.font.Font(font1, 50)
    header = h_font.render("Nana's Bakery", True, BLACK)
    rect = header.get_rect()
    pg.draw.rect(window, WHITE, (95, y+10, rect.w+10, 310))
    pg.draw.rect(window, PINK, (95, y+10, rect.w+10, 50))
    window.blit(header, (100, y+10))
    draw_input_boxes(window, inputs)
    draw_login_button(window, log)
    draw_signup_button(window, sign)

def draw_signup(window, y, inputs, log, sign):
    background(window)
    h_font = pg.font.Font(font1, 50)
    header = h_font.render("Nana's Bakery", True, BLACK)
    rect = header.get_rect()
    pg.draw.rect(window, WHITE, (95, y+10, rect.w+10, 540))
    pg.draw.rect(window, PINK, (95, y+10, rect.w+10, 50))
    window.blit(header, (100, y+10))
    draw_input_boxes(window, inputs)
    draw_login_button(window, log)
    draw_signup_button(window, sign)

def check_signup(info):
    inf = []
    for i in range(1, len(info)):
        inf.append(info[i][2])
    return check_signup_db(inf)

def clear_text(boxes):
    for i in range(1, len(boxes)):
        boxes[i][2] = ''

def login_main(window):
    running = True
    clock = pg.time.Clock()
    fps = 60
    active = 0
    lg_y, sg_y = 229, 104
    login_boxes = setup_boxes(['Phone or Email', 'Password'], lg_y)
    signup_boxes = setup_boxes(['Name', 'Phone', 'Address', 'Email', 'Password', 'Confirm Password'], sg_y-25)
    login_button = [pg.Rect(150, 255+lg_y, 70, 35), pg.Rect(150, 495+sg_y, 70, 35)]
    signup_button = [pg.Rect(232, 255+lg_y, 70, 35), pg.Rect(232, 495+sg_y, 70, 35)]
    msg = ''
    isConnected = False
    
    while running:
        clock.tick(fps)
        
        if active == 0:
            draw_login(window, lg_y, login_boxes, login_button[0], signup_button[0])
            show_msg(window, lg_y, msg)
        else:
            draw_signup(window, sg_y, signup_boxes, login_button[1], signup_button[1])
            show_msg(window, sg_y+230, msg)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if active == 0:
                    for i in range(1, len(login_boxes)):
                        if login_boxes[i][1].collidepoint(pg.mouse.get_pos()):
                            login_boxes[0] = i-1
                else:
                    for i in range(1, len(signup_boxes)):
                        if signup_boxes[i][1].collidepoint(pg.mouse.get_pos()):
                            signup_boxes[0] = i-1
                            
                if login_button[active].collidepoint(pg.mouse.get_pos()):
                    if active != 0:
                        msg = ''
                        active = 0
                        clear_text(signup_boxes)
                    elif check_password(login_boxes):
                        running = False
                        isConnected = True
                        break
                    else:
                        msg = 'Invalid Account or Password'
                        login_boxes[2][2] = ''
                        
                if signup_button[active].collidepoint(pg.mouse.get_pos()):
                    if active != 1:
                        msg = ''
                        active = 1
                        clear_text(login_boxes)
                    elif check_signup(signup_boxes):
                        active = 0
                        msg = ''
                        login_boxes[1][2] = signup_boxes[2][2]
                        clear_text(signup_boxes)
                    else:
                        msg = 'Invalid Infomation'
                        signup_boxes[4][2] = ''
                        signup_boxes[5][2] = ''
                    
            if event.type == pg.KEYDOWN:
                if active == 0:
                    current = login_boxes[0]
                    if current != -1:
                        if event.key == pg.K_RETURN:
                            login_boxes[current+1][2] = ''
                        elif event.key == pg.K_BACKSPACE:
                            login_boxes[current+1][2] = login_boxes[current+1][2][:-1]
                        elif event.key == pg.K_TAB:
                            if current < len(login_boxes)-1:
                                login_boxes[0] += 1
                        elif event.key == pg.K_KP_ENTER:
                            if check_password(login_boxes):
                                running = False
                                isConnected = True
                                break
                            else:
                                msg = 'Invalid Account or Password'
                                login_boxes[2][2] = ''
                        else:
                            if len(login_boxes[current+1][2]) <= 20:
                                login_boxes[current+1][2] += event.unicode
                else:
                    current = signup_boxes[0]
                    if current != -1:
                        if event.key == pg.K_RETURN:
                            signup_boxes[current+1][2] = ''
                        elif event.key == pg.K_BACKSPACE:
                            signup_boxes[current+1][2] = signup_boxes[current+1][2][:-1]
                        elif event.key == pg.K_TAB:
                            if current < len(signup_boxes)-1:
                                signup_boxes[0] += 1
                        elif event.key == pg.K_KP_ENTER:
                            if check_signup(signup_boxes):
                                active = 0
                                login_boxes[1][2] = signup_boxes[2][2]
                                clear_text(signup_boxes)
                            else:
                                msg = 'Invalid Account or Password'
                                signup_boxes[4][2] = ''
                                signup_boxes[5][2] = ''
                        else:
                            if len(signup_boxes[current+1][2]) <= 20:
                                signup_boxes[current+1][2] += event.unicode                  
                
        pg.display.update()    
    pg.quit()
    
    return isConnected, login_boxes[1][2]

def login_init():
    pg.init()
    WIDTH, HEIGHT = 432, 768
    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Login')
    return login_main(window)