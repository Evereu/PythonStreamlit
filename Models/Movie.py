

class Movie:
    def __init__(self, title,price, year):
        self.title = title
        self.year = year
        self.price = price

    def __str__(self):
        return f"{self.title},{self.price},{self.year}"