# 이중 연결 리스트의 하나의 노드를 표현한다.
class Node:
    # 노드의 데이터와 이전/다음 노드 연결 정보를 초기화한다.
    def __init__(self, data):
        self.prev = None
        self.next = None
        self.data = data


# 삽입과 삭제를 O(1)에 처리할 수 있는 이중 연결 리스트를 구현한다.
class DoublyLinkedList:
    # 빈 이중 연결 리스트를 초기화한다.
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    # 새로운 노드를 리스트의 맨 앞에 삽입한다.
    def insert_front(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self._size += 1
        return new_node

    # 새로운 노드를 리스트의 맨 뒤에 삽입한다.
    def insert_back(self, data):
        new_node = Node(data)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1
        return new_node

    # 리스트의 맨 앞 노드를 삭제하고 데이터를 반환한다.
    def remove_front(self):
        if self.head is None:
            return None

        removed_node = self.head

        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        removed_node.prev = None
        removed_node.next = None
        self._size -= 1

        return removed_node.data

    # 리스트의 맨 뒤 노드를 삭제하고 데이터를 반환한다.
    def remove_back(self):
        if self.tail is None:
            return None

        removed_node = self.tail

        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        removed_node.prev = None
        removed_node.next = None
        self._size -= 1

        return removed_node.data

    # 지정한 노드를 리스트에서 O(1) 시간에 삭제한다.
    def remove_node(self, node):
        if node is None:
            return None

        if node is self.head:
            return self.remove_front()

        if node is self.tail:
            return self.remove_back()

        node.prev.next = node.next
        node.next.prev = node.prev

        data = node.data

        node.prev = None
        node.next = None
        self._size -= 1

        return data

    # 지정한 노드를 리스트의 맨 앞으로 O(1) 시간에 이동한다.
    def move_to_front(self, node):
        if node is None or node is self.head:
            return

        if node is self.tail:
            self.tail = node.prev

        node.prev.next = node.next

        if node.next is not None:
            node.next.prev = node.prev

        node.prev = None
        node.next = self.head

        self.head.prev = node
        self.head = node

    # 현재 리스트에 저장된 노드의 개수를 반환한다.
    def size(self):
        return self._size