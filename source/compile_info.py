
class CompileInfo:
    def __init__(self, name, word_list, location=None):
        self.name = name
        self.word_list = word_list
        self.locations = []
        if location:
            self.locations.append(location)

    def add_target(self, location: int):
        self.locations.append(location)

    def add_current_location(self, expected_name):
        assert self.name == expected_name, f'expected {expected_name}, found {self.name}'
        self.add_target(len(self.word_list))


    def patch(self, name):
        assert self.name == name, f'expected {name}, found {self.name}'
        if not self.locations:
            print(f'{self.name} has no locations')
        for location in self.locations:
            self.word_list[location] = len(self.word_list)

