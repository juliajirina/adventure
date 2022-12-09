# adventure.py

from room import Room
from history import History
from item import Item

class Adventure():

    # Create rooms and items for the appropriate 'game' version.
    def __init__(self, game):

        # Rooms is a dictionary that maps a room number to the corresponding room object
        self.rooms: dict[int,Room] = {}

         # items is a dict that will contain all items for every room
        self.items: dict[int,list[Item]] = {}

        # Keep track of visited rooms in separate history object
        self.visited_rooms = History()

        # Load room structures
        self.load_rooms(f"data/{game}Adv.dat")

        # Game always starts in room number 1, so we'll set it after loading
        assert 1 in self.rooms
        self.current_room = self.rooms[1]
        self.inventory = self.items[0]

    # Load rooms from filename in two-step process
    def load_rooms(self, filename):

        section = 0
        with open(filename) as f:

            # first phase: create all rooms
            for line in f:
                if line != '\n':
                    room_data = line.split("\t")
                    room_id = int(room_data[0])
                    room_name = room_data[1].strip()
                    room_descr = room_data[2].strip()
                    room = {room_id:Room(room_id, room_name, room_descr)}
                    self.rooms.update(room)
                if line == '\n':
                    section += 1
                    if section == 1:
                        break

            assert 1 in self.rooms
            assert self.rooms[1].room_name == "Outside building"

            # second phase: make all connections
            for line in f:
                if line != '\n':
                    connection_data = line.split("\t")
                    source_room = self.rooms[int(connection_data[0])]
                    for i in range(1, len(connection_data), 2):
                        if connection_data[i] == '\n':
                            break
                        if connection_data[i+1].strip().isnumeric():
                            destination_room = self.rooms[int(connection_data[i + 1])]
                            source_room.add_connection(connection_data[i].strip(), destination_room)
                        else:
                            conditional_data = connection_data[i+1].split("/")
                            destination_room = self.rooms[int(conditional_data[0])]
                            conditional_item = conditional_data[1].strip()
                            source_room.add_connection(connection_data[i].strip(), destination_room, conditional_item)

                if line == '\n':
                    section += 1
                    if section == 2:
                        break
            
            # third phase: load items
            for line in f:
                if line != '\n':
                    item_data = line.split("\t")
                    item_name = item_data[0].strip()
                    item_descr = item_data[1].strip()
                    spawn_loc = int(item_data[2])
                    if spawn_loc in self.items:
                        item = Item(item_name,item_descr,spawn_loc)
                        self.items[spawn_loc].append(item)
                    else:
                        item = {spawn_loc:[Item(item_name,item_descr,spawn_loc)]}
                        self.items.update(item)
            inventory = {0:[]}
            self.items.update(inventory)

    # Pass along the description of the current room
    def get_description(self) -> str:
        if self.current_room.is_visited():
            return f'{self.current_room.room_name}'
        else:
            return f'{self.current_room.room_descr}'

     # Pass along the long description of the current room
    def get_long_description(self) -> str:
        return f'{self.current_room.room_descr}'

    # Check the current room for items
    def check_items(self) -> bool:
        return self.current_room.room_id in self.items

    # Pass along the description of the items in the current room
    def get_items_description(self):
        if self.current_room.room_id in self.items:
            items = [item for item in self.items[self.current_room.room_id]]
            return '\n'.join(str(items)[1:-1].split(', '))

    # Pass along current items in inventory
    def show_inventory(self) -> str:
        inventory = [item for item in self.inventory]
        if len(inventory) == 0:
            return 'Your inventory is empty'
        return '\n'.join(str(inventory)[1:-1].split(', '))

    # Index easier
    def options(self,direction):
        return [room for room in self.current_room.get_connection(direction)]

    # Move to a different room by changing "current" room, if possible
    def move(self, direction: str) -> bool:
        if self.current_room.has_connection(direction):
            self.visited_rooms.push(self.current_room)
            self.current_room.set_visited()
            ways = self.options(direction)
            for option in ways:
                for stuff in self.inventory:
                    if option[1] == stuff.name:
                        for room in ways:
                            if option == room:
                                self.current_room = room[0] 
                                return True
                else:
                    if option[1] is None:
                        for room in ways:
                            if option == room:
                                self.current_room = room[0] 
                                return True
        else:
            return False
    
    # Grab items by adding them to inventory and removing them from self.items list for current room
    def take_item(self, action: str):
        if self.current_room.room_id in self.items:
            for item in self.items[self.current_room.room_id]:
                if item.name == action:
                    action = item
                    action.change_loc(0)
                    self.inventory.append(action)
                    self.items[self.current_room.room_id].remove(action)
                    return f'{action.name} taken.'
                else:
                    return f'No such item.'
        else:
            return f'No such item.'

    # Drop items by removing them to inventory and adding them from self.items list for current room
    def drop_item(self, action: str) -> bool:
        for item in self.inventory:
            if item.name == action:
                action = item
                action.change_loc(self.current_room.room_id)
                self.inventory.remove(action)
                if self.current_room.room_id in self.items:
                    self.items[self.current_room.room_id].append(action)
                    return f'{action.name} dropped.'
                else:
                    item = {action.spawn_loc:[action]}
                    self.items.update(item)
                    return f'{action.name} dropped.'
        else:
            return f'No such item.'

    # Go back one step in the history of visited rooms, if possible
    def go_back(self):
        if self.visited_rooms.no_history():
            return None
        elif self.visited_rooms.size() > 0:
            self.current_room = self.visited_rooms.pop()
            return self.current_room
    
    # Check whether a move is forced or not
    def is_forced(self) -> bool:
        return 'FORCED' in self.current_room.connections


