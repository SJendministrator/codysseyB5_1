from mini_redis.commands import CommandHandler
from mini_redis.core import MiniRedis


# 명령 처리기를 새 Mini Redis와 함께 생성한다.
def create_handler():
    redis = MiniRedis()
    return CommandHandler(redis)


# SET과 GET 명령을 테스트한다.
def test_set_get():
    handler = create_handler()

    assert handler.execute("SET name Alice") == "OK"
    assert handler.execute("GET name") == '"Alice"'


# 존재하지 않는 키의 조회 결과를 테스트한다.
def test_missing_get():
    handler = create_handler()

    assert handler.execute("GET unknown") == "(nil)"


# EXISTS와 DEL 명령을 테스트한다.
def test_exists_delete():
    handler = create_handler()

    handler.execute("SET name Alice")

    assert handler.execute("EXISTS name") == "(integer) 1"
    assert handler.execute("DEL name") == "(integer) 1"
    assert handler.execute("EXISTS name") == "(integer) 0"
    assert handler.execute("DEL name") == "(integer) 0"


# DBSIZE와 KEYS 명령을 테스트한다.
def test_dbsize_keys():
    handler = create_handler()

    assert handler.execute("DBSIZE") == "(integer) 0"
    assert handler.execute("KEYS") == "(empty array)"

    handler.execute("SET name Alice")
    handler.execute("SET city Seoul")

    assert handler.execute("DBSIZE") == "(integer) 2"

    keys = handler.execute("KEYS")

    assert '"name"' in keys
    assert '"city"' in keys


# CONFIG SET과 INFO memory를 테스트한다.
def test_memory_commands():
    handler = create_handler()

    assert handler.execute("CONFIG SET maxmemory 100") == "OK"

    result = handler.execute("INFO memory")

    assert "used_memory:" in result
    assert "maxmemory:100" in result
    assert "evicted_keys:0" in result


# EXPIRE와 TTL 명령을 테스트한다.
def test_ttl_commands():
    handler = create_handler()

    handler.execute("SET name Alice")

    assert handler.execute("EXPIRE name 30") == "(integer) 1"

    ttl = int(
        handler.execute("TTL name").split()[-1]
    )

    assert 0 <= ttl <= 30


# 존재하지 않는 키의 EXPIRE와 TTL을 테스트한다.
def test_missing_ttl():
    handler = create_handler()

    assert handler.execute("EXPIRE unknown 30") == "(integer) 0"
    assert handler.execute("TTL unknown") == "(integer) -2"


# TTL이 없는 키의 TTL을 테스트한다.
def test_no_ttl():
    handler = create_handler()

    handler.execute("SET name Alice")

    assert handler.execute("TTL name") == "(integer) -1"


# 잘못된 명령과 인자 개수를 테스트한다.
def test_errors():
    handler = create_handler()

    assert (
        handler.execute("UNKNOWN")
        == "(error) ERR unknown command 'unknown'"
    )

    assert (
        handler.execute("GET")
        == "(error) ERR wrong number of arguments "
        "for 'get' command"
    )

    assert (
        handler.execute("SET name")
        == "(error) ERR wrong number of arguments "
        "for 'set' command"
    )


# 정수가 필요한 명령의 잘못된 입력을 테스트한다.
def test_integer_error():
    handler = create_handler()

    result = handler.execute(
        "CONFIG SET maxmemory abc"
    )

    assert (
        result
        == "(error) ERR value is not an integer or out of range"
    )


# 공백을 포함한 따옴표 문자열을 테스트한다.
def test_quoted_value():
    handler = create_handler()

    assert (
        handler.execute(
            'SET message "Hello World"'
        )
        == "OK"
    )

    assert (
        handler.execute("GET message")
        == '"Hello World"'
    )


# 모든 명령 처리 테스트를 실행한다.
def main():
    test_set_get()
    test_missing_get()
    test_exists_delete()
    test_dbsize_keys()
    test_memory_commands()
    test_ttl_commands()
    test_missing_ttl()
    test_no_ttl()
    test_errors()
    test_integer_error()
    test_quoted_value()

    print("CommandHandler 테스트 통과!")


# 테스트 파일을 직접 실행했을 때 테스트를 시작한다.
if __name__ == "__main__":
    main()