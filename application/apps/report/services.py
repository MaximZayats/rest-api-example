from datetime import datetime
from typing import Optional

# from models.tortoise import Task
from apps.core.models.tortoise import Task
from xlwt import Workbook, Worksheet
from xlwt.CompoundDoc import XlsDoc

REPORT_TIME_FORMAT = '%m/%d/%Y, %H:%M:%S'
REPORT_FILE_TIME_FORMAT = '%m-%d-%Y %H-%M-%S'


class _CustomXlsDoc(XlsDoc):
    def __init__(self,
                 book: Optional[Workbook] = None,
                 stream: Optional[bytes] = None):
        super().__init__()

        self.stream = stream or book.get_biff_data()  # type: ignore

        # Copied from original class
        self.padding = b'\x00' * (0x1000 - (len(self.stream) % 0x1000))
        self.book_stream_len = len(self.stream) + len(self.padding)

        self._build_directory()
        self._build_sat()
        self._build_header()

    def get_virtual_document(self) -> bytes:
        # Copied from `save` method
        bytes_ = bytes()

        bytes_ += self.header
        bytes_ += self.packed_MSAT_1st
        bytes_ += self.stream
        bytes_ += self.padding
        bytes_ += self.packed_MSAT_2nd
        bytes_ += self.packed_SAT
        bytes_ += self.dir_stream

        return bytes_


def _generate_report_title(sheet: Worksheet,
                           column: int = 0,
                           start_row: int = 0):
    sheet.write(column, start_row, 'Task Id')
    sheet.write(column, start_row + 1, 'Task Name')
    sheet.write(column, start_row + 2, 'Task Description')
    sheet.write(column, start_row + 3, 'Task Start Date')
    sheet.write(column, start_row + 4, 'Task End Date')
    sheet.write(column, start_row + 5, 'Task Element Id')
    sheet.write(column, start_row + 6, 'Task Element Name')
    sheet.write(column, start_row + 7, 'Task Element Description')


def generate_report_file_name() -> str:
    return f'Report from {datetime.now().strftime(REPORT_FILE_TIME_FORMAT)}.xlsx'


async def generate_report_content() -> bytes:
    tasks = await Task.all().prefetch_related('task_elements')

    book = Workbook()
    sheet: Worksheet = book.add_sheet('Report')

    _generate_report_title(sheet)

    current_row = 1

    for task in tasks:
        sheet.write(current_row, 0, task.pk)
        sheet.write(current_row, 1, task.name)
        sheet.write(current_row, 2, task.description)
        sheet.write(current_row, 3, task.start_date.strftime(REPORT_TIME_FORMAT))
        sheet.write(current_row, 4, task.end_date.strftime(REPORT_TIME_FORMAT))

        for task_element in task.task_elements:
            sheet.write(current_row, 5, task_element.pk)
            sheet.write(current_row, 6, task_element.name)
            sheet.write(current_row, 7, task_element.description)

            current_row += 1

        if not task.task_elements:
            current_row += 1

    doc = _CustomXlsDoc(book=book)

    return doc.get_virtual_document()
