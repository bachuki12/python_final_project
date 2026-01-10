import time


class SafeExecutor:
    @staticmethod
    def run(func, *, delay=1.1):
        try:
            return func()
        except Exception as e:
            print(e)
            time.sleep(delay)
            return None
