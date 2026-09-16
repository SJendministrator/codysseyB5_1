# 최소 힙을 직접 구현하여 가장 작은 값을 항상 루트에 유지한다.
class MinHeap:
    # 빈 힙을 생성한다.
    def __init__(self):
        self._items = []

    # 새로운 값을 힙에 추가하고 위쪽으로 정렬한다.
    def push(self, item):
        self._items.append(item)
        self._heapify_up(len(self._items) - 1)

    # 가장 작은 값을 삭제하고 반환한다.
    def pop(self):
        if not self._items:
            return None

        if len(self._items) == 1:
            return self._items.pop()

        minimum = self._items[0]
        self._items[0] = self._items.pop()
        self._heapify_down(0)

        return minimum

    # 현재 힙에서 가장 작은 값을 삭제하지 않고 반환한다.
    def peek(self):
        if not self._items:
            return None

        return self._items[0]

    # 현재 힙에 저장된 항목의 개수를 반환한다.
    def size(self):
        return len(self._items)

    # 지정한 위치의 값을 부모 노드와 비교하여 위쪽으로 이동한다.
    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2

            if self._items[index] >= self._items[parent_index]:
                break

            self._items[index], self._items[parent_index] = (
                self._items[parent_index],
                self._items[index],
            )

            index = parent_index

    # 지정한 위치의 값을 자식 노드와 비교하여 아래쪽으로 이동한다.
    def _heapify_down(self, index):
        size = len(self._items)

        while True:
            left_index = index * 2 + 1
            right_index = index * 2 + 2
            smallest_index = index

            if (
                left_index < size
                and self._items[left_index] < self._items[smallest_index]
            ):
                smallest_index = left_index

            if (
                right_index < size
                and self._items[right_index] < self._items[smallest_index]
            ):
                smallest_index = right_index

            if smallest_index == index:
                break

            self._items[index], self._items[smallest_index] = (
                self._items[smallest_index],
                self._items[index],
            )

            index = smallest_index