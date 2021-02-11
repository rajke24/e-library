from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import BookReservation, BookInstance, BookRental
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=BookRental)
def update_bookinstance_status(sender, instance, created, **kwargs):
    if created:
        book = BookInstance.objects.get(pk=instance.book.id)
        book.status = "ON_LOAN"
        book.save()
        try:
            bookReservation = BookReservation.objects.get(
                book=instance.book.id)
            bookReservation.delete()
        except ObjectDoesNotExist:
            pass


@receiver(pre_save, sender=BookRental)
def update_bookinstance_on_rental_change(sender, instance, **kwargs):
    if instance.on_loan_end is not None:
        previous_book_rental = BookRental.objects.get(pk=instance.id)
        if previous_book_rental.on_loan_end != instance.on_loan_end:
            book = BookInstance.objects.get(pk=instance.book.id)
            book.status = "AVAILABLE"
            book.save()


@receiver(post_save, sender=BookReservation)
def update_bookinstance_on_reservation_create(sender, instance, created, **kwargs):
    if created:
        book = BookInstance.objects.get(pk=instance.book.id)
        book.status = "RESERVED"
        book.save()