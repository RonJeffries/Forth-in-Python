
class CompileInfo:
    def __init__(self, name, word_list, location=None):
        self.name = name
        self.word_list = word_list
        self.locations = []
        if location:
            self.locations.append(location)

    def add_target(self, location: int):
        self.locations.append(location)

    def patch(self, name):
        assert self.name == name, f'expected {name}, found {self.name}'
        for location in self.locations:
            self.word_list[location] = len(self.word_list)

