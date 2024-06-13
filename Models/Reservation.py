
class Reservation:
    def __init__(self, user, movie, date_from, date_to, cost):
        self.user = user
        self.movie = movie
        self.date_from = date_from
        self.date_to = date_to
        self.cost = cost

    def __str__(self):
        return f"{self.user},{self.movie},{self.date_from},{self.date_to},{self.cost}"
