from rest_framework import serializers

from book.models import Book, ExportBooksTask


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ExportBooksTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportBooksTask
        exclude = ('filepath',)

