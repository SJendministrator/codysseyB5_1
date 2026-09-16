from mini_redis.hashmap import HashMap


# HashMap의 기본 동작을 테스트한다.
def test_basic_operations():
    hashmap = HashMap()

    hashmap.put("name", "Alice")
    hashmap.put("age", "22")

    assert hashmap.get("name") == "Alice"
    assert hashmap.get("age") == "22"
    assert hashmap.get("unknown") is None

    assert hashmap.contains("name") is True
    assert hashmap.contains("unknown") is False

    assert hashmap.size() == 2


# 같은 키를 다시 저장하면 값을 수정하는지 테스트한다.
def test_update():
    hashmap = HashMap()

    hashmap.put("name", "Alice")
    hashmap.put("name", "Bob")

    assert hashmap.get("name") == "Bob"
    assert hashmap.size() == 1


# 항목 삭제가 정상적으로 동작하는지 테스트한다.
def test_remove():
    hashmap = HashMap()

    hashmap.put("name", "Alice")

    assert hashmap.remove("name") == "Alice"
    assert hashmap.get("name") is None
    assert hashmap.contains("name") is False
    assert hashmap.size() == 0

    assert hashmap.remove("unknown") is None


# 여러 키를 저장하고 keys()가 모든 키를 반환하는지 테스트한다.
def test_keys():
    hashmap = HashMap()

    hashmap.put("name", "Alice")
    hashmap.put("age", "22")
    hashmap.put("city", "Seoul")

    keys = list(hashmap.keys())

    assert len(keys) == 3
    assert "name" in keys
    assert "age" in keys
    assert "city" in keys

# 많은 데이터를 넣어 자동 리사이즈가 발생하는지 테스트한다.
def test_resize():
    hashmap = HashMap(initial_capacity=4)

    for number in range(20):
        hashmap.put(f"key{number}", f"value{number}")

    assert hashmap.size() == 20

    for number in range(20):
        assert hashmap.get(f"key{number}") == f"value{number}"


# HashMap의 전체 테스트를 실행한다.
def main():
    test_basic_operations()
    test_update()
    test_remove()
    test_keys()
    test_resize()

    print("HashMap 테스트 통과!")


# 테스트 파일을 직접 실행했을 때 테스트를 시작한다.
if __name__ == "__main__":
    main()