if __name__ == "__main__":
    
    from sys import argv

    # Check command line arguments
    if len(argv) not in [1,2]:
        print("Usage: python adventure.py [name]")
        exit(1)

    # Load the requested game or else Tiny
    if len(argv) == 1:
        game_name = "Tiny"
    elif len(argv) == 2:
        game_name = argv[1]

    # Create game
    adventure = Adventure(game_name)

    # Welcome user
    print("Welcome to Adventure.\n")

    # Print very first room description
    print(adventure.get_description())

    # Prompt the user for commands until they type QUIT
    while True:

        # Prompt
        command = input("> ").upper()
        if len(command)  == 0:
            continue
        action = command.split()

        # Perform move
        if adventure.move(command):
            while adventure.is_forced():
                print(adventure.get_long_description())
                adventure.move('FORCED')
                print(adventure.get_description())
                if adventure.check_items():
                    print(adventure.get_items_description())
            else:
                print(adventure.get_description())
                if adventure.check_items():
                    print(adventure.get_items_description())

        # Perform action
        elif action[0] == "TAKE":
            print(adventure.take_item(action[1]))
        elif action[0] == "DROP":
            print(adventure.drop_item(action[1]))
        
        elif command == "INVENTORY":
            print(adventure.show_inventory())

        # Escape route
        elif command == "QUIT":
            break
       
        elif command == "HELP":
            print("You can move by typing directions such as EAST/WEST/IN/OUT\n"
                  "QUIT quits the game.\n"
                  "HELP prints instructions for the game.\n"
                  "INVENTORY lists the item in your inventory.\n"
                  "LOOK lists the complete description of the room and its contents.\n"
                  "TAKE <item> take item from the room.\n"
                  "DROP <item> drop item from your inventory.")
        
        elif command == "LOOK":
            print(adventure.get_long_description())
            if adventure.check_items():
                    print(adventure.get_items_description())
        
        elif command == "BACK":
            if adventure.go_back():
                if adventure.is_forced():
                    adventure.go_back()
                print(adventure.get_description())
                if adventure.check_items():
                    print(adventure.get_items_description())
            else:
                print('Can\'t go back further.')

        else:
            print("Invalid command.")
