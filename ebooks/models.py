from django.db import models
from django.core.validators import FileExtensionValidator
from books.models import Book


def ebook_directory_path(instance, filename):
    return f'ebooks/{instance.book.title.replace(" ", "_")}/{filename}'


class Ebook(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    txt_book = models.FileField(blank=True, null=True, upload_to=ebook_directory_path,
                                validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    pdf_book = models.FileField(blank=True, null=True, upload_to=ebook_directory_path,
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    download_count = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f'Ebook: {self.book.title}, {self.book.author}'
