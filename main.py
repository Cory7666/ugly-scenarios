from scenario import scenario_repository
from context import Context
from bot_call import bot_calls
import traceback
from type_manipulation import type_check, type_cast


def call_bot_function(function_name: str, context: Context) -> None:
    if function_name in bot_calls.keys():
        bot_calls[function_name](context)
    else:
        print(f"Функция {function_name} не существует. Обнуление контекста.")
        context.clear()


def choose_and_run_next_state(user_input: str, state: dict[str, str | dict | list], context: Context) -> None:
    if 'next' in state.keys() and len(state['next']) > 0:
        if 'var_name' in state.keys():
            if 'type' in state.keys():
                if type_check[state['type']](user_input):
                    context[state['var_name']
                            ] = type_cast[state['type']](user_input)
                else:
                    print(
                        f"Полученная строка не соответствует требуемому типу ({state['type']}).")
                    return
            else:
                context[state['var_name']] = user_input

        for next_state_variant in state['next']:
            if 'if' in next_state_variant.keys():
                if bool(eval(next_state_variant['if'], context.get_container())):
                    run_state(
                        scenario_repository[next_state_variant['id']], context)
                    break
            else:
                run_state(
                    scenario_repository[next_state_variant['id']], context)
                break
    else:
        context.clear()


def run_state(state: dict[str, str | dict | list], context: Context) -> None:
    context.set_state(state['id'])
    if 'call' in state.keys():
        if 'require' in state.keys():
            for require in state['require']:
                if require not in context.get_container().keys():
                    print(
                        f"Состояние {state['id']} не может быть запущено, так как в контексте отсутствует параметр {require}.")
                    context.clear()
                    break
            else:
                call_bot_function(state['call'], context)
        else:
            call_bot_function(state['call'], context)
    elif 'message' in state.keys():
        print(state['message'])

    if 'next' not in state.keys() or len(state['next']) <= 0:
        context.clear()
    elif 'var_name' not in state.keys():
        # Перейти к следующему состоянию, так как в текущем от пользователя не требуется ввод.
        choose_and_run_next_state("", state, context)


def main() -> None:
    context = Context()
    user_input = ''
    while user_input != 'exit':
        try:
            print("> ", end='')
            user_input = input().strip()
            user_input_lower = user_input.lower()

            if len(user_input_lower) == 0 or user_input_lower == 'exit':
                continue
            elif context.is_empty():
                try:
                    begin_state = scenario_repository[user_input_lower]
                    if 'is_start_state' in begin_state.keys() and bool(begin_state['is_start_state']):
                        context.set_type(begin_state['id'])
                        run_state(begin_state, context)
                    else:
                        print("Невозможно начать выполнение с данного сценария.")
                except KeyError:
                    print(f'Сценарий с именем {user_input_lower} не найден.')
                    context.clear()
            else:
                choose_and_run_next_state(
                    user_input, scenario_repository[context.get_state()], context)

        except EOFError:
            print()
            user_input = "exit"
        except KeyboardInterrupt:
            print()
            user_input = ""
        except Exception:
            print(traceback.format_exc())
            context.clear()
    print("Bye!")


main()
