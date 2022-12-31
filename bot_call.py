from sevsu import SchedulePage


def __print_schedule_link(context: dict[str, str]) -> None:
    with open('./site.htm', 'r', encoding='utf-8') as file:
        link = SchedulePage(file).getLinkByPath(
            context['university'], context['semestre'], context['course'])
    print(f"Найдена ссылка: {link if link != None else '<not found>'}")


bot_calls = {
    'print_schedule_link': __print_schedule_link
}
