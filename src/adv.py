import textwrap

from room import Room
from player import Player
from item import Item
from item import Container
from character import Character

# Declare all the rooms

room = {
    'beach':  Room("Somerton Beach",
    "You see a flurry of activity. There is a a dead man on this beach with you. I guess that's why you're here: to investigate. North of you, you spot a police station.", "You're back on the beach. The body has not yet been removed, and there is nowhere to go except the police station to the north"),

    'police':    Room("Police Station", """Dimly lit by the fading light from the beach. There are several police officers milling around and filling out paperwork. One has a file on his desk marked 'John Doe.' There are three exits - to the train station to the west, the library to the north, and into the neighborhood to the east.""", """The police station is still full of activity, with several officers around. You see a phonebook on a desk."""),

    'station': Room("Train Station", """The high, curved ceiling of the expansive station almost makes you feel dizzy. There is a ticket counter to the north, a bank of lockers to the west, and baths to the south.""", """The high, curved ceiling of the expansive station almost makes you feel dizzy. There is a ticket counter to the north, a bank of lockers to the west, and baths to the south."""),

    'lockers': Room("Bank of Lockers", """There are rows and rows of lockers here, but there's one in the corner that has dust on the lock.""", """There are no other lockers of interest."""),

    'tickets': Room("Ticket Counter", """There is a friendly looking lady behind the counter.""", """The ticket lady has nothing more to offer you."""),

    'baths': Room("Station Baths", """There's nothing much to see here. Just a train station bathroom. It's pretty nice, though.""", """Still just a train station bathroom."""),

    'library': Room("City Library", """Stacks of books line the walls. There is a librarian's office to the north. There are no exits except the way you came in.""", """Stacks of books line the walls. There is a librarian's office to the north. There are no exits except the way you came in."""),

    'librarian': Room("Librarian\'s Office", """The librarian seems nice. She asks what she can do to help you.""", """The librarian has nothing else to tell you about the book."""),

    'neighborhood': Room("Neighborhood", """It's just a neighboorhood. Is this really a good time for a stroll? You should probably head back""", """The address you wrote down should be just down the road"""),

    'jestyn':   Room("JEstyn's House", """You walk through the neighborhood. Just 400 meters from the beach, you find the house you are looking for. In the living room, you see a bookshelf to the north, and the family rooms to the east and west.""", """JEstyn has already told you everything she wants to. Which is, of course, nothing."""),

    'secret': Room("Secret Room", """Good instincts! The bookcase was a false door to a secret room. Unfortunately, she must have known you were coming. The room is empty. The only way out is back the way you came.""", """Did you think something would magically appear in this room?"""),
}

item = {
    'ticket': Item("Unused Rail Ticket", "An unused secont-class rail ticket from Adelaide to Henley Beach"),

    'paper': Item("Piece of Paper", "The piece of paper only has the words 'Tamam shud' on it. Huh. What is that? Persian?"),

    'label': Item("Clothing Label", "Most of the labels have been removed from the clothing, but there are a couple left. This one says 'T. Keane'."),

    'report': Item("Coroner's Report", "The coroner didn't find much, but it looks like they suspect poison. Digitalis, actually."),

    'address': Item("Address Matching Number", "The page of the phonebook containing the address that matches the number from the the book"),

    'book': Item("The Rubaiyat of Omar Khayyam", "A translated selection of Persian quatrains. The back cover contains indentations that look like a couple of phone numbers and some kind of code."),

    'schedule': Item("Train Schedule", "A schedule of all of the trains that could have brought the mystery man to this neck of the woods"),

    'statement': Item("Jessica's Statement", "Even though she wasn't much help, you decided to write down everything Jessica said.")
}

container = {
    'suitcase': Container("Brown Suitcase", "A brown suitcase checked into the station cloakroom on 30 November. The label has been removed."),

    'body': Container("Somerset Man", "all of the labels have been removed from his clothing. There is an unlit cigarette on his collar and it looks like there might be something in his pockets."),

    'phonebook': Container("Phonebook", "a local phonebook"),

    'file': Container("Police Report", "A file containing everything the police currently know about the Somerset Man"),
}

character = {
    'librarian': Character("Librarian", "A small, but intimidating woman. She's definitely smarter than you are.", "I'm not sure I can help you", "I don't think I have anything more I can help you with", "I recognize that! It's the last page of The Rubaiyat of Omar Khayyam. I know we have a copy around... hmmmm. The last page is missing from this. That's probably important. Here!"),

    'jessica': Character("Jessica", "A delicate woman", "I don't want to talk to you.", "I've said all that I'm going to say to you.", "Oh. Oh goodness. Is he... dead? No, no I don't know him. I've never seen him before in my life."),

    'agent': Character("Ticket Agent", "A small, bookish-looking man in his late twenties", "I don't really know anything.", "I don't think I can help you further", "Oh, an unused rail ticket? Well, in that case I can narrow down a time frame and find you a schedule of trains he may have come in on. Here!")
}

