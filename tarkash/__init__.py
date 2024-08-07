__INITLIASED = False

def init():
    global __INITLIASED
    if __INITLIASED: return
    
    from dotenv import load_dotenv, find_dotenv
    _ = load_dotenv(find_dotenv()) # read local .env file
    
    __INITLIASED = True