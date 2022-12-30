class Context:
    def __init__(self) -> None:
        self.__container: dict[str, str] = {}

    def __getitem__(self, key) -> str:
        return self.__container[str(key)]

    def __setitem__(self, key, value) -> None:
        self.__container[str(key)] = str(value)
