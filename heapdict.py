import collections

#@profile
def _min_heapify(heap, i):
    l = ((i << 1) + 1)
    r = ((i+1) << 1)
    n = len(heap)
    low = l if l < n and heap[l][0] < heap[i][0] else i
    if r < n and heap[r][0] < heap[low][0]:
        low = r

    if low != i:
        heap[i], heap[low] = heap[low], heap[i]
        heap[i][2] = i
        heap[low][2] = low
        _min_heapify(heap, low)


class heapdict(collections.MutableMapping):
    __marker = object()

    @staticmethod
    def _parent(i):
        return ((i - 1) >> 1)
    
    def __init__(self, *args, **kw):
        self.heap = []
        self.d = {}
        self.update(*args, **kw)

    def clear(self):
        self.heap.clear()
        self.d.clear()

    #@profile
    def __setitem__(self, key, value):
        if key in self.d:
            del self[key]
        wrapper = [value, key, len(self)]
        self.d[key] = wrapper
        self.heap.append(wrapper)
        self._decrease_key(len(self.heap)-1)

    def _decrease_key(self, i):
        while i:
            parent = ((i - 1) >> 1)
            if self.heap[parent][0] < self.heap[i][0]: break
            self._swap(i, parent)
            i = parent

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.heap[i][2] = i
        self.heap[j][2] = j

    #@profile
    def __delitem__(self, key):
        wrapper = self.d[key]
        while wrapper[2]:
            parentpos = self._parent(wrapper[2])
            parent = self.heap[parentpos]
            self._swap(wrapper[2], parent[2])
        self.popitem()

    def __getitem__(self, key):
        return self.d[key][0]

    def __iter__(self):
        return iter(self.d)

    #@profile
    def popitem(self):
        """D.popitem() -> (k, v), remove and return the (key, value) pair with 
        lowest value; but raise KeyError if D is empty."""
        wrapper = self.heap[0]
        if len(self.heap) == 1:
            self.heap.pop()
        else:
            self.heap[0] = self.heap.pop(-1)
            self.heap[0][2] = 0
            _min_heapify(self.heap, 0)
        del self.d[wrapper[1]]
        return wrapper[1], wrapper[0]    

    def __len__(self):
        return len(self.d)

    def peekitem(self):
        """D.peekitem() -> (k, v), return the (key, value) pair with lowest 
        value; but raise KeyError if D is empty."""
        return (self.heap[0][1], self.heap[0][0])
