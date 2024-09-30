from django.core.mail import send_mail


def send_notification(user, message):
    send_mail(
        "Auction Notification",
        message,
        "from@gmail.com",
        [user.email],
        fail_silently=True
    )