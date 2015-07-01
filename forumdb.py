#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    connection = psycopg2.connect('dbname=forum')
    c = connection.cursor()

    c.execute("""SELECT * FROM posts ORDER BY time DESC """)
    posts = ({'content': str(row[1]), 'time': str(row[0])}
    		  for row in c.fetchall())
    connection.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    content = bleach.clean(content)
    connection = psycopg2.connect('dbname=forum')
    c = connection.cursor()
    c.execute("INSERT INTO posts(content) VALUES (%s)", (content,))
    connection.commit()
    connection.close()
