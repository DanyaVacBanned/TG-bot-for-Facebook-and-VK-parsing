from database import Database

db = Database('fb_db.db')
db.reset_post_content_data('keywords_kv')
print(db.make_array_from_post_content_data('keywords_kv'))