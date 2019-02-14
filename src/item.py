# Item class


class Container:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.contents = []

    def on_open(self, player):
        player.inspecting_container = [self]
        print(f'Inspecting the {self.name}, you find')
        if len(self.contents) > 0:
            for item in self.contents:
                print(item.name)
        else:
            print('nothing more of interest')

    def __repr__(self):
        return f'Name:{self.name}, description: {self.description}'


class Item:
    def __init__(self, name, description, takable=True, useable=True):
        self.name = name
        self.description = description
        self.take_message = 'You place the ' + name + ' in your briefcase'
        self.use_message = 'You hold out the ' + name
        self.takable = takable
        self.useable = useable

    def on_take_room(self, player):
        print(f'\n{self.take_message}')
        player.items.append(self)
        player.current_room.items.remove(self)

    def on_take_container(self, player, container):
        print(f'\n{self.take_message}')
        player.items.append(self)
        container.contents.remove(self)

    def on_drop(self, player):
        print(f'\nYou drop the {self.name}')
        player.current_room.items.append(self)
        player.items.remove(self)

    def inspect(self, player):
        player.inspecting_item = [self]
        print(f'\nYou approach the {self.name} to try to get a better look.')
        print(f'It\'s {self.description}')

    def on_use(self, player):
        player.using_item = [self]
        print(f'\n{self.use_message}')

    def __repr__(self):
        return f'Name: {self.name}, Description: {self.description}'


class Trinket(Item):
    def __init__(self, color, shape, description):
        super().__init__("trinket", color, shape, description)
        self.color = color
        self.shape = shape
        self.name = color + description
