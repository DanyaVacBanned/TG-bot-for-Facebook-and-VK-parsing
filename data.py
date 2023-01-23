def get_words(name):

    with open(f"Keywords dir/{name}.txt" , 'r', encoding='utf-8') as file:
        words = [row.strip() for row in file]
        
        return words

def get_kv_words():
    with open('keywords_.txt','r',encoding='utf-8') as file:
        words = [row.strip() for row in file]
        return words


