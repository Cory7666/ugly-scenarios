from context import Context
from sevsu import SchedulePage
import time
from scenario import scenario_repository
import os


def __print_available_scenarios_list(context: Context) -> None:
    for key in sorted(scenario_repository):
        print(key, "(start)" if bool(scenario_repository[key].get(
            'is_start_state', False)) else "(general)")


def __update_scenarios_list(context: Context) -> None:
    prev_scen_count = len(scenario_repository.keys())
    scenario_repository.load()
    print(
        f"Обновлено. {prev_scen_count} -> {len(scenario_repository.keys())}.")


def __clear_screen(context: Context) -> None:
    os.system("clear || cls")


def __print_schedule_link(context: Context) -> None:
    with open('./site.htm', 'r', encoding='utf-8') as file:
        link = SchedulePage(file).getLinkByPath(
            context['university'], context['semestre'], context['course'])
    print(f"Найдена ссылка: {link if link != None else '<not found>'}")


def __print_time(context: Context) -> None:
    print(f"Сейчас {time.asctime()}.")


def __input_age(context: Context) -> None:
    print("Введите возраст.")


def __print_person_info(context: Context) -> None:
    if 'first_name' in context.get_container().keys():
        print(f"Имя: {context['first_name']}. Возраст: {context['age']}.")
    else:
        print(f"Возраст: {context['age']}.")


def __input_university_name_with_help(context: Context) -> None:
    print("Введите университет.")


def __print_schedule_link(context: Context) -> None:
    with open('./site.htm', 'r') as file:
        link = SchedulePage(file).getLinkByPath(
            university_name=context['university'], semestre_name=context['semestre'], course_name=context['course'])
        print("Ссылка не найдена." if link ==
              None else f"Найдена ссылка: {link}.")


bot_calls: dict[str, (Context)] = {
    'print_schedule_link': __print_schedule_link,
    'print_time': __print_time,
    'input_age': __input_age,
    'print_person_info': __print_person_info,
    'input.university_name_with_help': __input_university_name_with_help,
    'print_schedule_link': __print_schedule_link,

    'print_available_scenarios_list': __print_available_scenarios_list,
    'update_scenarios_list': __update_scenarios_list,
    'clear_screen': __clear_screen
}
