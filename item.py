# item.py

from room import Room

class Item(object):
    """Represents objects within the Crowther's Adventure Game."""

    def __init__(self, name: str, descr: int, spawn_loc: int) -> None:
        """ Creates an item object with name, description and room_id for initial spawn location. """
        self.name = name
        self.descr = descr
        self.spawn_loc = spawn_loc

    def change_loc(self, location:int):
        self.spawn_loc = location

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f'{self.name}: {self.descr}'
        

