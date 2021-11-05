from django.template import Library

register = Library()

@register.filter
def sent_notifications(notifications):
    return notifications.filter(sent=True).order_by('-created_at')

@register.filter
def get_posts(posts):
    return posts.filter(belong_to=None).count()