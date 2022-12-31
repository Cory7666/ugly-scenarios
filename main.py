import json
from bot_call import bot_calls


def find_state_by_name(name: str, scenario: list[dict]):
    return list(filter(lambda x: x['id'] == name, scenario['state_container']))[0]


def find_scenario_by_name(name: str, scenario: list) -> dict[str, str | list]:
    return list(filter(lambda x: x['id'] == name, scenario['scenario_container']))


def execute_simple_command(state_name: str, scenario: list[dict], context: dict[str, str]) -> None:
    state = find_state_by_name(state_name, scenario)
    if state.get('message', None) != None:
        print(state['message'])

    for require in state.get('require', []):
        if require == 'url' and 'url' not in context.keys():
            context['url'] = 'localhost'
        elif require == 'data' and 'data' not in context.keys():
            with open("./schedule.json", "r", encoding='utf-8') as file:
                context['data'] = json.load(file)

    if state.get('execute', None) != None:
        exec_result = eval(state['execute'], context)
        if state.get('value_name', None) != None:
            context[state['value_name']] = exec_result
        print(f"Exec Result: {exec_result}")
    elif state.get('call', None) != None:
        bot_calls[state['call']](context)


def execute_states(states: list[str | dict], scenario: list[dict], context: dict[str, str]) -> None:
    for state in states:
        if isinstance(state, str):
            execute_simple_command(state, scenario, context)
        elif isinstance(state, dict):
            if bool(eval(state['if-statement'], context)):
                if state.get('then-sequence', None) != None:
                    execute_states(state['then-sequence'], scenario, context)
            else:
                if state.get('else-sequence', None) != None:
                    execute_states(state['else-sequence'], scenario, context)


def main() -> None:
    with open("./scenario.json", "r", encoding='utf-8') as file:
        scenario = json.load(file)
        print('Сценарии загружены!')

    context: dict[str, str] = {}
    user_input = ''
    while user_input != 'exit':
        try:
            print("> ", end='')
            user_input = input().strip().lower()

            if len(user_input) > 0:
                result = find_scenario_by_name(user_input, scenario)

                if len(result) <= 0:
                    # Inner system commands
                    if user_input == 'scenario.update':
                        with open("./scenario.json", "r", encoding='utf-8') as file:
                            scenario = json.load(file)
                        print('Сценарии обновлены.')

                    elif user_input == 'scenario.list' or user_input == 'list':
                        scenarios_list = list(
                            map(lambda x: x['id'], scenario['scenario_container']))
                        scenarios_list.append('scenario.update')
                        scenarios_list.append('scenario.list')
                        scenarios_list.append('exit')

                        for s in sorted(scenarios_list):
                            print(s)

                    elif user_input == 'exit':
                        continue

                    else:
                        print("Сценарий не найден.")

                elif len(result) > 1:
                    print(
                        f"Найдено похожих сценариев: ${len(result)}. Устраните неоднозначность.")
                else:
                    execute_states(
                        result[0]['states_sequence'], scenario, context)

        except EOFError:
            print()
            user_input = "exit"
        except KeyboardInterrupt:
            print()
            user_input = ""
        except Exception as ex:
            print(type(ex), ex)
    print("Bye!")


main()
