from django.http import FileResponse
from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from book.models import Book, ExportBooksTask
from book.serializers import BookSerializer, ExportBooksTaskSerializer


class BookViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer: BookSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book, is_new = Book.objects.get_or_create(**serializer.data)

        data: dict = serializer.to_representation(book)
        headers: dict = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
def create_task(request):
    task: ExportBooksTask = ExportBooksTask.objects.create()
    return Response({'task_id': task.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_file(request, task_id: int):
    try:
        export_task: ExportBooksTask = ExportBooksTask.objects.get(id=task_id, status=ExportBooksTask.TaskStatus.COMPLETED)
    except ExportBooksTask.DoesNotExist:
        raise NotFound(detail="Task not found")

    filepath: str = export_task.filepath
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='books.cvs')


@api_view(['GET'])
def get_task_status(request, task_id: int):
    try:
        export_task: ExportBooksTask = ExportBooksTask.objects.get(id=task_id)
    except ExportBooksTask.DoesNotExist:
        raise NotFound(detail="Task not found")

    data: dict = ExportBooksTaskSerializer(export_task).data
    return Response(data, status=status.HTTP_200_OK)
