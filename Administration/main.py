from admin_login import login_init
from administration import admin_init

def main():
    if login_init():
        admin_init()
    
if __name__ == '__main__':
    main()