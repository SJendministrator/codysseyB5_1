from .commands import CommandHandler
from .core import MiniRedis


# Mini Redis REPL을 실행하고 사용자의 명령을 반복해서 처리한다.
def run():
    redis = MiniRedis()
    handler = CommandHandler(redis)

    while True:
        try:
            line = input("mini-redis> ")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break

        if line.strip().lower() in ("exit", "quit"):
            break

        try:
            result = handler.execute(line)
        except ValueError as error:
            result = f"(error) {error}"
        except Exception:
            result = "(error) internal error"

        if result:
            print(result)

    return 0