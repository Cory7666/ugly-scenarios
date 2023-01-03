import json
from context import Context
from bot_call import bot_calls


def parse_scenario_file(obj: any) -> dict[str, dict[str, dict[str, str | list | dict]]]:
    return {
        'states_container': {
            x['id']: x for x in obj['states_container']
        }
    }


def main() -> None:
    with open("./scenario.json", "r", encoding='utf-8') as file:
        scenario = parse_scenario_file(json.load(file))
        print('Сценарии загружены!')

    context = Context()
    user_input = ''
    while user_input != 'exit':
        try:
            print("> ", end='')
            user_input = input().strip().lower()

            if context.is_empty():
                try:
                    begin_state = scenario['states_container'][user_input]
                    context.set_type(user_input)
                    context.set_state(begin_state['id'])
                    bot_calls[begin_state['call']](context)
                except KeyError:
                    print(f'Сценарий с именем {user_input} не найден.')
            else:
                pass

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
