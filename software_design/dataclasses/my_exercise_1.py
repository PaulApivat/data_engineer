from dataclasses import dataclass, field


@dataclass
class A:
    _length: int = field(init=False)

    def __post_init__(self) -> None:
        self._length = 0


@dataclass(slots=True)
class B:
    x: int
    y: str = "hello"
    l: list[int] = field(default_factory=list)


@dataclass
class C:
    a: int = 3
    b: int = field(init=False)

    def __post_init__(self) -> None:
        self.b = self.a + 3
