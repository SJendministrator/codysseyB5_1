import shlex

from .core import MiniRedis


# Mini Redis 명령을 처리하고 Redis 스타일의 결과 문자열을 반환한다.
class CommandHandler:
    # Mini Redis 코어 객체를 전달받아 명령 처리기를 초기화한다.
    def __init__(self, redis):
        self.redis = redis

    # 입력된 명령 문자열을 따옴표를 고려하여 토큰으로 분리한다.
    def _parse(self, line):
        try:
            return shlex.split(line)
        except ValueError:
            raise ValueError("ERR syntax error")

    # 명령어가 올바른 개수의 인자를 사용하는지 확인한다.
    def _check_args(self, parts, minimum, maximum=None):
        argument_count = len(parts) - 1

        if argument_count < minimum:
            return False

        if maximum is not None and argument_count > maximum:
            return False

        return True

    # 정수 인자를 Redis 스타일로 변환한다.
    def _parse_integer(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValueError(
                "ERR value is not an integer or out of range"
            )

    # SET 명령을 처리한다.
    def _set(self, parts):
        if not self._check_args(parts, 2, 2):
            return (
                "(error) ERR wrong number of arguments "
                "for 'set' command"
            )

        key = parts[1]
        value = parts[2]

        if not self.redis.set(key, value):
            return (
                "(error) OOM command not allowed when "
                "used_memory > 'maxmemory'"
            )

        return "OK"

    # GET 명령을 처리한다.
    def _get(self, parts):
        if not self._check_args(parts, 1, 1):
            return (
                "(error) ERR wrong number of arguments "
                "for 'get' command"
            )

        value = self.redis.get(parts[1])

        if value is None:
            return "(nil)"

        return f'"{value}"'

    # DEL 명령을 처리한다.
    def _delete(self, parts):
        if not self._check_args(parts, 1, 1):
            return (
                "(error) ERR wrong number of arguments "
                "for 'del' command"
            )

        deleted = self.redis.delete(parts[1])

        return f"(integer) {1 if deleted else 0}"

    # EXISTS 명령을 처리한다.
    def _exists(self, parts):
        if not self._check_args(parts, 1, 1):
            return (
                "(error) ERR wrong number of arguments "
                "for 'exists' command"
            )

        exists = self.redis.exists(parts[1])

        return f"(integer) {1 if exists else 0}"

    # DBSIZE 명령을 처리한다.
    def _dbsize(self, parts):
        if not self._check_args(parts, 0, 0):
            return (
                "(error) ERR wrong number of arguments "
                "for 'dbsize' command"
            )

        return f"(integer) {self.redis.dbsize()}"

    # KEYS 명령을 처리한다.
    def _keys(self, parts):
        if not self._check_args(parts, 0, 0):
            return (
                "(error) ERR wrong number of arguments "
                "for 'keys' command"
            )

        keys = list(self.redis.keys())

        if not keys:
            return "(empty array)"

        lines = []

        for index, key in enumerate(keys, start=1):
            lines.append(f'{index}. "{key}"')

        return "\n".join(lines)

    # CONFIG SET 명령을 처리한다.
    def _config(self, parts):
        if not self._check_args(parts, 3, 3):
            return (
                "(error) ERR wrong number of arguments "
                "for 'config' command"
            )

        if parts[1].lower() != "set":
            return (
                "(error) ERR unknown subcommand "
                f"'{parts[1].lower()}'"
            )

        if parts[2].lower() != "maxmemory":
            return (
                "(error) ERR unknown option "
                f"'{parts[2]}'"
            )

        try:
            maxmemory = self._parse_integer(parts[3])
        except ValueError as error:
            return f"(error) {error}"

        if maxmemory < 0:
            return (
                "(error) ERR maxmemory must be "
                "greater than or equal to 0"
            )

        self.redis.set_maxmemory(maxmemory)

        return "OK"

    # INFO memory 명령을 처리한다.
    def _info(self, parts):
        if not self._check_args(parts, 1, 1):
            return (
                "(error) ERR wrong number of arguments "
                "for 'info' command"
            )

        if parts[1].lower() != "memory":
            return (
                "(error) ERR unknown section "
                f"'{parts[1]}'"
            )

        info = self.redis.memory_info()

        return (
            f"used_memory:{info.used_memory}\n"
            f"maxmemory:{info.maxmemory}\n"
            f"evicted_keys:{info.evicted_keys}"
        )

    # EXPIRE 명령을 처리한다.
    def _expire(self, parts):
        if not self._check_args(parts, 2, 2):
            return (
                "(error) ERR wrong number of arguments "
                "for 'expire' command"
            )

        try:
            seconds = self._parse_integer(parts[2])
        except ValueError as error:
            return f"(error) {error}"

        result = self.redis.expire(parts[1], seconds)

        return f"(integer) {1 if result else 0}"

    # TTL 명령을 처리한다.
    def _ttl(self, parts):
        if not self._check_args(parts, 1, 1):
            return (
                "(error) ERR wrong number of arguments "
                "for 'ttl' command"
            )

        return f"(integer) {self.redis.ttl(parts[1])}"

    # 하나의 명령 문자열을 실행하고 결과를 반환한다.
    def execute(self, line):
        parts = self._parse(line)

        if not parts:
            return ""

        command = parts[0].lower()

        if command == "set":
            return self._set(parts)

        if command == "get":
            return self._get(parts)

        if command == "del":
            return self._delete(parts)

        if command == "exists":
            return self._exists(parts)

        if command == "dbsize":
            return self._dbsize(parts)

        if command == "keys":
            return self._keys(parts)

        if command == "config":
            return self._config(parts)

        if command == "info":
            return self._info(parts)

        if command == "expire":
            return self._expire(parts)

        if command == "ttl":
            return self._ttl(parts)

        return f"(error) ERR unknown command '{command}'"