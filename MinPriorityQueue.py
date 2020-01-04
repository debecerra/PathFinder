""" Class definition for MinProrityQueue class. """

class MinPriorityQueue:
    """ Implementation of a Min Priority Queue using the Min Heap data structure.

    The MinPriorityQueue class is holds key-value pairs in min-heap data structure,
    allowing for efficient implementation of extracting the element with the minimum key,
    decreasing the key of an existing element and inserting new elements.

    Attributes:
        elements: A list/array of key value pairs that hold the elements of the MinPriorityQueue
        size: The number of elements in the MinPriorityQueue
        mapping: A dict that maps each element/value to its index position in elements, allowing
            for O(1) lookup of existing elements
    """

    # Interface Methods

    def __init__(self, *args):
        self.__elements = []
        self.__size = 0
        self.__mapping = {}

        for key_value in args:
            assert isinstance(key_value, tuple)
            assert isinstance(key_value[0], int)
            self.__elements.append(key_value)
            self.__size += 1
            self.__mapping[key_value[1]] = self.__size - 1

        self.build_min_heap()

    def extract_min(self):
        """ Extract the smallest element from the min-heap.

        Exchanges element at root of min heap with element at the end of the
        min-heap. Then returns element which was initially at the root of the
        min-heap, which is the smallest element. Runs in O(logn).

        Raises:
            IndexError: no element in MinPriorityQueue that can be extracted

        Returns:
            smallest: the element in the heap with the smallest key (highest priority)
        """

        if self.__size == 0:
            raise IndexError("Priority queue is empty")

        # Swap smallest with last element
        smallest = self.__elements[0]
        self.__elements[0] = self.__elements[self.__size-1]

        # Update heap size
        self.__elements.pop()
        self.__size -= 1

        # Remove mapping for smallest
        self.__mapping.pop(smallest[1])

        # Restore heap property
        if self.__size > 0:
            self.__mapping[self.__elements[0][1]] = 0  # Update mapping
            self.min_heapify(0)

        return smallest[1]

    def decrease_key(self, element, new_key):
        """ Increase the priority of an existing element in the min priority queue.

        Decreases the key of an element in the min-heap based MinPriorityQueue. The
        index mapping is used to find the key we want to move in O(1) time. The key is decreased.
        Then the heap property is restored.

        Args:
            element: the element to be updated
            new_key: the new int key to be assigned to the element

        Raises:
            KeyError: element does not exist in the MinPriorityQueue
            ValueError: new key is greater than current key
        """

        # Find index of existing element
        try:
            i = self.__mapping[element]
        except KeyError:
            raise KeyError('Element does not exist.')

        if new_key <= self.__elements[i][0]:
            self.__elements[i] = (new_key, self.__elements[i][1])
        else:
            raise ValueError('New key must be less than current key')

        while i > 0 and self.__elements[self.parent(i)][0] > self.__elements[i][0]:
            p = self.parent(i)

            # Swap element with parent and bubble up
            temp = self.__elements[i]
            self.__elements[i] = self.__elements[p]
            self.__elements[p] = temp

            # Update the mappings
            self.__mapping[self.__elements[i][1]] = i
            self.__mapping[self.__elements[p][1]] = p

            i = self.parent(i)

    def insert(self, new_key, new_element):
        """ Insert a new element into the min priority queue.

        Inserts a new element into the priority queue with the lowest priority.
        Then decreases key to desired key value.

        Args:
            new_key: the int key of the element to be inserted
            new_element: the element to be inserted
        """

        self.__elements.append((new_key, new_element))
        self.__size += 1
        self.__mapping[new_element] = self.__size - 1
        self.decrease_key(new_element, new_key)

    def element_exists(self, element):
        """ Returns True if given element exists in the min priority queue. """

        i = self.__mapping.get(element, -1)
        return i >= 0

    def get_key(self, element):
        """ Gets the key of a given element. 

        Raises:
            KeyError: element does not exist in MinPriorityQueue
        """

        i = self.__mapping.get(element)
        if i is None:
            raise KeyError('Element does not exist.')
        key = self.__elements[i][0]
        return key


    # Private Helper Methods

    def leftchild(self, i):
        """ Gets index of the left child of given element. """

        return 2*i + 1

    def rightchild(self, i):
        """ Gets index of the right child of given element. """

        return 2*i + 2

    def parent(self, i):
        """ Gets index of the parent of given element. """

        return (i-1) // 2

    def min_heapify(self, i):
        """ Turns an almost-heap into a heap.

        Given an almost-min-heap rooted at index i (only the root does not
        satisfy the heap property), turn it into a min-heap.

        Args:
            i : the index of the given almost heap
        """
        lc = self.leftchild(i)
        rc = self.rightchild(i)
        smallest = i

        # Find the smallest out of left child, right child and root
        if lc < self.__size and self.__elements[lc][0] < self.__elements[smallest][0]:
            smallest = lc
        if rc < self.__size and self.__elements[rc][0] < self.__elements[smallest][0]:
            smallest = rc

        if smallest != i:
            # Swap root of sub-heap with smallest child
            temp = self.__elements[i]
            self.__elements[i] = self.__elements[smallest]
            self.__elements[smallest] = temp

            # Update the mappings
            self.__mapping[self.__elements[i][1]] = i
            self.__mapping[self.__elements[smallest][1]] = smallest

            # Recursive call on sub-heap rooted at smallest
            self.min_heapify(smallest)

    def build_min_heap(self):
        """ Builds min-heap from current list of elements. """

        for i in range(self.parent(self.__size-1), -1, -1):
            self.min_heapify(i)
