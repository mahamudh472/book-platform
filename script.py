from accounts.models import UserProfile, UserFollow, User
from main.utils import get_last_n_days_data

obj = UserFollow.objects.all().first()
user = User.objects.get(username='admin')

data =get_last_n_days_data(model=UserFollow, user=user, n=28)
print(data.count())
