import bs4 as bs
import json

column_selector = '.schedule-table__column'
column_title_selector = '.schedule-table__column-header .schedule-table__column-name'
column_element_selector = '.document-accordion'
element_header_selector = 'h4'
doc_group_selector = '.document-link__group'
doc_group_title_selector = '.document-link__group-name'
docs_selector = 'a'

class SchedulePage:
    def __init__(self, doc: bs.BeautifulSoup) -> None:
        self.__doc = doc

    def getAsObject(self) -> list[
        dict[str, str | list[
            dict[str, str | list[
                dict[str, str | list[
                    dict[str, str]]]]]]]]:
        return [
            {
                'name': column.select_one(column_title_selector).text.strip(),
                'content': [
                    {
                        'name': column_element.select_one(element_header_selector).text.strip(),
                        'content': [
                            {
                                'name': doc_group.select_one(doc_group_title_selector).text.strip() if doc_group.select_one(doc_group_title_selector) != None else '',
                                'content': [
                                    {
                                        'name': doc.text.strip(),
                                        'link': doc.attrs['href']
                                    }
                                    for doc in doc_group.select(docs_selector)
                                ]
                            }
                            for doc_group in column_element.select(doc_group_selector)
                        ]
                    }
                    for column_element in column.select(column_element_selector)
                ]
            }
            for column in self.__doc.select(column_selector)
        ]

    def getAsJson(self) -> str:
        return json.dumps(self.getAsObject())
