import time

from mini_redis.core import MiniRedis


# SET과 GET의 기본 동작을 테스트한다.
def test_set_get():
    redis = MiniRedis()

    assert redis.set("name", "Alice") is True
    assert redis.get("name") == "Alice"

    assert redis.dbsize() == 1


# GET에서 존재하지 않는 키를 조회하는지 테스트한다.
def test_missing_key():
    redis = MiniRedis()

    assert redis.get("unknown") is None
    assert redis.exists("unknown") is False
    assert redis.dbsize() == 0


# 같은 키를 다시 SET하면 기존 값이 교체되는지 테스트한다.
def test_overwrite():
    redis = MiniRedis()

    redis.set("name", "Alice")
    redis.set("name", "Bob")

    assert redis.get("name") == "Bob"
    assert redis.dbsize() == 1


# DEL이 키를 정상적으로 삭제하는지 테스트한다.
def test_delete():
    redis = MiniRedis()

    redis.set("name", "Alice")

    assert redis.delete("name") is True
    assert redis.get("name") is None
    assert redis.dbsize() == 0

    assert redis.delete("name") is False


# EXPIRE와 TTL의 기본 동작을 테스트한다.
def test_expire():
    redis = MiniRedis()

    redis.set("name", "Alice")

    assert redis.expire("name", 2) is True

    ttl = redis.ttl("name")

    assert ttl >= 1
    assert ttl <= 2


# TTL이 만료된 키가 자동으로 삭제되는지 테스트한다.
def test_expiration():
    redis = MiniRedis()

    redis.set("name", "Alice")
    assert redis.expire("name", 0) is True

    assert redis.get("name") is None
    assert redis.exists("name") is False
    assert redis.ttl("name") == -2


# TTL이 없는 키의 TTL이 -1인지 테스트한다.
def test_no_ttl():
    redis = MiniRedis()

    redis.set("name", "Alice")

    assert redis.ttl("name") == -1


# 존재하지 않는 키의 TTL이 -2인지 테스트한다.
def test_missing_ttl():
    redis = MiniRedis()

    assert redis.ttl("unknown") == -2


# SET으로 값을 덮어쓰면 기존 TTL이 제거되는지 테스트한다.
def test_overwrite_clears_ttl():
    redis = MiniRedis()

    redis.set("name", "Alice")
    redis.expire("name", 30)

    assert redis.ttl("name") > 0

    redis.set("name", "Bob")

    assert redis.get("name") == "Bob"
    assert redis.ttl("name") == -1


# UTF-8 기준 메모리 사용량을 테스트한다.
def test_memory_usage():
    redis = MiniRedis()

    redis.set("name", "Alice")

    info = redis.memory_info()

    expected = len("name".encode("utf-8"))
    expected += len("Alice".encode("utf-8"))

    assert info.used_memory == expected


# 단일 데이터가 maxmemory보다 크면 저장하지 않는지 테스트한다.
def test_single_entry_oom():
    redis = MiniRedis()

    redis.set_maxmemory(5)

    assert redis.set("name", "Alice") is False
    assert redis.dbsize() == 0


# LRU eviction이 정상적으로 동작하는지 테스트한다.
def test_lru_eviction():
    redis = MiniRedis()

    redis.set_maxmemory(10)

    redis.set("a", "1234")
    redis.set("b", "1234")

    assert redis.exists("a") is True
    assert redis.exists("b") is True

    redis.get("a")

    redis.set("c", "1234")

    assert redis.exists("a") is True
    assert redis.exists("c") is True
    assert redis.exists("b") is False

    info = redis.memory_info()

    assert info.evicted_keys == 1


# 모든 MiniRedis 코어 테스트를 실행한다.
def main():
    test_set_get()
    test_missing_key()
    test_overwrite()
    test_delete()
    test_expire()
    test_expiration()
    test_no_ttl()
    test_missing_ttl()
    test_overwrite_clears_ttl()
    test_memory_usage()
    test_single_entry_oom()
    test_lru_eviction()

    print("MiniRedis 코어 테스트 통과!")


# 테스트 파일을 직접 실행했을 때 전체 테스트를 시작한다.
if __name__ == "__main__":
    main()