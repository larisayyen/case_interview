
import sqlite3

conn = sqlite3.connect('../raw_data/sql/movies.sqlite')
db = conn.cursor()

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """
        SELECT m.title,m.genres ,d.name
        from movies m
        join directors d on d.id = m.director_id
    """
    return db.execute(query).fetchall()

def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """
        SELECT m.title
        from movies m
        join directors d on d.id = m.director_id
        where m.start_year > d.death_year
        order by m.title
    """
    db.execute(query)
    res = db.fetchall()

    return [i[0] for i in res]

def stats_on(db,genre):
    '''return a dict of stats for a given genre'''
    query = """
        SELECT m.genres, count(m.title), round(avg(m.minutes),2)
        from movies m
        where m.genres like ?
    """

    db.execute(query,(genre,))
    res = db.fetchone()

    return {'genre':res[0],'number_of_movies':res[1],'avg_length':res[2]}

def top_five_directors(db,genre):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = """
        SELECT directors.name, COUNT(movies.title) AS movie_num
        FROM movies
        JOIN directors ON directors.id = movies.director_id
        WHERE movies.genres LIKE ?
        GROUP BY directors.name
        ORDER BY movie_num DESC,directors.name
        LIMIT 5
    """

    db.execute(query,(genre,))
    res = db.fetchall()

    return res

def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    query = """
        select
            (m.minutes / 30 +1) * 30 time_range,
            count(*)
        from movie m
        where m.minutes is not null
        group by time_range
    """
    return db.execute(query).fetchall()

def top_five_youngest_new_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = """
        SELECT
            directors.name,
	        movies.start_year-directors.birth_year age
        FROM movies
        JOIN directors ON directors.id =movies.director_id
        GROUP BY directors.name
        HAVING age IS NOT NULL
        ORDER BY age
        LIMIT 5
    """
    return db.execute(query).fetchall()
