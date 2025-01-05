import pytest


class Heap:
    def __init__(self, number_of_cells):
        self.data = [0] * number_of_cells
        self.names = {}
        self.next = 0

    def _at(self, index):
        return self.data[index]

    def _bang(self, index, value):
        self.data[index] = value

    def allot(self, name, count=1):
        self.names[name] = (self.next, count)
        self.next += count
        if self.next >= len(self.data):
            self.data.extend([0] * 10)

    def at(self, name):
        return self._at(self.names[name][0])

    def bang(self, name, value):
        self._bang(self.names[name][0], value)


class TestHeap:
    def test_heap_access(self):
        heap = Heap(10)
        assert heap._at(5) == 0
        heap._bang(5, 666)
        assert heap._at(5) == 666
        with pytest.raises(IndexError):
            heap._bang(10, 666)

    def test_named_access(self):
        heap = Heap(10)
        heap.allot('X', 1)
        assert heap.at('X') == 0
        heap.bang('X', 666)
        assert heap.at('X') == 666

    def test_extension(self):
        heap = Heap(4)
        heap.allot('X', 2)
        heap.allot('Y')
        heap.allot('Z')
        heap.allot('EXTRA')
        heap.bang('EXTRA', 666)
        assert len(heap.data) == 14
        assert heap.at('EXTRA') == 666
