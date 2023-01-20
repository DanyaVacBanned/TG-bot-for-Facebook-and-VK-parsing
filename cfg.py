def get_token():
    with open('token.txt', 'r', encoding='utf-8') as f:
        return f.read()

def get_admin_id():
    with open('admin_id.txt','r', encoding='utf-8') as f:
        admin_id = f.read().strip()
        return str(admin_id)

def get_chat_id():
    with open('chat_id.txt', 'r', encoding='utf-8') as f:
        chat_id = f.read().strip().split()
        return chat_id

def tmp(cn):
    with open('tmp.txt', 'w', encoding='utf-8') as f:
        f.write(cn)


def tmp_get():
    with open('tmp.txt','r',encoding='utf-8') as f:
        return f.read().strip()

def get_channel_id():
    with open('channel_id.txt','r',encoding='utf-8') as f:
        return f.read().strip()
        
    
