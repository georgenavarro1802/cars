# Model for objects Cars that it will be use in the app (bonus points)


class Car:

    def __init__(self, year, make, model):
        assert year > 0, "Car's Year must be greater than zero"
        assert make != "", "Car's Make cannot be empty"
        assert model != "", "Car's Model cannot be empty"
        self.year = year
        self.make = make
        self.model = model

    def has_all_elements(self):
        return self.year > 0 and self.make != "" and self.model != ""

    def get_obj(self):
        return self.year, self.make, self.model
