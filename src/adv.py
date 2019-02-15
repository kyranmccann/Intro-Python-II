import textwrap

from player import Player
import world
import messages
# Make a new player object that is currently in the 'outside' room.
player = Player('Detective', world.room['beach'])

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


# Print welcome message and intro to story
def start_game():
    print(chr(27) + "[2J")
    print(messages.title)
    print(textwrap.fill(messages.intro_text, width=60))
    print('\n')
    input('Press enter to continue')


# Print rest of story intro
def intro_game():
    print(chr(27) + "[2J")
    print(textwrap.fill(messages.intro_cont, width=60))
    print('\n')
    input('Press enter to accept your new position')


# Error message for moving in a direction with nothing for you
def movement_disallowed():
    print(chr(27) + '[2J')
    print('You begin in that direction, but realize there is nothing over there.')
    print('\n')
    print('------------------------------------------------------')


# Player move between rooms logic
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
            special_room = world.room.get('neighborhood')
            address = world.item.get('address')
            if player.current_room == special_room:
                if address in player.items:
                    player.current_room = player.current_room.e_to
                else:
                    movement_disallowed()
            else:
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


# Speak to a character
def talk_to_character(action, target):
    # check to make sure the target is a character
    if target in world.character:
        target_character = world.character.get(target)
        # check to make sure the character is in the current room
        if target_character in player.current_room.characters:
            player.speaking_to = target_character
            print(f'You ask {player.speaking_to.name} about the case')
            player.speaking_to.speak(player)
    elif player.speaking_to:
        player.speaking_to.speak(player)


# Inspect container logic
def inspect_container(action, target):
    # check to see if the target is in the container dictionary.
    # didn't it have to be to get here, you ask?
    # yes BUT if you're inspecting an item in the container and then stop inspecting that item, it falls back to this.
    if target in world.container:
        target_container = world.container.get(target)
        # check to make sure the target is in the room
        if target_container in player.current_room.items:
            # set player inspecting container for display check
            player.inspecting_container = target_container
            player.inspecting_container.on_open(player)
            print('------------------------------------------------------')
        else:
            print(f"{target_container.name} isn't here")
            print('------------------------------------------------------')
    # fall back on the inspecting container list on the player for when you're backing out of inspecting an item in the container
    else:
        player.inspecting_container[0].on_open(player)


# Inspect item logic
def inspect_item(action, target):
    # get the correct item out of the item dictionary
    target_item = world.item.get(target)
    # set as the inspecting item for display
    player.inspecting_item = target_item
    player.inspecting_item.inspect(player)


# Inspect room logic
def inspect_room(action, target):
    # get the correct room out of the room dictionary
    target_room = world.room.get(target)
    # check to see if it's the current room
    if target_room == player.current_room:
        target_room.inspect(player)
    # don't allow inspect if it isn't the current room
    else:
        print("Uh... that's not where you are. If you want to look around there you'll need to go there.")
        print('------------------------------------------------------')


# Main inspect
def start_inspect(action, target):
    # check type of target and direct accordingly
    if target in world.room:
        inspect_room(action, target)
    elif target in world.container:
        inspect_container(action, target)
    elif target in world.item:
        inspect_item(action, target)
    else:
        print("I don't know what you mean. Press h for help")
        print('------------------------------------------------------')


# Stop inspect
def stop_inspect(action, target):
    if target in world.item:
        print(f'You stop looking at {player.inspecting_item[0].name}')
        print('------------------------------------------------------')
        player.inspecting_item = []
        inspect_container(action, player.inspecting_container[0].name)
    elif target in world.container:
        print(f'You stop examining the {player.inspecting_container[0].name}')
        print('------------------------------------------------------')
        player.inspecting_container = []
    elif target in world.character:
        print(f"You leave {player.speaking_to.name}.")
        print('------------------------------------------------------')
        player.speaking_to = []


# Take item logic
def take_item(action, target):
    # check to see if the target is an item
    if target in world.item:
        target_item = world.item.get(target)
        if len(player.inspecting_container) > 0:
            item_container = player.inspecting_container[0]
            # check to see if the target item is in the container being inspected
            if target_item in item_container.contents:
                target_item.on_take_container(player, item_container)
                if len(player.inspecting_item) > 0 and player.inspecting_item[0] == target_item:
                    player.inspecting_item = []
            else:
                print("I don't see that item here")
                print('------------------------------------------------------')
        else:
            if target_item in player.current_room.items:
                target_item.on_take_room(player)
            else:
                print("I don't see that item here")
                print('------------------------------------------------------')
    else:
        print("You can't take that.")
        print('------------------------------------------------------')


# Drop item logic
def drop_item(action, target):
    # check to see if the target is an item
    if target in world.item:
        target_item = world.item.get(target)
        if target_item in player.items:
            target_item.on_drop(player)
        else:
            print("You don't seem to have that item")
            print('------------------------------------------------------')
    else:
        print("That's not something you can drop")
        print('------------------------------------------------------')


# Use item logic
def use_item(action, target):
    if target in world.item:
        target_item = world.item.get(target)
        if target_item in player.items:
            target_item.on_use(player)
        else:
            print("You can't use something you don't have")
            print('------------------------------------------------------')
    else:
        print("That's not something you can use")
        print('------------------------------------------------------')


# Main text display
def main_text():
    print('------------------------------------------------------')
    # check to see if the player is inspecting an item
    if len(player.inspecting_item) > 0:
        print(f'Where you are: {player.current_room.name}. \nYou are inspecting {player.inspecting_item[0].name}\n')
    # check to see if the player is inspecting a container
    elif len(player.inspecting_container) > 0:
        print(f'Where you are: {player.current_room.name}. \nYou are inspecting {player.inspecting_container[0].name}\n')
    # check to see if the player is speaking to a character
    # elif len(player.speaking_to) > 0:
    elif player.speaking_to:
        print(f'Where you are: {player.current_room.name}. \nYou are speaking to {player.speaking_to.name}')
    # print room description
    else:
        special_item = world.item.get('address')
        print(f'Where you are: {player.current_room.name}')
        if player.current_room.name == 'Neighborhood':
            if special_item in player.items:
                print(f"{player.current_room.return_description} \n")
            else:
                print(textwrap.fill(f'{player.current_room.description} \n', width=60))
        else:
            print(textwrap.fill(f'{player.current_room.description} \n', width=60))
        print('------------------------------------------------------')


# Actually start the game
start_game()
intro_game()


while True:
    main_text()
    player_move = input(f"What's your move, {player.name}?")

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

    if action in character_actions:
        talk_to_character(action, target)

    if action in use_item_actions:
        use_item(action, target)

    if action in move:
        move_player(action)
