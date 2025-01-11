class Heap:
    def __init__(self):
        self._heap = []

    def allot(self, n):
        self._heap.extend([0] * n)

    def at(self, index):
        return self._heap[index]

    def comma(self, value):
        self.allot(1)
        self._heap[-1] = value

    def next_available(self):
        return len(self._heap)

    def put(self, index, value):
        self._heap[index] = value
