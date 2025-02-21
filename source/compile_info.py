
class CompileInfo:
    def __init__(self, name, word_list, location=None):
        self.name = name
        self.word_list = word_list
        self.locations = []
        if location:
            self.locations.append(location)

    def __repr__(self):
        return f'CI({self.name}): {self.locations}'

    def add_target(self, location: int):
        self.locations.append(location)

    def add_current_location(self, expected_name):
        assert self.name == expected_name, f'expected {expected_name}, found {self.name}'
        self.add_target(len(self.word_list))

    def add_locations_from(self, another_info):
        for loc in another_info.locations:
            self.add_target(loc)


    def patch(self, name):
        assert self.name == name, f'expected {name}, found {self.name}'
        if not self.locations:
            print(f'{self.name} has no locations')
        for location in self.locations:
            self.word_list[location] = len(self.word_list)

