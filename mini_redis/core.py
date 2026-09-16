import time

from .hashmap import HashMap
from .heap import MinHeap
from .linked_list import DoublyLinkedList
from .models import LRUEntry, MemoryInfo, RedisEntry


# HashMap, 이중 연결 리스트, Min Heap을 통합하여 Mini Redis의 핵심 기능을 구현한다.
class MiniRedis:
    # Mini Redis에서 사용할 자료구조와 메모리 상태를 초기화한다.
    def __init__(self):
        self._data = HashMap()
        self._lru = DoublyLinkedList()
        self._lru_nodes = HashMap()
        self._ttl = MinHeap()

        self._used_memory = 0
        self._maxmemory = 0
        self._evicted_keys = 0

    # 키와 값이 사용하는 UTF-8 바이트 크기를 계산한다.
    def _memory_size(self, key, value):
        return len(key.encode("utf-8")) + len(value.encode("utf-8"))

    # 만료 시간이 지난 키를 Min Heap에서 찾아 삭제한다.
    def _remove_expired(self):
        current_time = time.time()

        while True:
            item = self._ttl.peek()

            if item is None:
                break

            expire_at, key = item

            if expire_at > current_time:
                break

            self._ttl.pop()

            entry = self._data.get(key)

            if entry is None:
                continue

            if entry.expire_at != expire_at:
                continue

            self._delete_key(key)

    # HashMap과 LRU에서 지정한 키를 삭제하고 사용 메모리를 갱신한다.
    def _delete_key(self, key):
        entry = self._data.remove(key)

        if entry is None:
            return False

        self._used_memory -= self._memory_size(
            key,
            entry.value,
        )

        node = self._lru_nodes.remove(key)

        if node is not None:
            self._lru.remove_node(node)

        return True

    # 이미 존재하는 키를 LRU 리스트의 맨 앞으로 이동한다.
    def _touch_lru(self, key):
        node = self._lru_nodes.get(key)

        if node is not None:
            self._lru.move_to_front(node)

    # 새로운 키를 LRU 리스트의 맨 앞에 추가한다.
    def _add_lru(self, key, value):
        node = self._lru.insert_front(
            LRUEntry(key, value)
        )

        self._lru_nodes.put(key, node)

    # 가장 오래 사용되지 않은 키를 LRU 리스트에서 제거한다.
    def _evict_lru(self):
        node = self._lru.tail

        if node is None:
            return False

        key = node.data.key

        if self._delete_key(key):
            self._evicted_keys += 1
            return True

        return False

    # 최대 메모리를 초과하면 오래된 키부터 제거한다.
    def _evict_if_needed(self):
        if self._maxmemory == 0:
            return

        while self._used_memory > self._maxmemory:
            if not self._evict_lru():
                break

    # 키와 값을 저장하고 기존 키가 있다면 값을 덮어쓴다.
    def set(self, key, value):
        self._remove_expired()

        new_memory = self._memory_size(key, value)

        if self._maxmemory > 0 and new_memory > self._maxmemory:
            return False

        old_entry = self._data.get(key)

        if old_entry is not None:
            self._used_memory -= self._memory_size(
                key,
                old_entry.value,
            )

            old_node = self._lru_nodes.remove(key)

            if old_node is not None:
                self._lru.remove_node(old_node)

        entry = RedisEntry(value)

        self._data.put(key, entry)
        self._used_memory += new_memory

        self._add_lru(key, value)
        self._evict_if_needed()

        return True

    # 키에 저장된 값을 반환하고 성공한 조회를 LRU 최신 상태로 만든다.
    def get(self, key):
        self._remove_expired()

        entry = self._data.get(key)

        if entry is None:
            return None

        self._touch_lru(key)

        return entry.value

    # 키를 삭제하고 실제로 삭제되었는지 반환한다.
    def delete(self, key):
        self._remove_expired()
        return self._delete_key(key)

    # 키가 존재하는지 확인한다.
    def exists(self, key):
        self._remove_expired()
        return self._data.contains(key)

    # 현재 저장된 키의 개수를 반환한다.
    def dbsize(self):
        self._remove_expired()
        return self._data.size()

    # 현재 저장된 모든 키를 하나씩 반환한다.
    def keys(self):
        self._remove_expired()

        for key in self._data.keys():
            yield key

    # 최대 메모리 사용량을 설정한다.
    def set_maxmemory(self, maxmemory):
        if maxmemory < 0:
            raise ValueError(
                "maxmemory는 0 이상의 정수여야 합니다."
            )

        self._maxmemory = maxmemory
        self._evict_if_needed()

    # 현재 Mini Redis의 메모리 상태를 반환한다.
    def memory_info(self):
        return MemoryInfo(
            used_memory=self._used_memory,
            maxmemory=self._maxmemory,
            evicted_keys=self._evicted_keys,
        )

    # 지정한 키에 초 단위 TTL을 설정한다.
    def expire(self, key, seconds):
        self._remove_expired()

        entry = self._data.get(key)

        if entry is None:
            return False

        expire_at = time.time() + seconds
        entry.expire_at = expire_at

        self._ttl.push((expire_at, key))

        if seconds <= 0:
            self._remove_expired()

        return True

    # 키의 남은 TTL을 초 단위 정수로 반환한다.
    def ttl(self, key):
        self._remove_expired()

        entry = self._data.get(key)

        if entry is None:
            return -2

        if entry.expire_at is None:
            return -1

        remaining = int(
            entry.expire_at - time.time()
        )

        if remaining < 0:
            self._delete_key(key)
            return -2

        return remaining