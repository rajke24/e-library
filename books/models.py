from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import datetime


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    image = models.ImageField(default='book_default.jpg', upload_to='books_pics')
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def get_enabled_star(self):
        return range(int(self.rating))

    def get_disabled_star(self):
        disabled_star = 5 - int(self.rating)
        if float(int(self.rating)) - self.rating != 0.0:
            disabled_star = 4 - int(self.rating)

        return range(disabled_star)

    def is_half_star_active(self):
        return True if float(int(self.rating)) - self.rating != 0.0 else False


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    class LoanStatus(models.TextChoices):
        MAINTENANCE = 'MAINTENANCE', _('Maintenance')
        ONLOAN = 'ON_LOAN', _('On loan')
        AVAILABLE = 'AVAILABLE', _('Available')
        RESERVED = 'RESERVED', _('Reserved')

    status = models.CharField(choices=LoanStatus.choices, default=LoanStatus.AVAILABLE, blank=True,
                              help_text='Book availability', max_length=11)

    class Meta:
        ordering = ["created_date"]

    def __str__(self):
        return F'{self.id}: {self.book.title}'


class BookRental(models.Model):
    book = models.ForeignKey(BookInstance, on_delete=models.CASCADE)
    on_loan_start = models.DateField(auto_now_add=True)
    on_loan_duration = models.IntegerField(
        default=1, null=False, help_text="Months")
    on_loan_end = models.DateField(null=True, blank=True)
    booker = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-on_loan_start"]

    def __str__(self):
        return '%s (%s, %s)' % (self.id, self.book.book.title, self.booker.username)

    def get_due_date(self):
        return self.on_loan_start + datetime.timedelta(weeks=4 * self.on_loan_duration)

    def get_cost(self):
        due_date = self.get_due_date()
        if datetime.datetime.today().date() > due_date:
            return (datetime.datetime.today().date() - due_date).days * 2.53
        else:
            return 0

    def get_days_expired(self):
        due_date = self.get_due_date()
        if (datetime.datetime.today().date() - due_date).days > 0:
            return (datetime.datetime.today().date() - due_date).days
        else:
            return 0


class BookReservation(models.Model):
    book = models.OneToOneField(BookInstance, on_delete=models.CASCADE)
    reservation_date = models.DateField(auto_now_add=True)
    booker = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["reservation_date"]

    def __str__(self):
        return '%s (%s, %s)' % (self.id, self.book.book.title, self.booker.username)


class Opinion(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='opinions')
    rating = models.IntegerField(default=5)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Opinion: {self.title}, by {self.author.username}'
