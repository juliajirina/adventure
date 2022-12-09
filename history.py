# history.py

from room import Room

class History(object):

    def __init__(self) -> None:
        """post: creates an empty LIFO stack"""
        self._history: list[Room] = []
    
    def no_history(self) -> bool:
        """post: returns True if the stack size is 0 (empty), else False"""
        return self.size() == 0

    def push(self, room: Room) -> None:
        """post: places room on top of the stack"""
        self._history.append(room)
    
    def pop(self) -> Room:
        """pre: self.size() > 0
        post: removes and returns the top element of
        the stack"""
        if self.size() > 0:
            room = self._history[self.size() - 1]
            room.visited = False
            self._history = self._history[:-1]
            return room

    def top(self) -> Room:
        """pre: self.size() > 0
        post: returns the top element of the stack without
        removing it"""
        if self.size() > 0:
            return self._history[self.size() - 1]

    def size(self) -> int:
        """post: returns the number of elements in the stack"""
        return len(self._history)
    
    def __str__(self) -> str:
        """post: returns data in list as list"""
        return f'{self._history}'