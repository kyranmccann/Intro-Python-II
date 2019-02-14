import textwrap

from player import Player
import world
import messages
# Make a new player object that is currently in the 'outside' room.
player = Player('Detective', world.room['beach'])

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


move = ('n', 's', 'e', 'w')
take_item_actions = ('get', 'take', 'pickup')
drop_item_actions = ('drop', 'putdown')
use_item_actions = ('use', 'show')
inspect_actions = ('examine', 'look', 'check', 'inspect')
stop_inspect_actions = ('leave', 'continue', 'return')
# inspect_item_actions = ('examine', 'look')
# inspect_container_actions = ('inspect', 'open')
# inspect_room_actions = ('inspect', 'look', 'examine')
character_actions = ('speak', 'ask', 'talk')


def start_game():
    print(chr(27) + "[2J")
    print(messages.title)
    print(textwrap.fill(messages.intro_text, width=60))
    print('\n')
    input('Press enter to continue')


def intro_game():
    print(chr(27) + "[2J")
    print(textwrap.fill(messages.intro_cont, width=60))
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


def talk_to_character(action, target):
    target_character = world.character.get(target)
    print(target_character.name)
    player.speaking_to = target_character
    print(f'{player.speaking_to.name} asks how they can help you')
    player.speaking_to.speak(player)


def inspect_container(action, target):
    if target in world.container:
        target_container = world.container.get(target)
        player.inspecting_container = target_container
        player.inspecting_container.on_open(player)
        print(f"Do you see anything you think might be useful to you?")
    else:
        player.inspecting_container[0].on_open(player)


def inspect_item(action, target):
    target_item = world.item.get(target)
    print(target_item.name)
    player.inspecting_item = target_item
    player.inspecting_item.inspect(player)


def start_inspect(action, target):
    if target in world.container:
        inspect_container(action, target)
    elif target in world.item:
        inspect_item(action, target)


def stop_inspect(action, target):
    if target in world.item:
        print(f'You stop looking at {player.inspecting_item[0].name}')
        player.inspecting_item = []
        inspect_container(action, player.inspecting_container[0].name)
    elif target in world.container:
        print(f'You stop examining the {player.inspecting_container[0].name}')
        player.inspecting_container = []


def take_item(action, target):
    if target in world.item:
        target_item = world.item.get(target)
        item_container = player.inspecting_container[0]
        if target_item in item_container.contents:
            print("yup that's in here.")
            target_item.on_take_container(player, item_container)
            if len(player.inspecting_item) > 0 and player.inspecting_item[0] == target_item:
                player.inspecting_item = []
                # inspect_container(action, player.inspecting_container[0].name)
        else:
            print("I don't see that item here")
    else:
        print("You can't take that.")


def drop_item(action, target):
    if target in world.item:
        print('yes that is an item')
        target_item = world.item.get(target)
        print(target_item)
        print(player.items)
        if target_item in player.items:
            print('yes you have it')
            target_item.on_drop(player)
        else:
            print("You don't seem to have that item")
    else:
        print("That's not something you can drop")


def main_text():
    print(f'Where you are: {player.current_room.name}')
    if len(player.inspecting_item) > 0:
        inspect_item(action, target)
    elif len(player.inspecting_container) > 0:
        inspect_container(action, target)
    elif len(player.speaking_to) > 0:
        talk_to_character(action, target)
    else:
        print(textwrap.fill(f'{player.current_room.description} \n', width=60))


# Actually start the game
start_game()
intro_game()


while True:

    print(f'Where you are: {player.current_room.name} \n')

    main_text()
    player_move =input(f'What\'s your move, {player.name}?')

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

    if action in inspect_actions:
        start_inspect(action, target)

    if action in stop_inspect_actions:
        stop_inspect(action, target)

    if action in take_item_actions:
        take_item(action, target)

    if action in drop_item_actions:
        drop_item(action, target)
    # print(textwrap.fill(f'{player.current_room.description} \n', width=60))
    # player_move = input(f'What\'s your move, {player.name}?')
    # player_move = player_move.lower().split(" ", 1)
    #
    # action = player_move[0]
    # if len(player_move) == 1:
    #     target = ""
    # else:
    #     target = player_move[1]

    # player moves
    if action in move:
        move_player(action)
