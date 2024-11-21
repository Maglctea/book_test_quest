from django.contrib import admin

from book.models import Book, ExportBooksTask


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ...


@admin.register(ExportBooksTask)
class ExportBooksTaskAdmin(admin.ModelAdmin):
    ...