character['agent'].item = [item['schedule']]
character['librarian'].item = [item['book']]
character['jessica'].item = [item['statement']]

container['body'].contents = [item['ticket'], item['paper']]
container['suitcase'].contents = [item['label']]
container['phonebook'].contents = [item['address']]
container['file'].contents = [item['report']]

room['beach'].items = [container['body']]
room['lockers'].items = [container['suitcase']]
room['police'].items = [container['file'], container['phonebook']]

room['librarian'].characters = [character['librarian']]
room['tickets'].characters = [character['agent']]
room['jestyn'].characters = [character['jessica']]

# Link rooms together

room['beach'].n_to = room['police']
room['police'].s_to = room['beach']
room['police'].w_to = room['station']
room['police'].n_to = room['library']
room['police'].e_to = room['neighborhood']
room['station'].e_to = room['police']
room['station'].n_to = room['tickets']
room['station'].w_to = room['lockers']
room['station'].s_to = room['baths']
room['baths'].n_to = room['station']
room['lockers'].e_to = room['station']
room['tickets'].s_to = room['station']
room['library'].s_to = room['police']
room['library'].n_to = room['librarian']
room['librarian'].s_to = room['library']
room['neighborhood'].w_to = room['police']
room['neighborhood'].e_to = room['jestyn']
room['jestyn'].w_to = room['neighborhood']
room['jestyn'].n_to = room['secret']
room['secret'].s_to = room['jestyn']


#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player('Detective', room['beach'])

# Write a loop that:
#
# * Prints the current room name

# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
# welcome message
title = ("\n   Welcome, Student!\n")
# start intro text
intro_text = "   As is your custom, you are sitting on your couch re-watching the day's lecture on training kit. It's getting late, and you're finding it hard to stay focused. It\'s not long before your fingers fall away from the keyboard and your eyes fall closed...\n"
# after acceptance intro text
intro_cont = "   When you awake, you are no longer curled into your favorite study nook. You are on a beach. Even stranger, you're wearing a ...suit? You fumble around in your pockets and find a wallet. It has a police badge in it. You are apparently a detective. In Australia. Honestly, that's not even the weird part. You can't believe your eyes when you see the date on your identification: 1948.\n"


move = ('n', 's', 'e', 'w')
take_item_actions = ('get', 'take', 'pickup')
drop_item_actions = ('drop', 'leave', 'putdown')
use_item_actions = ('use', 'show')
inspect_item_actions = ('examine', 'look')
inspect_container_actions = ('inspect', 'open')
character_actions = ('speak', 'ask', 'talk')


def start_game():
    print(chr(27) + "[2J")
    print(title)
    print(textwrap.fill(intro_text, width=60))
    print('\n')
    input('Press enter to continue')


def intro_game():
    print(chr(27) + "[2J")
    print(textwrap.fill(intro_cont, width=60))
    print('\n')
    input('Press enter to accept your new position')


def movement_disallowed():
    print(chr(27) + '[2J')
    print('You begin in that direction, but realize there is nothing over there.')
    print('\n')


def move_player(action):
    # move north
    if action == 'n':
        if hasattr(player.current_room, 'n_to'):
            player.current_room = player.current_room.n_to
        else:
            movement_disallowed()
    # move south
    elif action == 's':
        if hasattr(player.current_room, 's_to'):
            player.current_room = player.current_room.s_to
        else:
            movement_disallowed()
    # move east
    elif action == 'e':
        if hasattr(player.current_room, 'e_to'):
            player.current_room = player.current_room.e_to
        else:
            movement_disallowed()
    # move west
    elif action == 'w':
        if hasattr(player.current_room, 'w_to'):
            player.current_room = player.current_room.w_to
        else:
            movement_disallowed()
    else:
        movement_disallowed()




start_game()
intro_game()


while True:
    inspecting = player.inspecting
    speaking = player.speaking_to
    using = player.using_item

    print(f'Where you are: {player.current_room.name} \n')

    print(textwrap.fill(f'{player.current_room.description} \n', width=60))
    player_move = input(f'What\'s your move, {player.name}?')
    player_move = player_move.lower().split(" ", 1)

    action = player_move[0]
    if len(player_move) == 1:
        target = ""
    else:
        target = player_move[1]

    if action in ['q', 'quit']:
        break

    if action in ['h', 'help']:
        print(chr(27) + "[2J")
        print('probably gonna need instructions because this got weird.')
        print('\n')
        input('Press enter to return to your game.')
    # player moves
    if action in move:
        move_player(action)
