import webbrowser

class Movie(object):
    """ Store info about a movie """

    VALID_RATINGS = ['G', 'PG', 'PG-13', 'R']

    def __init__(self, title, storyline, image, trailer):
        self.title = title
        self.storyline = storyline
        self.image = image
        self.trailer = trailer

    def show_trailer(self):
        webbrowser.open(self.trailer)
