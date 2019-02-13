import textwrap
import os

from room import Room
from player import Player

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player('Adventurer', room['outside'])

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
clear = lambda: os.system('cls')
clear()

def start_game():
    input('Press Enter to Begin')

def movement_disallowed():
    print(chr(27) + '[2J')
    print('You begin in that direction, but realize there is nothing over there.')

move = ('n', 's', 'e', 'w')


while True:
    print(f'Where you are: {player.current_room.name} \n')
    print(f'{player.current_room.description} \n')
    player_move = input(f'What\'s your move, {player.name}?')
    player_move = player_move.lower()

    if player_move in ['q', 'quit']:
        break
    # player moves
    if player_move in move:
        # move north
        if player_move == 'n':
            if hasattr(player.current_room, 'n_to'):
                player.current_room = player.current_room.n_to
            else:
                movement_disallowed()
        # move south
        elif player_move == 's':
            if hasattr(player.current_room, 's_to'):
                player.current_room = player.current_room.s_to
            else:
                movement_disallowed()
        # move east
        elif player_move == 'e':
            if hasattr(player.current_room, 'e_to'):
                player.current_room = player.current_room.e_to
            else:
                movement_disallowed()
        # move west
        elif player_move == 'w':
            if hasattr(player.current_room, 'w_to'):
                player.current_room = player.current_room.w_to
            else:
                movement_disallowed()
        else:
            movement_disallowed()
