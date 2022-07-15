
import sqlite3

conn = sqlite3.connect("data/blog.sqlite")
db = conn.cursor()

# pd.read_sql_query(query, conn)

def most_liked_post(db):
    query = """
        SELECT l.post_id ,p.title,COUNT(*) AS like_count
        FROM likes l
        JOIN posts p ON p.id=l.post_id
        GROUP BY l.post_id
        ORDER BY like_count DESC
        LIMIT 3
    """
    return db.execute(query).fetchall()

def three_user_liked_most(db):
    query = """
        SELECT
            l.user_id ,
            u.first_name|| " " ||u.last_name full_name,
            COUNT(*) AS like_count
        FROM likes l
        JOIN users u ON u.id = l.user_id
        GROUP BY l.user_id
        ORDER BY like_count DESC
        LIMIT 3
    """
    return db.execute(query).fetchall()

def most_liked_author(db):
    query = """
        SELECT
            p.user_id ,
            u.first_name|| " " ||u.last_name author_full_name,
            COUNT(l.post_id) AS like_count
        FROM likes l
        JOIN posts p ON p.id = l.post_id
        JOIN users u ON u.id = l.user_id
        GROUP BY p.user_id
        ORDER BY like_count DESC
        LIMIT 1
    """
    return db.execute(query).fetchall()

def author_of_three_most_liked_posts(db):
    query = """
        SELECT
            u.first_name|| " " ||u.last_name author_full_name,
            l.post_id,
            COUNT(l.post_id) AS like_count
        FROM likes l
        JOIN posts p ON p.id = l.post_id
        JOIN users u ON u.id = l.user_id
        GROUP BY l.post_id
        ORDER BY like_count DESC
        LIMIT 3
    """
    return db.execute(query).fetchall()

def number_of_people_liked_at_least_one(db):
    query = """
        SELECT COUNT(DISTINCT user_id) AS liker_count
        FROM likes
    """
    return db.execute(query).fetchone()[0]

def cumulative_number_of_likes_per_day(db):
    query = """
        SELECT
            l.created_at,
            SUM(COUNT(*)) OVER(
                ORDER BY l.created_at
            ) AS cum_sum
        FROM likes l
        GROUP BY l.created_at
    """
    return db.execute(query).fetchall()

def biggest_fan_of_each_author(db):
    query = """
        WITH liker_per_author AS(
            SELECT
                p.user_id author_id,
                l.user_id liker_id,
                COUNT(*) like_count
            FROM likes l
            JOIN posts p ON p.id = l.post_id
            GROUP BY author_id , liker_id
            ORDER BY author_id , liker_id DESC
        )
        SELECT
            authors.first_name || " " || authors.last_name author_full_name,
            likers.first_name  || " " || likers.last_name biggest_full_name,
            like_count
        FROM liker_per_author
        JOIN users authors ON liker_per_author.author_id = authors.id
        JOIN users likers ON liker_per_author.liker_id = likers.id
        GROUP BY authors.id
        ORDER BY author_full_name
    """
    return db.execute(query).fetchall()
