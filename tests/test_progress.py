"""Проверки модели чтения и загрузки нескольких файлов."""

import asyncio

import pytest

from reading_plan.progress import BookProgress, remaining_pages
from reading_plan.reading_lists import CsvReadingRepository, load_reading_lists


@pytest.mark.parametrize("total,read,expected", [(100, 20, 80), (40, 40, 0), (40, 0, 40)])
def test_remaining_pages(total, read, expected):
    assert remaining_pages(total, read) == expected


def test_invalid_update_preserves_progress():
    book = BookProgress("Маленький принц", 96, 42)
    book.pages_read = 50
    with pytest.raises(ValueError):
        book.pages_read = 97
    assert (book.pages_read, book.remaining) == (50, 46)


def test_reads_independent_lists(tmp_path):
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"
    first.write_text("title,total,read\nПовесть,120,90\n", encoding="utf-8")
    second.write_text("title,total,read\nРоман,500,0\n", encoding="utf-8-sig")
    groups = asyncio.run(load_reading_lists(CsvReadingRepository(first), CsvReadingRepository(second)))
    assert [[(book.title, book.remaining) for book in books] for books in groups] == [
        [("Повесть", 30)], [("Роман", 500)],
    ]
