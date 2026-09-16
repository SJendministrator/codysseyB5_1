from .linked_list import DoublyLinkedList


# 키와 값을 하나의 데이터로 저장하는 HashMap 노드를 만든다.
class HashMapEntry:
    # 키와 값을 저장한다.
    def __init__(self, key, value):
        self.key = key
        self.value = value


# 체이닝 방식으로 충돌을 처리하는 HashMap을 구현한다.
class HashMap:
    # 지정된 크기의 버킷 배열을 생성하고 HashMap을 초기화한다.
    def __init__(self, initial_capacity=8):
        self._buckets = [None] * initial_capacity
        self._size = 0
        self._capacity = initial_capacity

    # 문자열 키를 정수 해시값으로 변환한다.
    def _hash(self, key):
        hash_value = 0

        for character in key:
            hash_value = (hash_value * 31 + ord(character)) & 0xFFFFFFFF

        return hash_value

    # 키에 해당하는 버킷 번호를 계산한다.
    def _get_index(self, key):
        return self._hash(key) % self._capacity

    # 현재 저장된 항목의 비율을 계산한다.
    def _load_factor(self):
        return self._size / self._capacity

    # 새로운 키와 값을 저장하거나 기존 값을 수정한다.
    def put(self, key, value):
        index = self._get_index(key)

        if self._buckets[index] is None:
            self._buckets[index] = DoublyLinkedList()

        bucket = self._buckets[index]
        current = bucket.head

        while current is not None:
            entry = current.data

            if entry.key == key:
                entry.value = value
                return

            current = current.next

        bucket.insert_back(HashMapEntry(key, value))
        self._size += 1

        if self._load_factor() > 0.75:
            self._resize()

    # 키에 해당하는 값을 반환한다.
    def get(self, key):
        index = self._get_index(key)
        bucket = self._buckets[index]

        if bucket is None:
            return None

        current = bucket.head

        while current is not None:
            entry = current.data

            if entry.key == key:
                return entry.value

            current = current.next

        return None

    # 키에 해당하는 항목을 삭제하고 값을 반환한다.
    def remove(self, key):
        index = self._get_index(key)
        bucket = self._buckets[index]

        if bucket is None:
            return None

        current = bucket.head

        while current is not None:
            entry = current.data

            if entry.key == key:
                value = entry.value
                bucket.remove_node(current)
                self._size -= 1

                if bucket.size() == 0:
                    self._buckets[index] = None

                return value

            current = current.next

        return None

    # 해당 키가 HashMap에 존재하는지 확인한다.
    def contains(self, key):
        index = self._get_index(key)
        bucket = self._buckets[index]

        if bucket is None:
            return False

        current = bucket.head

        while current is not None:
            if current.data.key == key:
                return True

            current = current.next

        return False

    # 저장된 모든 키를 순서 없이 하나씩 반환한다.
    def keys(self):
        for bucket in self._buckets:
            if bucket is None:
                continue

            current = bucket.head

            while current is not None:
                yield current.data.key
                current = current.next

    # 현재 저장된 항목의 개수를 반환한다.
    def size(self):
        return self._size

    # 버킷 수를 두 배로 늘리고 기존 데이터를 재배치한다.
    def _resize(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity

        for bucket in old_buckets:
            if bucket is None:
                continue

            current = bucket.head

            while current is not None:
                entry = current.data

                index = self._get_index(entry.key)

                if self._buckets[index] is None:
                    self._buckets[index] = DoublyLinkedList()

                self._buckets[index].insert_back(
                    HashMapEntry(entry.key, entry.value)
                )

                current = current.next