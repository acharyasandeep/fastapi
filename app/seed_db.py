import psycopg2

from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
    password='postgres', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connection Successful")
except Exception as error:
    print("Connection failed")
    print("Error: ", error)
    exit()
    

print("Seeding Database...")

create_table_posts = """ CREATE TABLE IF NOT EXISTS posts (
    id serial PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN DEFAULT True,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
); """

insert_table_posts = """ INSERT INTO posts(title, content) 
VALUES
    ('Midlife Crisis', 'Actually I have been facing midlife crisis and I am not into my mid age yet. Paradoxical ain''t it?'),
    ('Existential Crisis', 'A threat to exist.') """

insert_table_users = """ INSERT INTO users(email, password) 
VALUES
    ('sandeep@gmail.com', '12345'),
    ('emily@gmail.com', 'iloveyou') """

# cursor.execute(create_table_posts)
# cursor.execute(insert_table_posts)
cursor.execute(insert_table_users)

conn.commit()

print("Seeding Successful")