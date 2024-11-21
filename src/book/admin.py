from django.contrib import admin

from book.models import Book, ExportBooksTask


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'price', 'created_at')
    search_fields = ('title', 'description')


@admin.register(ExportBooksTask)
class ExportBooksTaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'status', 'created_at', 'updated_at')
    search_fields = ('pk',)
    list_filter  = ('status',)
