from mini_redis.linked_list import DoublyLinkedList


# 리스트의 모든 노드를 앞에서부터 확인한다.
def get_forward_values(linked_list):
    values = []
    current = linked_list.head

    while current is not None:
        values.append(current.data)
        current = current.next

    return values


# 리스트의 모든 노드를 뒤에서부터 확인한다.
def get_backward_values(linked_list):
    values = []
    current = linked_list.tail

    while current is not None:
        values.append(current.data)
        current = current.prev

    return values


linked_list = DoublyLinkedList()

a = linked_list.insert_front("A")
b = linked_list.insert_back("B")
c = linked_list.insert_back("C")

assert get_forward_values(linked_list) == ["A", "B", "C"]
assert get_backward_values(linked_list) == ["C", "B", "A"]
assert linked_list.size() == 3

linked_list.move_to_front(c)

assert get_forward_values(linked_list) == ["C", "A", "B"]
assert get_backward_values(linked_list) == ["B", "A", "C"]

linked_list.remove_node(a)

assert get_forward_values(linked_list) == ["C", "B"]
assert get_backward_values(linked_list) == ["B", "C"]
assert linked_list.size() == 2

assert linked_list.remove_front() == "C"
assert linked_list.remove_back() == "B"
assert linked_list.size() == 0

assert linked_list.head is None
assert linked_list.tail is None

print("DoublyLinkedList 테스트 통과!")