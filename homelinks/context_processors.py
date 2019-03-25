from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dashboard.models import Action
from links.models import Website, Channel, Group, Instagram

def object_counter(request):
    context = {}
    user = request.user
    if user.is_superuser or user.is_staff:
        recent_actions_count = Action.objects.filter(is_read=False).count()
        context['recent_actions_count'] = recent_actions_count

    if user.is_authenticated:
        websites_count = Website.objects.filter(author=user, parent=None).count()
        channels_count = Channel.objects.filter(author=user, parent=None).count()
        groups_count = Group.objects.filter(author=user, parent=None).count()
        instagrams_count = Instagram.objects.filter(author=user, parent=None).count()
        context['websites_count'] = websites_count
        context['channels_count'] = channels_count
        context['groups_count'] = groups_count
        context['instagrams_count'] = instagrams_count

    return context
