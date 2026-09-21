# Mini Redis

Python 3.8 이상에서 실행하는, 메모리 안에서 동작하는 Redis 스타일의
Key-Value CLI입니다. `dict`, `set`, `collections`로 캐시를 대체하지 않고
체이닝 해시맵, 이중 연결 리스트, 최소 힙을 직접 조합해 String 명령어,
LRU 메모리 제거, TTL 만료 처리를 구현합니다.

## 실행

```bash
python -m mini_redis
```

`exit` 또는 `quit`을 입력하면 종료합니다. 값에 공백이 있다면 큰따옴표로
감싸 입력할 수 있습니다.

```text
mini-redis> SET user:1 "Alice Kim"
OK
mini-redis> EXPIRE user:1 30
(integer) 1
mini-redis> TTL user:1
(integer) 29
mini-redis> GET user:1
"Alice Kim"
```

## 지원 명령어

| 명령어 | 설명 |
| --- | --- |
| `SET key value` | 값을 저장하고 기존 TTL을 제거합니다. |
| `GET key` | 값을 조회하고 성공한 조회를 LRU 최신 상태로 만듭니다. |
| `DEL key` / `EXISTS key` | 키를 삭제하거나 존재 여부를 반환합니다. |
| `DBSIZE` / `KEYS` | 현재 키 개수 또는 모든 키를 반환합니다. |
| `CONFIG SET maxmemory bytes` | 최대 메모리를 바이트 단위로 설정합니다. `0`은 무제한입니다. |
| `INFO memory` | `used_memory`, `maxmemory`, `evicted_keys`를 출력합니다. |
| `EXPIRE key seconds` / `TTL key` | 만료 시간을 설정하거나 남은 초를 반환합니다. |

## 내부 구조와 동작

- **`HashMap`**: 문자열을 31 기반 해시 함수로 계산하고, 같은 버킷에
  들어온 항목은 `DoublyLinkedList`로 체이닝합니다. 로드 팩터가 0.75를
  넘으면 버킷 수를 두 배로 확장합니다.
- **LRU**: 키별 LRU 노드를 별도 해시맵에 보관하고, 이중 연결 리스트의
  앞은 가장 최근 사용(MRU), 뒤는 가장 오래 사용(LRU)으로 유지합니다.
  따라서 조회 후 앞으로 이동, 오래된 키 제거 모두 O(1)입니다.
- **TTL**: 최소 힙에는 `(expire_at, key)`를 넣습니다. 명령 실행 전에
  힙의 루트부터 만료 항목을 정리하므로 가장 이른 만료 시간을 빠르게
  찾습니다. TTL을 재설정하거나 키를 삭제한 뒤 남은 힙 항목은 실제
  엔트리의 만료 시간과 비교해 무시하는 lazy deletion 방식입니다.
- **메모리**: `used_memory`는 모든 키와 값의 UTF-8 바이트 길이 합입니다.
  `SET` 뒤 제한을 초과하면 LRU 키부터 제한 이하가 될 때까지 제거하고,
  하나의 키-값 쌍 자체가 제한보다 크면 저장하지 않고 OOM 오류를
  반환합니다.

## 테스트

```bash
pytest -q
```

테스트는 각 자료구조의 기본 동작과 리사이즈, 명령 파싱, TTL, UTF-8
메모리 산정, LRU 제거를 검증합니다.
