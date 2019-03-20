
class UserMixIn:
    """
    A mixin to only filter user's links
    `model` property must be set in sub class.
    """
    model = None

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, parent=None)
