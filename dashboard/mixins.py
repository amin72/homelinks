from rest_framework.generics import ListAPIView
from dashboard import utils


class UserMixIn:
    """
    A mixin to only filter user's links
    `model` property must be set in sub class.
    """
    model = None

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, parent=None)


class ReplaceChildWithParent:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        links = context.get('object_list')
        object_list = utils.replace_child_with_parent(links)
        context['object_list'] = object_list
        return context


class ReplaceChildWithParentMixIn(ListAPIView):
    """
    Replace child with parent object if child parent has child.
    `model` attribute must be set in sub classes.
    """
    model = None

    def get_queryset(self):
        queryset = self.model.objects.filter(author=self.request.user,
            parent=None)
        result = utils.replace_child_with_parent(queryset)
        return result
