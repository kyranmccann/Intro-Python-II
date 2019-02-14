# Write a class to hold player information, e.g. what room they are in
# currently.


class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        self.inspecting_container = []
        self.inspecting_item = []
        self.speaking_to = []
        self.using_item = []
        self.items = []

    def __repr__(self):
        return f'{self.name} is currently in  {self.current_room.name}'
