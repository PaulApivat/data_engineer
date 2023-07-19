# ---- Add Type Hints to functions -----

def headline(text: str, align: bool = True) -> str:
    if align:
        return f"{text.title()}\n{'-' * len(text)}"
    else:
        return f" {text.title()} ".center(50, "o")

print(headline("python type checking"))

print(headline("python type chekcing", align=False))

# this code should not run, because align param should be bool
# to catch this you nneed a static type checker
#print(headline("python type chekcing", align="center"))

print(headline("python type chekcing", align=True))


# ------- Annotations ----------------

import math

def circumference(radius: float) -> float:
    return 2 * math.pi * radius 

print(circumference(1.23))

print(circumference.__annotations__)

# ---- Mypy interpreting type hints ----

#reveal_type(math.pi)
#radius = 1
#circumference = 2 * math.pi * radius
#reveal_locals()

# ---- Variable Annotations ---------

#pi: float = 3.142

#def circumference(radius: float) -> float:
#    return 2 * math.pi * radius 

#print(circumference(1))

#print(__annotations__)

# --------Type Comments: specify each argument on separate line with own annotation -------

def headline_2(
    text,           # type: str
    width=80,       # type: int
    fill_char="-",  # type: str
):                  # type: (...) -> str
    return f" {text.title()} ".center(width, fill_char)

print(headline_2("type comments work", width=40))