from django.utils import timezone
from datetime import timedelta
from main.models import BookView

def get_last_n_days_data(model, n, user=None, book=None):
    startdate = timezone.now() - timedelta(days=n)
    filters = {
        "created_at__gte": startdate
    }
    if user:
        filters["user"] = user
    
    if book:
        filters["book"] = book

    return model.objects.filter(**filters)

def year_specific_data(model, year, user=None, book=None):
    filters = {
        "created_at__year": year
    }
    if user:
        filters["author"] = user
    
    if book:
        filters["book"] = book

    return model.objects.filter(**filters)

def log_book_view(book, user=None):
    BookView.objects.create(book=book, user=user)
    book.views = BookView.objects.filter(book=book).count()
    book.save()

def create_notification(user, message):
    from .models import Notification
    Notification.objects.create(
        user=user,
        content=message
    )
