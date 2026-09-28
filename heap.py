def better(a, b):

    # 1. Points
    if a.points != b.points:
        return a.points > b.points

    # 2. Wins
    if a.wins != b.wins:
        return a.wins > b.wins

    # 3. Score Difference
    if a.score_difference != b.score_difference:
        return a.score_difference > b.score_difference

    # 4. Alphabetical order
    return a.name.lower() < b.name.lower()


class MaxHeap:

    def __init__(self):

        self.heap = []

    def insert(self, team):

        self.heap.append(team)

        self._heapify_up()

    def _heapify_up(self):

        index = len(self.heap) - 1

        while index > 0:

            parent = (index - 1) // 2

            if better(self.heap[index], self.heap[parent]):

                self.heap[index], self.heap[parent] = (
                    self.heap[parent],
                    self.heap[index]
                )

                index = parent

            else:

                break

    def extract_max(self):

        if not self.heap:

            return None

        maximum = self.heap[0]

        last = self.heap.pop()

        if self.heap:

            self.heap[0] = last

            self._heapify_down()

        return maximum

    def _heapify_down(self):

        index = 0

        size = len(self.heap)

        while True:

            left = 2 * index + 1
            right = 2 * index + 2

            largest = index

            if (
                left < size
                and better(self.heap[left], self.heap[largest])
            ):

                largest = left

            if (
                right < size
                and better(self.heap[right], self.heap[largest])
            ):

                largest = right

            if largest == index:

                break

            self.heap[index], self.heap[largest] = (
                self.heap[largest],
                self.heap[index]
            )

            index = largest