class CompileInfo:
    def __init__(self, name):
        self.name = name
        self.locations = []

    def add_target(self, location: int):
        self.locations.append(location)
