class Context:
    def __init__(self) -> None:
        self.__container: dict[str, str] = {}

    def __getitem__(self, key) -> str:
        return self.__container[str(key)]

    def __setitem__(self, key, value) -> None:
        self.__container[str(key)] = str(value)

    def get_container(self) -> dict[str, str]:
        return self.__container

    def set_type(self, type: str) -> None:
        self.__container['__type'] = type

    def get_type(self) -> str:
        return self.__container['__type']

    def get_state(self) -> str:
        return self.__container['__state']

    def set_state(self, id: str) -> None:
        self.__container['__state'] = id

    def clear(self) -> None:
        self.__container = {}

    def is_empty(self) -> bool:
        return len(self.__container) <= 0
