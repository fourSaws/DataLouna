from datetime import datetime, timedelta

from LounaAdmin.onetimeMailing import one_timeMailing
from LounaAdmin.models import NoviceNewsTellers, User


def NewsTellersCron():
    notifications = NoviceNewsTellers.objects.all()
    for notification in notifications:
        users = list(
            i["chat_id"]
            for i in User.objects.filter(
                registration_date=datetime.today().date() - timedelta(days=notification.after_time)
            ).values('chat_id')
        )
        notification_title = notification.title
        notification_text = notification.text
        one_timeMailing(title=notification_title, text=notification_text, users=users)
