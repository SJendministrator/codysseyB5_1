# Redis에 저장되는 하나의 키와 값을 표현한다.
class RedisEntry:
    # 값과 만료 시간을 저장한다.
    def __init__(self, value, expire_at=None):
        self.value = value
        self.expire_at = expire_at


# LRU 리스트에서 관리할 키와 값을 표현한다.
class LRUEntry:
    # 키와 값을 저장한다.
    def __init__(self, key, value):
        self.key = key
        self.value = value


# Mini Redis의 메모리 상태를 표현한다.
class MemoryInfo:
    # 현재 사용 메모리와 최대 메모리 및 eviction 횟수를 저장한다.
    def __init__(self, used_memory, maxmemory, evicted_keys):
        self.used_memory = used_memory
        self.maxmemory = maxmemory
        self.evicted_keys = evicted_keys