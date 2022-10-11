import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    
    def add_groups(self, group_id, groups_list, country_id):
        with self.connection:
            return self.cursor.execute('insert into `groups` (`group_id`, `groups_list`, `country_id`) values (?,?,?)',(group_id, groups_list, country_id,))
    
    def select_groups_list(self, country_id):
        with self.connection:
            return self.cursor.execute('select `groups_list`, `group_id` from `groups` where `country_id`=?', (country_id,))