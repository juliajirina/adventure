# room.py

class Room(object):

    def __init__(self, room_id: int, room_name: str, room_descr: str) -> None:
        """1. Storing information about one room: in particular its ID, short description
        and long description.
        2. Storing information about the connections to other rooms, and the commands
        typed to go there, stored in a dictionary."""

        # information about one room
        self.room_id = room_id
        self.room_name = room_name
        self.room_descr = room_descr

        # information about connections
        self.connections: dict[str, list[tuple(object, str)]] = {}

        # short and long descriptions
        self.visited = False
    
    def add_connection(self, direction: str, room_id: object, item: str = None) -> None:
        """pre: direction is string and room is another Room object
        post: stores direction and room in connections dictionary"""
        if direction in self.connections:
            new_connection = room_id, item
            self.connections[direction].append(new_connection)
        else:
            connection = {direction: [(room_id,item)]}
            self.connections.update(connection)

    def has_connection(self, direction: str) -> bool:
        """pre: direction is string
        post: returns true if there is a connection in dictionary under that name"""
        return direction in self.connections

    def get_connection(self, direction: str) -> object:
        """pre: direction is string
        post: returns actual Room object that it connects to"""
        if self.has_connection(direction):
            return self.connections.get(direction)

    def set_visited(self) -> None:
        """post: marks room as visited by setting visited to true"""
        self.visited = True
    
    def is_visited(self) -> bool:
        """post: returns true if room is visited, else false"""
        return self.visited
    
    def __str__(self) -> str:
        return f'{self.room_id}. {self.room_name}, connections: {self.connections}'