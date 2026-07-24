from __future__ import annotations

from datetime import date
from pathlib import Path

from openpyxl import Workbook, load_workbook


class ExcelService:
    """Small replaceable persistence adapter for the MVP."""

    def __init__(self, path: Path | None = None) -> None:
        default = Path.home() / ".flashtile" / "FlashTile.xlsx"
        self.path = path or default
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._create()

    def _create(self) -> None:
        workbook = Workbook()
        progress = workbook.active
        progress.title = "Progress"
        progress.append(["date", "topic", "lesson", "xp"])
        settings = workbook.create_sheet("Settings")
        settings.append(["key", "value"])
        settings.append(["selected_topic", "AWS Cloud"])
        workbook.save(self.path)

    def selected_topic(self) -> str:
        workbook = load_workbook(self.path)
        for key, value in workbook["Settings"].iter_rows(min_row=2, values_only=True):
            if key == "selected_topic":
                return str(value)
        return "AWS Cloud"

    def set_selected_topic(self, topic: str) -> None:
        workbook = load_workbook(self.path)
        sheet = workbook["Settings"]
        for row in range(2, sheet.max_row + 1):
            if sheet.cell(row, 1).value == "selected_topic":
                sheet.cell(row, 2).value = topic
                break
        else:
            sheet.append(["selected_topic", topic])
        workbook.save(self.path)

    def complete(self, topic: str, lesson: str, xp: int) -> bool:
        workbook = load_workbook(self.path)
        sheet = workbook["Progress"]
        today = date.today().isoformat()
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] == today and row[1] == topic and row[2] == lesson:
                return False
        sheet.append([today, topic, lesson, xp])
        workbook.save(self.path)
        return True

    def totals(self) -> tuple[int, int]:
        workbook = load_workbook(self.path)
        rows = list(workbook["Progress"].iter_rows(min_row=2, values_only=True))
        xp = sum(int(row[3] or 0) for row in rows)
        unique_days = sorted({str(row[0]) for row in rows if row[0]}, reverse=True)
        streak = 0
        cursor = date.today()
        for value in unique_days:
            if value == cursor.isoformat():
                streak += 1
                cursor = date.fromordinal(cursor.toordinal() - 1)
            elif value < cursor.isoformat():
                break
        return xp, streak

