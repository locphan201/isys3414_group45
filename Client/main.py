from login import *
from customer import *
from db_connector import *

def main():
    isConnected, info = login_init()
    if isConnected:
        customer_init(info)
    
if __name__ == '__main__':
    main()