"""Чтение списков через Repository и их одновременная загрузка."""

import asyncio
import csv
from pathlib import Path
from typing import Protocol

from .progress import BookProgress


class ReadingRepository(Protocol):
    def list_books(self) -> list[BookProgress]: ...


class CsvReadingRepository:
    def __init__(self, path: Path):
        self.path = path

    def list_books(self) -> list[BookProgress]:
        books = []
        with self.path.open(encoding="utf-8-sig", newline="") as source:
            rows = csv.DictReader(source)
            if not {"title", "total", "read"}.issubset(rows.fieldnames or ()):
                raise ValueError(f"{self.path}: нужны колонки title,total,read.")
            for row in rows:
                try:
                    books.append(BookProgress(row["title"] or "", int(row["total"]), int(row["read"])))
                except (TypeError, ValueError) as error:
                    raise ValueError(f"{self.path}, строка {rows.line_num}: {error}") from error
        return books


async def load_reading_lists(*repositories: ReadingRepository) -> list[list[BookProgress]]:
    """Читать разные списки параллельно и сохранить порядок аргументов."""
    jobs = (asyncio.to_thread(repository.list_books) for repository in repositories)
    return await asyncio.gather(*jobs)
