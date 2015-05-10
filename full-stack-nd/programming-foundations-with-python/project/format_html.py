""" Place data in templates """

import os

# store template strings in seperate files for easier editing

f = open(os.path.join('templates', 'main_page.html'))
main_page_template = f.read()
f.close()

f = open(os.path.join('templates', 'movie_tile.html'))
movie_tile_template = f.read()
f.close()

f = open(os.path.join('templates', 'star.html'))
star_html = f.read()
f.close()

def format_movie_tiles(movies):
    """ return a single string containing divs for all movies """
    return '\n'.join([
        movie_tile_template.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_img_url,
            trailer_youtube_id=movie.youtube_id,
            stars = ''.join(
                [star_html for _ in range(movie.rating)]
            )
        ) for movie in movies])

def write_movies_page(movies, filename='index.html'):
    """ write out html file and return path to file """
    f = open(filename, 'w')
    f.write(
        main_page_template.format(
            movie_tiles=format_movie_tiles(movies)
        )
    )
    f.close()
    return os.path.abspath(f.name)
