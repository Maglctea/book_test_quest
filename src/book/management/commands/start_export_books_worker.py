# your_app/management/commands/your_command.py
from django.core.management.base import BaseCommand

from book.workers import ExportBookTaskWorker


class Command(BaseCommand):
    help = 'Starting a worker to process file export tasks '

    def add_arguments(self, parser):
        parser.add_argument('tasks_limit', type=int, default=10, help='Count tasks to process in batch')
        parser.add_argument('books_limit', type=int, default=30, help='Count books to process in batch')

    def handle(self, *args, **kwargs):
        tasks_limit: int = kwargs['tasks_limit']
        books_limit: int = kwargs['books_limit']
        worker = ExportBookTaskWorker(tasks_limit, books_limit)
        print('START WORKER...')
        worker.run()
