from queue import PriorityQueue

if __name__ == '__main__':
    # This entry value will be the second value in
    # triplet added to the priority queue. Its purpose
    # is to break ties when the priority of two elements
    # is the same. Because entry is incremented after every
    # put, no two elements will have the same entry value.
    # This entry value ensures that if two elements have the
    # same priority, the elements are returned in the order
    # in which they are placed in the queue.
    entry = 0
    a = PriorityQueue()
    elements = ["foo", "bar", "taco", "cat"]
    priorities = [3, 1, 2, 1]

    for i in range(len(elements)):
        a.put((priorities[i], entry, elements[i]))
        entry += 1

    while a.qsize() != 0:
        print(a.get())
