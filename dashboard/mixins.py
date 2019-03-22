
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

        object_list = []
        for object in context.get('object_list'):
            child = object.child
            if child:
                object_list.append(child)
            else:
                object_list.append(object)

        context['object_list'] = object_list
        return context
