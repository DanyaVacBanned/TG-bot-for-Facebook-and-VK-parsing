def get_words():

    with open("keywords_.txt" , 'r', encoding='utf-8') as file:
        words = [row.strip() for row in file]
        
        return words




