# Implement a class to hold room information. This should have name and
# description attributes.
import world


class Room:
    def __init__(self, name, description, return_description):
        self.name = name
        self.description = description
        self.return_description = return_description,
        self.visits = 0
        self.items = []
        self.characters = []

    def inspect(self, player):
        book = world.item.get('book')
        print_items = []
        if self.name == 'Police Station':
            if [book] in player.items:
                print_items = self.items
            else:
                print_items = [self.items[0]]
        else:
            print_items = self.items

        print(f"\nLooking around {self.name}, you see: \n")
        for item in print_items:
            print(item.name + '\n')
        for character in self.characters:
            print(character.name + '\n')

    def __repr__(self):
        return f'Name: {self.name}, description: {self.description}'
