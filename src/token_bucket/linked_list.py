"""Small capacity-limited linked list used as the token store."""


class Node:
    """A token and its neighboring nodes."""

    def __init__ (self, data:dict, next_node:object = None, prev_node:object = None ) -> None:
        self.next_node = next_node
        self.prev_node = prev_node
        self.data = data

class LinkedList:
    """Bounded LIFO collection used by the token bucket."""

    def __init__ (self, max_size:int) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self.head = None
        self.tail = None
        self.size = 0
        self.max_size = max_size

    def append(self, data:dict) -> dict:
        """Append an item unless the configured capacity is reached."""
        if self.size < self.max_size:
            if self.size == 0:
                self.head = Node(data=data)
                self.tail = self.head
            elif self.size > 0:
                node = Node(data=data, next_node=None, prev_node=self.tail)
                self.tail.next_node = node
                self.tail = node
            self.size += 1
            return {"appended":True, "current_size":self.size}
        return {"appended":False, "reason":"MAX capacity reached", "current_size":self.size}

    def pop(self) -> dict:
        """Remove and return the newest item, if one exists."""
        if self.size == 0:
            return {"popped":False, "reason":"SIZE is 0"}
        data = self.tail.data
        node = self.tail
        prev_node = node.prev_node
        if prev_node:
            prev_node.next_node = None
        self.tail = prev_node
        self.size -= 1
        if self.size == 0:
            self.head = None

        return {"popped":True, "data":data, "current_size": self.size}

    def get_size(self) -> int:
        """Return the number of stored items."""
        return self.size
