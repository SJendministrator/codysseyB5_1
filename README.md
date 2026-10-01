# Mini Redis

Python으로 구현한 CLI 기반 Mini Redis 프로젝트입니다.

Redis의 핵심 동작 원리를 이해하기 위해 Python의 내장 `dict`, `set`, `collections` 등에 의존하지 않고 **해시맵, 이중 연결 리스트, 최소 힙을 직접 구현**합니다.

이를 기반으로 Redis의 기본적인 Key-Value 저장 기능과 LRU 메모리 관리, TTL 만료 관리를 구현하는 것을 목표로 합니다.

---

## 1. 프로젝트 소개

Redis는 메모리에 데이터를 저장하는 In-Memory Key-Value 데이터 저장소입니다.

빠른 데이터 접근을 위해 다양한 자료구조를 활용하며, 특히 Key-Value 데이터를 효율적으로 관리하고 메모리 사용량을 제어하기 위한 자료구조가 중요합니다.

이 프로젝트에서는 Redis의 핵심 기능을 단순히 사용하는 것이 아니라 내부 자료구조를 직접 구현하여 다음 개념을 학습합니다.

* 해시맵과 해시 함수
* 해시 충돌 해결과 체이닝
* 이중 연결 리스트
* LRU(Least Recently Used)
* 최소 힙
* TTL(Time To Live)
* 메모리 제한과 자동 제거
* CLI(REPL) 명령어 처리
* 명령어 파싱 및 실행

---

## 2. 프로젝트 목표

### 자료구조 직접 구현

Python의 내장 Key-Value 컬렉션을 사용하지 않고 다음 자료구조를 직접 구현합니다.

* HashMap
* Doubly Linked List
* Min Heap

### Redis 기능 구현

Redis의 기본적인 String 명령어를 CLI에서 사용할 수 있도록 구현합니다.

```text
SET
GET
DEL
EXISTS
DBSIZE
KEYS
EXPIRE
TTL
CONFIG SET maxmemory
INFO memory
```

### CLI 구현

사용자가 Redis와 비슷한 방식으로 명령어를 입력할 수 있는 REPL 환경을 구현합니다.

```text
mini-redis> SET name hello
OK
mini-redis> GET name
"hello"
```

---

## 3. 개발 환경

* Python 3.8 이상
* macOS / Linux 환경
* Git / GitHub

별도의 외부 라이브러리 없이 Python 기본 기능을 중심으로 구현합니다.

---

## 4. 프로젝트 구조

```text
codysseyB5_1/
├── mini_redis/
│   ├── ...
│   └── ...
├── test/
│   └── ...
├── README.md
└── .gitignore
```

자료구조와 CLI 기능은 역할에 따라 모듈을 분리하여 관리합니다.

---

## 5. 핵심 자료구조

### 5.1 HashMap

Key-Value 데이터를 저장하기 위한 자료구조입니다.

해시 함수를 이용하여 Key를 특정 버킷 위치로 변환하고, 동일한 버킷에 여러 Key가 저장되는 경우 체이닝 방식으로 충돌을 처리합니다.

기본적인 연산은 다음과 같습니다.

```text
put()
get()
remove()
contains()
keys()
size()
```

평균적으로 Key를 빠르게 찾을 수 있도록 구현하는 것이 목표입니다.

또한 저장된 데이터의 수가 증가하여 로드 팩터가 기준을 초과하면 버킷 크기를 확장합니다.

---

### 5.2 Doubly Linked List

각 노드가 이전 노드와 다음 노드를 가리키는 이중 연결 리스트를 사용합니다.

```text
prev ← [ Node ] → next
```

노드는 다음 정보를 가집니다.

```text
prev
next
data
```

주요 연산:

```text
insert_front()
insert_back()
remove_front()
remove_back()
remove_node()
move_to_front()
```

각 노드를 직접 알고 있는 경우 삽입, 삭제, 이동을 O(1)에 수행할 수 있도록 구현합니다.

---

### 5.3 Min Heap

TTL이 설정된 Key의 만료 시간을 관리하기 위해 최소 힙을 사용합니다.

힙에는 다음과 같은 형태의 데이터를 저장할 수 있습니다.

```text
(expire_at, key)
```

가장 만료 시간이 빠른 데이터가 Heap의 최상단에 위치하도록 합니다.

주요 연산:

```text
push()
pop()
peek()
size()
```

힙의 내부 정렬을 위해 다음 연산을 구현합니다.

```text
_heapify_up()
_heapify_down()
```

---

## 6. LRU 메모리 관리

LRU는 **Least Recently Used**의 약자로, 가장 오랫동안 사용되지 않은 데이터를 먼저 제거하는 방식입니다.

Mini Redis에서는 해시맵과 이중 연결 리스트를 조합하여 LRU를 관리합니다.

개념적으로 다음과 같은 구조를 사용합니다.

```text
HashMap
   │
   ├── key → List Node
   │
   ↓
Doubly Linked List

[가장 최근 사용]
       ↓
      A
      B
      C
       ↓
[가장 오래 사용되지 않음]
```

