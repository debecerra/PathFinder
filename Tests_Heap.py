""" Test file for MinPriorityQueue.py """

import unittest
from MinPriorityQueue import MinPriorityQueue


class TestHeapDataStructure(unittest.TestCase):
    """ Unittest class from testing MinPriorityQueue class """

    def test_init(self):
        """ Test for __init__ method in MinPriorityQueue class. """

        a = MinPriorityQueue()
        expected = []
        self.assertListEqual(a.elements, expected)

        b = MinPriorityQueue((2, 'apple'), (3, 'orange'), (4, 'banana'))
        expected = [(2, 'apple'), (3, 'orange'), (4, 'banana')]
        self.assertListEqual(b.elements, expected)

        c = MinPriorityQueue((4, 'banana'), (3, 'orange'), (2, 'apple'))
        expected = [(2, 'apple'), (3, 'orange'), (4, 'banana')]
        self.assertListEqual(c.elements, expected)

        flag = False
        try:
            MinPriorityQueue(9)
        except AssertionError:
            flag = True
        self.assertTrue(flag)

        flag = False
        try:
            MinPriorityQueue(('1', '2'))
        except AssertionError:
            flag = True
        self.assertTrue(flag)


    def test_min_heapify(self):
        """ Test for min_heapify method in MinPriorityQueue class. """

        queue = MinPriorityQueue()

        queue.elements = [(4, 'apple'), (2, 'bear'), (3, 'tangerine')]
        queue.size = 3
        queue.min_heapify(0)
        result = queue.elements
        expected = [(2, 'bear'), (4, 'apple'), (3, 'tangerine')]

        self.assertListEqual(result, expected)

        queue.elements = [(3, "apple"), (8, "pear"), (5, "orange"), (7, "bear"), (6, "fruit")]
        queue.size = 5
        queue.min_heapify(2)
        result = queue.elements
        expected = [(3, "apple"), (8, "pear"), (5, "orange"), (7, "bear"), (6, "fruit")]

        self.assertListEqual(result, expected)

        queue.elements = [(3, "apple"), (8, "pear"), (5, "orange"), (7, "bear"), (6, "fruit")]
        queue.size = 5
        queue.min_heapify(1)
        result = queue.elements
        expected = [(3, "apple"), (6, "fruit"), (5, "orange"), (7, "bear"), (8, "pear")]

        self.assertListEqual(result, expected)

    def test_build_min_heap(self):
        """ Test for build_max_heap method in MinPriorityQueue class. """

        queue = MinPriorityQueue()

        queue.elements = [(4, 'apple'), (2, 'apple'), (3,)]
        queue.size = 3

        queue.build_min_heap()

        expected = [(2, 'apple'), (4, 'apple'), (3,)]
        results = queue.elements
        self.assertEqual(results, expected)


        queue.elements = [(3, ''), (8, ''), (5, ''), (7, ''), (6, '')]
        queue.size = 5

        queue.build_min_heap()

        expected = [(3, ''), (6, ''), (5, ''), (7, ''), (8, '')]
        results = queue.elements
        self.assertEqual(results, expected)


        queue.elements = [(10, ''), (9, ''), (8, ''), (7, ''), (6, ''), (5, ''), (4, ''), (3, ''), (2, ''), (1, '')]
        queue.size = 10

        queue.build_min_heap()

        expected = [(1, ''), (2, ''), (4, ''), (3, ''), (6, ''), (5, ''), (8, ''), (10, ''), (7, ''), (9, '')]
        results = queue.elements
        self.assertEqual(results, expected)

    def test_extract_min(self):
        """ Test for extract_min method in MinPriorityQueue class. """

        queue = MinPriorityQueue((3, 'apple'), (8, 'turkey'), (5, 'ham'), (6, 'rooster'), (6, 'water'))

        smallest = queue.extract_min()
        expected_smallest = (3, "apple")
        expected_leftover = [(8, 'turkey'), (5, 'ham'), (6, 'rooster'), (6, 'water')]
        self.assertTupleEqual(smallest, expected_smallest)
        self.assertSetEqual(set(queue.elements), set(expected_leftover))

        smallest = queue.extract_min()
        expected_smallest = (5, "ham")
        expected_leftover = [(8, 'turkey'), (6, 'rooster'), (6, 'water')]
        self.assertTupleEqual(smallest, expected_smallest)
        self.assertSetEqual(set(queue.elements), set(expected_leftover))

        smallest = queue.extract_min()
        expected_smallest = (6, "rooster")  # Could also be water
        expected_leftover = [(8, 'turkey'), (6, 'water')]
        self.assertTupleEqual(smallest, expected_smallest)
        self.assertSetEqual(set(queue.elements), set(expected_leftover))

        smallest = queue.extract_min()
        expected_smallest = (6, "water")
        expected_leftover = [(8, 'turkey')]
        self.assertTupleEqual(smallest, expected_smallest)
        self.assertSetEqual(set(queue.elements), set(expected_leftover))

        smallest = queue.extract_min()
        expected_smallest = (8, "turkey")
        expected_leftover = []
        self.assertTupleEqual(smallest, expected_smallest)
        self.assertSetEqual(set(queue.elements), set(expected_leftover))

        flag = False
        try:
            queue.extract_min()
        except IndexError:
            flag = True
        self.assertTrue(flag)

    def test_decrease_key(self):
        """ Test for decrease_key method in MinPriorityQueue class. """

        queue = MinPriorityQueue((3, 'apple'), (8, 'turkey'), (5, 'ham'), (6, 'rooster'), (6, 'water'))

        queue.decrease_key('water', 4)
        expected = [(3, 'apple'), (4, 'water'), (5, 'ham'), (8, 'turkey'), (6, 'rooster')]
        self.assertEqual(queue.elements, expected)

        queue.decrease_key('rooster', 2)
        expected = [(2, 'rooster'), (3, 'apple'), (5, 'ham'), (8, 'turkey'), (4, 'water')]
        self.assertEqual(queue.elements, expected)

        queue.decrease_key('water', 1)
        expected = [(1, 'water'), (2, 'rooster'), (5, 'ham'), (8, 'turkey'), (3, 'apple')]
        self.assertEqual(queue.elements, expected)

    def test_insert(self):
        """ Test for decrease_key method in MinPriorityQueue class. """

        queue = MinPriorityQueue()

        queue.insert(6, 'apple')
        expected = [(6, 'apple')]
        self.assertListEqual(queue.elements, expected)

        queue.insert(4, 'cat')
        expected = [(4, 'cat'), (6, 'apple')]
        self.assertListEqual(queue.elements, expected)

        queue.insert(8, 'snow')
        expected = [(4, 'cat'), (6, 'apple'), (8, 'snow')]
        self.assertListEqual(queue.elements, expected)

        queue.insert(2, 'hare')
        expected = [(2, 'hare'), (4, 'cat'), (8, 'snow'), (6, 'apple')]
        self.assertListEqual(queue.elements, expected)

if __name__ == '__main__':
    unittest.main()
