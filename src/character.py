# Implement a class to hold character information for people that might be spoken to.


class Character:
    def __init__(self, name, description, line_one, line_two, required_line):
        self.name = name
        self.description = description
        self.line_one = line_one
        self.line_two = line_two
        self.required_line = required_line
        self.required_read = False
        self.required_item = []
        self.item = []

    def speak(self, player):
        if len(player.using_item) > 0:
            if player.using_item[0] == self.required_item and len(self.item) > 0:
                print(f'\n {self.name}: {self.required_line}')
                self.required_read = True
                player.items.append(self.item)
                print(f'\n{self.name} has nothing more to offer, so you should probably get back to it')
                input('Press enter to continue')
                self.item = []
                player.speaking_to = []
                player.using_item = []

            elif player.using_item[0] != self.required_item:
                print(f'{self.name}: {self.line_one}')
                print('------------------------------------------------------')

        elif len(self.item) == 0:
            print(f'\n{self.name}: {self.line_two}')
            print(f'\n{self.name} has nothing more to offer, so you should probably get back to it')
            input('Press enter to continue')
            player.speaking_to = []
            player.using_item = []

        else:
            print(self.line_one)
            print('------------------------------------------------------')

    def first_line(self):
        print(f'\n {self.line_one}')

    def second_line(self):
        print(f'\n{self.line_two}')

    def required_possessed(self):
        print(f'\n{self.required_line}')
        self.required_read = True

    def give_item(self, player):
        player.items.append(self.item)
        self.item = []

    def __repr__(self):
        return f'Name: {self.name}'