Key를 새로 저장하거나 성공적으로 조회하면 해당 Key를 리스트의 앞쪽으로 이동시킵니다.

메모리가 제한을 초과하면 리스트의 가장 뒤쪽에 있는 Key부터 제거합니다.

### LRU 동작 흐름

```text
SET / 성공적인 GET
        ↓
해당 Key 사용
        ↓
LRU 리스트의 맨 앞으로 이동
        ↓
used_memory 확인
        ↓
maxmemory 초과?
     ↓ YES
가장 오래 사용되지 않은 Key 제거
        ↓
used_memory 감소
        ↓
제한 이하가 될 때까지 반복
```

---

## 7. 메모리 관리

`CONFIG SET maxmemory` 명령을 이용하여 최대 메모리 사용량을 설정합니다.

```text
mini-redis> CONFIG SET maxmemory 100
OK
```

메모리 사용량은 다음 기준으로 계산합니다.

```text
used_memory
= Σ (UTF-8 Key의 바이트 길이 + UTF-8 Value의 바이트 길이)
```

자료구조 자체의 노드, 포인터, 버킷 등의 오버헤드는 계산하지 않습니다.

메모리 제한을 초과하면 LRU 정책에 따라 오래 사용되지 않은 Key부터 제거합니다.

---

## 8. INFO memory

현재 메모리 상태를 확인할 수 있습니다.

최소한 다음 정보를 출력합니다.

```text
used_memory
maxmemory
evicted_keys
```

예시:

```text
mini-redis> INFO memory
used_memory:22
maxmemory:30
evicted_keys:1
```

`evicted_keys`는 메모리 제한을 초과하여 LRU 방식으로 제거된 Key의 누적 개수입니다.

---

## 9. TTL 관리

TTL은 **Time To Live**의 약자로 Key가 얼마 동안 유지될 수 있는지를 나타냅니다.

`EXPIRE` 명령을 이용하여 Key에 만료 시간을 설정합니다.

```text
mini-redis> EXPIRE name 10
(integer) 1
```

`TTL` 명령을 이용하면 남은 시간을 확인할 수 있습니다.

```text
mini-redis> TTL name
(integer) 5
```

시간이 지나면 해당 Key는 만료되어 존재하지 않는 Key처럼 처리됩니다.

### TTL 상태

```text
-2
→ Key가 존재하지 않음

-1
→ Key는 존재하지만 TTL이 설정되지 않음

N
→ Key의 남은 만료 시간
```

### TTL 처리 흐름

```text
EXPIRE
  ↓
expire_at 계산
  ↓
Min Heap에 저장
  ↓
TTL 조회
  ↓
현재 시간과 expire_at 비교
  ↓
만료되었으면 Key 삭제
```

---

## 10. String 명령어

### SET

Key와 Value를 저장합니다.

```text
mini-redis> SET name hello
OK
```

기존 Key를 덮어쓰는 경우 기존 TTL은 초기화합니다.

---

### GET

Key의 값을 조회합니다.

```text
mini-redis> GET name
"hello"
```

존재하지 않는 Key는 다음과 같이 표시합니다.

```text
(nil)
```

GET에 성공하면 해당 Key의 LRU 사용 순서를 갱신합니다.

---

### DEL

Key를 삭제합니다.

```text
mini-redis> DEL name
(integer) 1
```

존재하지 않는 Key를 삭제하면:

```text
(integer) 0
```

Key를 삭제할 때는 데이터뿐만 아니라 LRU와 TTL 관련 정보도 함께 정리해야 합니다.

---

### EXISTS

Key의 존재 여부를 확인합니다.

```text
mini-redis> EXISTS name
(integer) 1
```

존재하지 않으면:

```text
(integer) 0
```

---

### DBSIZE

현재 저장된 Key의 개수를 반환합니다.

```text
mini-redis> DBSIZE
(integer) 1
```

---

### KEYS

현재 저장된 전체 Key를 출력합니다.

```text
mini-redis> KEYS
1. "name"
2. "age"
```

패턴 매칭은 구현하지 않습니다.

---

## 11. CLI

Mini Redis는 REPL 방식의 CLI를 제공합니다.

REPL은 사용자의 명령을 반복적으로 입력받고 즉시 실행 결과를 출력하는 구조입니다.

```text
mini-redis> SET name hello
OK
mini-redis> GET name
"hello"
mini-redis> EXISTS name
(integer) 1
mini-redis> DBSIZE
(integer) 1
mini-redis> KEYS
1. "name"
mini-redis> DEL name
(integer) 1
mini-redis> GET name
(nil)
```

CLI는 다음 과정을 반복합니다.

```text
입력
 ↓
명령어 파싱
 ↓
명령어 확인
 ↓
인자 확인
 ↓
해당 명령 실행
 ↓
결과 출력
 ↓
다음 명령 대기
```

`exit` 또는 `quit`을 입력하면 CLI를 종료합니다.

