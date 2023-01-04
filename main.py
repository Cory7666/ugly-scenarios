from scenario import scenario_repository
from context import Context
from bot_call import bot_calls
import traceback


def choose_and_run_next_state(user_input: str, state: dict[str, str | dict | list], context: Context) -> None:
    if 'next' in state.keys() and len(state['next']) > 0:

        if 'var_name' in state.keys():
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
                bot_calls[state['call']](context)
        else:
            bot_calls[state['call']](context)
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
            user_input = input().strip().lower()

            if len(user_input) == 0 or user_input == 'exit':
                continue
            elif context.is_empty():
                try:
                    begin_state = scenario_repository[user_input]
                    context.set_type(user_input)
                    run_state(begin_state, context)
                except KeyError:
                    print(f'Сценарий с именем {user_input} не найден.')
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
