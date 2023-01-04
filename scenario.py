import json


class __ScenarioRepository:
    def __init__(self) -> None:
        self.__container: dict[str, dict[str, str | dict | list]] = {}
        self.load()

    def __getitem__(self, key: str) -> dict[str, str | dict | list]:
        return self.__container['states_container'][key]

    def load(self) -> None:
        with open("./scenario.json", "r", encoding='utf-8') as file:
            self.__container = self.__parse_scenario_file(json.load(file))
            print('Сценарии загружены!')
    
    def keys(self):
        return self.__container['states_container'].keys()

    def __parse_scenario_file(self, obj: any) -> dict[str, dict[str, dict[str, str | list | dict]]]:
        return {
            'states_container': {
                x['id']: x for x in obj['states_container']
            }
        }


scenario_repository = __ScenarioRepository()
