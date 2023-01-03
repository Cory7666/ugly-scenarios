from context import Context
from sevsu import SchedulePage
import time


def __print_schedule_link(context: Context) -> None:
    with open('./site.htm', 'r', encoding='utf-8') as file:
        link = SchedulePage(file).getLinkByPath(
            context['university'], context['semestre'], context['course'])
    print(f"Найдена ссылка: {link if link != None else '<not found>'}")


def __print_time(context: Context) -> None:
    print(f"Сейчас {time.asctime()}.")
    context.clear()


bot_calls = {
    'print_schedule_link': __print_schedule_link,
    'print_time': __print_time
}
