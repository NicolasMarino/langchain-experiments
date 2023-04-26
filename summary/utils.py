import time
from rich.console import Console

console = Console()

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        console.print(f"Execution time for {func.__name__}: {execution_time:.6f} seconds \n")
        return result
    return wrapper
