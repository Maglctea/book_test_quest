import csv
import os
from datetime import datetime
from time import sleep

from django.conf import settings
from django.db.models import QuerySet

from book.models import ExportBooksTask, Book


class ExportBookTaskWorker:
    def __init__(self, batch_size_task: int = 10, batch_size_books: int = 30):
        self.batch_size_task = batch_size_task
        self.batch_size_books = batch_size_books

    def run(self):
        while True:
            tasks: QuerySet[ExportBooksTask] = ExportBooksTask.objects.filter(status=ExportBooksTask.TaskStatus.READY).order_by('created_at')[:self.batch_size_task]

            if not tasks:
                sleep(5)
                continue

            for task in tasks:
                task.status = ExportBooksTask.TaskStatus.IN_PROGRESS
                task.save()

                try:
                    filepath: str = self.build_file(self.make_file_path(task.pk), export_time=task.created_at)
                except Exception as e:
                    print(f'Error: {e}')
                    task.status = ExportBooksTask.TaskStatus.FAILED
                    task.save()
                    continue

                task.filepath = filepath
                task.status = ExportBooksTask.TaskStatus.COMPLETED
                task.save()

    def build_file(self, filepath: str, export_time: datetime) -> str:
        with open(filepath, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Title', 'Description', 'Price'])

            offset: int = 0
            total_books: int = Book.objects.filter(created_at__lte=export_time).count()
            while offset < total_books:
                # Исправленный срез
                books: QuerySet[Book] = Book.objects.filter(created_at__lte=export_time)[offset:offset + self.batch_size_books]

                for book in books:
                    writer.writerow([book.title, book.description, book.price])

                offset += self.batch_size_books
        return filepath

    def make_file_path(self, task_id: int) -> str:
        return os.path.join(settings.MEDIA_ROOT, 'csv', f'{task_id}.csv')
