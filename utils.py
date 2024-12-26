import heapq


class PriorityQueue:
    def __init__(self):
        self._heap = []
        self.item_map = {}

    def add_item(self, item, priority: float = 0):
        if item in self.item_map:
            self.remove_item(item)
        item_wrapper = (priority, item, True)
        self.item_map[item] = item_wrapper
        heapq.heappush(self.heap, item_wrapper)

    def remove_item(self, item):
        old_item = self.item_map[item]
        self.item_map[item] = (old_item[0], old_item[1], False)

    def pop_item(self):
        return heapq.heappop(self.heap)

    def change_priority(self, item, priority=0):
        self.add_item(item, priority=priority)

    def decrease_priority(self, item, change=0):
        old_priority = self.item_map[item][0]
        self.change_priority(item, old_priority - change)

    def __contains__(self, item):
        return item in self.item_map

    @property
    def heap(self):
        return self._heap
