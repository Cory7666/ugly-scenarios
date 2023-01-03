class Context:
    def __init__(self) -> None:
        self.__container: dict[str, str] = {}

    def __getitem__(self, key) -> str:
        return self.__container[str(key)]

    def __setitem__(self, key, value) -> None:
        self.__container[str(key)] = str(value)

    def set_type(self, type: str) -> None:
        self.__container['__type__'] = type

    def get_type(self) -> str:
        return self.__container['__type__']
    
    def get_state(self) -> str:
        return self.__container['__state__']
    
    def set_state(self, id: str) -> None:
        self.__container['__state__'] = id

    def clear(self) -> None:
        self.__container = {}

    def is_empty(self) -> bool:
        return len(self.__container) <= 0
