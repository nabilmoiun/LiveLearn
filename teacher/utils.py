from django.contrib.auth import get_user_model

User = get_user_model()


def generate_class_link(user: User) -> str:
    return "https://www.meet.com/%s" % str(user.full_name)

