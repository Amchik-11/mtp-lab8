"""Отчёт о прочитанных и оставшихся страницах."""

import argparse
import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory

from .reading_lists import CsvReadingRepository, load_reading_lists


def report(paths: list[Path]) -> None:
    groups = asyncio.run(load_reading_lists(*(CsvReadingRepository(path) for path in paths)))
    total = 0
    for path, books in zip(paths, groups):
        print(f"\n{path.stem}")
        for book in books:
            print(f"  {book.title}: {book.pages_read}/{book.total_pages} стр.")
            total += book.remaining
    print(f"\nОсталось прочитать: {total} стр.")


def demo() -> None:
    with TemporaryDirectory() as folder:
        novels = Path(folder) / "Художественное.csv"
        notes = Path(folder) / "На выходные.csv"
        novels.write_text("title,total,read\nДва капитана,640,180\nТри товарища,360,360\n", encoding="utf-8")
        notes.write_text("title,total,read\nМаленький принц,96,42\n", encoding="utf-8")
        report([novels, notes])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="*", type=Path, help="CSV со столбцами title,total,read")
    args = parser.parse_args()
    try:
        if args.sources:
            report(args.sources)
        else:
            demo()
    except (OSError, ValueError) as error:
        parser.exit(1, f"Ошибка: {error}\n")


if __name__ == "__main__":
    main()
