from package_1.file_1 import file_1_function
from package_1.file_1 import file_1_function2

R = 10


def some_function(x: int) -> None:
    print(x)
    print("original type-x ", type(x))


def main():
    new_var = "int"
    some_function(new_var)
    print(type(new_var))
    file_1_function()
    file_1_function2()


if __name__ == "__main__":
    main()
