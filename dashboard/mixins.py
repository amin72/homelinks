
class UserMixIn:
    """
    A mixin to only filter user's posts
    """
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
