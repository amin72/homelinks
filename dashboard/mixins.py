
class UserMixIn:
    """
    A mixin to only filter user's links
    """
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