---

## 12. 명령어 파싱

사용자가 입력한 문자열을 명령어와 인자로 분리합니다.

예를 들어:

```text
SET name hello
```

를 입력하면 개념적으로 다음과 같이 분리됩니다.

```text
명령어
SET

인자
name
hello
```

이후 명령어에 맞는 실행 함수를 호출합니다.

따옴표가 포함된 Value도 처리할 수 있도록 입력 파싱을 구성합니다.

---

## 13. Redis 스타일 출력

명령 실행 결과는 Redis와 비슷한 형식으로 출력합니다.

```text
OK
(nil)
(integer) 1
(integer) 0
(error) ...
```

잘못된 명령어:

```text
(error) ERR unknown command 'HELLO'
```

인자 개수가 잘못된 경우:

```text
(error) ERR wrong number of arguments for 'GET' command
```

정수 변환에 실패한 경우:

```text
(error) ERR value is not an integer or out of range
```

메모리 부족으로 저장할 수 없는 경우:

```text
(error) OOM command not allowed when used_memory > 'maxmemory'
```

---

## 14. 자료구조 간 관계

이 프로젝트의 핵심은 각각의 자료구조를 따로 구현하는 것에서 끝나지 않고 서로 연결하여 Redis의 동작을 만드는 것입니다.

```text
                    Mini Redis
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       HashMap      LRU List      Min Heap
          │            │            │
          │            │            │
       Key-Value    사용 순서      TTL 만료
          │            │            │
          └────────────┼────────────┘
                       ↓
                    CLI 명령
```

### SET

```text
SET
 ↓
HashMap에 데이터 저장
 ↓
LRU 리스트에 추가/갱신
 ↓
TTL 정보 초기화
 ↓
used_memory 계산
 ↓
maxmemory 초과 시 LRU 제거
```

### GET

```text
GET
 ↓
TTL 만료 여부 확인
 ↓
HashMap에서 Key 조회
 ↓
값 반환
 ↓
성공했다면 LRU 갱신
```

### DEL

```text
DEL
 ↓
HashMap에서 삭제
 ↓
LRU 리스트에서 삭제
 ↓
TTL 정보 삭제
 ↓
used_memory 감소
```

### EXPIRE

```text
EXPIRE
 ↓
Key 존재 여부 확인
 ↓
expire_at 계산
 ↓
Min Heap에 저장
```

---

## 15. 실행 방법

프로젝트를 Clone한 후 프로젝트 디렉터리에서 실행합니다.

```bash
git clone https://github.com/SJendministrator/codysseyB5_1.git
cd codysseyB5_1
```

Mini Redis 실행:

```bash
python -m mini_redis
```

실행되면 다음과 같은 CLI가 나타납니다.

```text
mini-redis>
```

---

## 16. 테스트 예시

### 기본 명령 테스트

```text
mini-redis> SET name hello
OK

mini-redis> GET name
"hello"

mini-redis> EXISTS name
(integer) 1

mini-redis> DBSIZE
(integer) 1

mini-redis> KEYS
1. "name"

mini-redis> DEL name
(integer) 1

mini-redis> GET name
(nil)
```

### TTL 테스트

```text
mini-redis> SET name hello
OK

mini-redis> EXPIRE name 10
(integer) 1

mini-redis> TTL name
(integer) 5
```

시간이 지나 만료된 경우:

```text
mini-redis> GET name
(nil)

mini-redis> TTL name
(integer) -2
```

---

## 17. 테스트

`test/` 디렉터리에서 각 자료구조와 기능에 대한 테스트를 관리합니다.

주요 테스트 대상:

* Doubly Linked List
* HashMap
* Min Heap
* SET / GET
* DEL / EXISTS
* DBSIZE / KEYS
* EXPIRE / TTL
* Memory / LRU
* CLI 명령어 파싱
* 오류 처리

---

## 18. 제한 사항

학습 목적으로 다음 Python 내장 자료형 및 라이브러리의 사용을 제한합니다.

```text
dict
set
collections
```

내장 Key-Value 컬렉션으로 HashMap이나 LRU를 대체하지 않고 직접 자료구조를 구현합니다.

또한 다음 기능은 구현 범위에서 제외합니다.

* 네트워크 통신
* 데이터 영속성
* Redis List / Set / Sorted Set
* 멀티스레딩
* 동시성 제어
* 복잡한 Redis 프로토콜

---

## 19. 학습한 내용

이 프로젝트를 통해 다음 내용을 직접 구현하고 학습하는 것을 목표로 합니다.

* 해시 함수와 해시 충돌
* 체이닝
* 해시맵의 데이터 저장 및 검색
* 이중 연결 리스트
* O(1) 노드 이동 및 삭제
* HashMap + Linked List 기반 LRU
* 최소 힙
* TTL 만료 관리
* 메모리 제한과 자동 제거
* UTF-8 기반 메모리 계산
* CLI와 REPL
* 문자열 파싱
* 예외 처리
* 자료구조 간 결합
