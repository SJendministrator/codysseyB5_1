from mini_redis.heap import MinHeap


# 정수 값을 넣고 최소값 순서로 꺼내지는지 테스트한다.
def test_integer_heap():
    heap = MinHeap()

    heap.push(50)
    heap.push(10)
    heap.push(30)
    heap.push(5)
    heap.push(20)

    assert heap.peek() == 5
    assert heap.size() == 5

    assert heap.pop() == 5
    assert heap.pop() == 10
    assert heap.pop() == 20
    assert heap.pop() == 30
    assert heap.pop() == 50

    assert heap.pop() is None
    assert heap.size() == 0


# TTL 형태의 (만료 시간, 키) 데이터를 최소 만료 시간 순서로 처리하는지 테스트한다.
def test_ttl_heap():
    heap = MinHeap()

    heap.push((300, "city"))
    heap.push((100, "name"))
    heap.push((200, "age"))
    heap.push((50, "token"))

    assert heap.peek() == (50, "token")

    assert heap.pop() == (50, "token")
    assert heap.pop() == (100, "name")
    assert heap.pop() == (200, "age")
    assert heap.pop() == (300, "city")


# 같은 만료 시간에서 키를 기준으로 안정적으로 비교할 수 있는지 테스트한다.
def test_same_expiration_time():
    heap = MinHeap()

    heap.push((100, "banana"))
    heap.push((100, "apple"))
    heap.push((100, "melon"))

    assert heap.pop() == (100, "apple")
    assert heap.pop() == (100, "banana")
    assert heap.pop() == (100, "melon")


# 빈 힙의 동작을 테스트한다.
def test_empty_heap():
    heap = MinHeap()

    assert heap.peek() is None
    assert heap.pop() is None
    assert heap.size() == 0


# 모든 MinHeap 테스트를 실행한다.
def main():
    test_integer_heap()
    test_ttl_heap()
    test_same_expiration_time()
    test_empty_heap()

    print("MinHeap 테스트 통과!")


# 테스트 파일을 직접 실행했을 때 테스트를 시작한다.
if __name__ == "__main__":
    main()