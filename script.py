# from accounts.models import UserProfile, UserFollow, User
# from main.utils import get_last_n_days_data

# obj = UserFollow.objects.all().first()
# user = User.objects.get(username='admin')

# data =get_last_n_days_data(model=UserFollow, user=user, n=28)
# print(data.count())

import uuid
from main.models import Book

books = list(Book.objects.all())

new_books = [
    Book(title=f"{book.title} {uuid.uuid4().hex[:4]}", author=book.author, description=book.description, content=book.content, category=book.category, thumbnail=book.thumbnail)
    for book in books for _ in range(10)
]
print(len(new_books))
Book.objects.bulk_create(new_books)
