
import sqlite3

conn = sqlite3.connect('../raw_data/sql/jukebox.sqlite')
db = conn.cursor()

def short_tracks(db):

    ''' return the number of tracks that last less than 2 mins'''
    query = """
        SELECT COUNT(t.name)
        FROM tracks t
        WHERE t.milliseconds /60000 <2
    """

    db.execute(query)
    res = db.fetchone()

    return res[0]

def track_keyword(db,keyword):
    query = """
        SELECT t.name,a.title
        FROM tracks t
        JOIN albums a ON a.id = t.album_id
        WHERE UPPER(t.name) LIKE ?
    """

    db.execute(query,(f"%{keyword}%",))
    res = db.fetchall()

    return res

def top_five_artists(db,genre):

    query="""
        SELECT a2.name , COUNT(t.name)
        FROM tracks t
        JOIN albums a ON a.id = t.album_id
        JOIN artists a2 ON a2.id = a.artist_id
        JOIN genres g ON g.id = t.genre_id
        WHERE g.name = ?
        GROUP BY a2.name
        ORDER BY COUNT(t.name) DESC
        LIMIT 5
    """

    return db.execute(query,(genre,)).fetchall()
