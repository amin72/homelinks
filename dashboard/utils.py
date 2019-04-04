from itertools import chain
from links.models import Website, Channel, Group, Instagram


def get_sorted_users_links(user):
    websites = Website.objects.filter(author=user, parent=None)
    channels = Channel.objects.filter(author=user, parent=None)
    groups = Group.objects.filter(author=user, parent=None)
    instagrams = Instagram.objects.filter(author=user, parent=None)

    sorted_links = sorted(chain(websites, channels, groups, instagrams),
        key=lambda link: link.updated, reverse=True)

    return sorted_links


def replace_child_with_parent(links: list):
    # if links have child, sent their child instead of them.
    links_and_children = []
    for link in links:
        child = link.child
        if child:
            links_and_children.append(child)
        else:
            links_and_children.append(link)

    return links_and_children
