import json
from sevsu import SchedulePage
import time


def main() -> None:
    with open("./schedule.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    with open("./scenario.json", "r", encoding='utf-8') as file:
        scenario = json.load(file)

    user_input = ''
    while user_input != 'exit':
        try:
            print("> ", end='')
            user_input = input().strip().lower()

            if len(user_input) > 0:
                result = list(filter(lambda x: x['id'] == user_input,
                                     scenario['scenario_container']))

                if len(result) <= 0:
                    # Inner system commands
                    if user_input == 'scenario.update':
                        with open("./scenario.json", "r", encoding='utf-8') as file:
                            scenario = json.load(file)
                        print('Сценарии обновлены.')
                    else:
                        print("Сценарий не найден.")
                elif len(result) > 1:
                    print(
                        f"Найдено похожих сценариев: ${len(result)}. Устраните неоднозначность.")
                else:
                    result = result[0]
                    for state_name in result['states_sequence']:
                        state = list(
                            filter(lambda x: x['id'] == state_name, scenario['state_container']))[0]
                        if state.get('message', None) != None:
                            print(state['message'])

                        for require in state.get('require', []):
                            if require == 'url' and globals().get('url', None) == None:
                                globals()['url'] = 'localhost'

                        if state.get('execute', None) != None:
                            exec_result = eval(state['execute'])
                            print(f"Exec Result: {exec_result}")
        except EOFError:
            print()
            user_input = "exit"
        except Exception as ex:
            print(ex)
    print("Bye!")


main()
