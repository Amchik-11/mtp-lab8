"""Подсчёт оставшихся страниц и модель книги."""


def remaining_pages(total: int, read: int) -> int:
    """Посчитать страницы, оставшиеся до конца книги."""
    if type(total) is not int or type(read) is not int:
        raise TypeError("Число страниц должно быть целым.")
    if total <= 0 or not 0 <= read <= total:
        raise ValueError("Число прочитанных страниц должно быть от нуля до объёма книги.")
    return total - read


class BookProgress:
    def __init__(self, title: str, total_pages: int, pages_read: int = 0):
        if not title.strip():
            raise ValueError("Укажите название книги.")
        self.title = title.strip()
        self._total_pages = total_pages
        self.pages_read = pages_read

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @property
    def pages_read(self) -> int:
        return self._pages_read

    @pages_read.setter
    def pages_read(self, value: int) -> None:
        remaining_pages(self.total_pages, value)
        self._pages_read = value

    @property
    def remaining(self) -> int:
        return remaining_pages(self.total_pages, self.pages_read)
