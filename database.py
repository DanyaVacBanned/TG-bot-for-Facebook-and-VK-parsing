import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    
    def add_new_list(self, ID, groups_list):
        with self.connection:
            return self.cursor.execute('insert into groups (`groups_list`,`id`) values (?, ?)', (groups_list,ID,))
        
    def make_array_from_groups_list(self, ID):
        with self.connection:
            data = self.cursor.execute('select `groups_list` from `groups` where `id`=?',(ID,)).fetchall()
            for row in data:
                return row[0].strip().split()

    # def add_new_channel_by_group(self, channel_id, group_id):
    #     with self.connection:
    #         return self.cursor.execute('insert into `channel_ids` (`ID`, `channel_id`) values (?,?)', (group_id, channel_id,))
    
    # def select_channel_id_by_group(self, group_id):
    #     with self.connection:
    #         data = self.cursor.execute('select channel_id from `channel_ids` where `ID` = ?', (group_id,)).fetchall()
    #         for row in data:
    #             return row[0]
            

    def check_groups_db_data(self):
        with self.connection:
            return self.cursor.execute('select * from groups').fetchall()
    
    def check_channel_id_db_data(self):
        with self.connection:
            return self.cursor.execute("select * from channel_ids").fetchall()

    def reset_all_data(self):
        with self.connection:
            self.cursor.execute("DELETE FROM groups")
            self.cursor.execute("DELETE FROM channel_ids")
            self.cursor.execute("DELETE FROM post_content")
#------------------post content-------------------------------------------
    def insert_post_content(self, text, name):
        with self.connection:
            self.cursor.execute(f'INSERT INTO {name} (text) VALUES (?)',(text,))

    def select_post_content(self, name):
        with self.connection:
            return self.cursor.execute(f'SELECT * FROM {name}').fetchall()


    def make_array_from_post_content_data(self, name):
        with self.connection:
            post_content_list = []
            data = self.cursor.execute(f"SELECT * FROM {name}").fetchall()
            for row in data:
                post_content_list.append(row[1])
            if post_content_list == []:
                return ['zero']
            return(post_content_list)
    
    def reset_post_content_data(self, name):
        with self.connection:
            self.cursor.execute(f'DELETE FROM {name}')

    def reset_groups(self, chat_id):
        with self.connection:
            self.cursor.execute(f"DELETE FROM groups WHERE id = ?",(chat_id,))
#--------------------------------------------------------------------------
    def reset_groups_data(self):
        with self.connection:
            self.cursor.execute("DELETE FROM groups")

    
    def create_table(self, name):
        self.cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {name}
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT
        )"""
    )
    
    # def reset_groups_for_picked_channel(self, chatId):
    #     with self.connection:
    #         self.cursor.execute("DELETE FROM groups WHERE id = ?",(chatId,))

    

# db = Database('fb_db.db')


# print(db.make_array_from_post_content_data())
