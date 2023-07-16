def bar(x = None):
    if x is None:
        x = []
    x.append(34)
    return x

my_var = [1]
print(bar(my_var))
print(bar([3]))

# ------- context manager -----------
from contextlib import contextmanager

@contextmanager
def logging():
    print("logging the results")
    yield 200
    print("All done!")

with logging() as log:
    print(f"The results are {log}")


# change number
def change_number(z):
    z = z * 0.1
    return z
    
var = 32
print(change_number(320))