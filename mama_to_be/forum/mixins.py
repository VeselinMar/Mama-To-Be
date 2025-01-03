class CreatedByMixin:
    @property
    def created_by_username(self):
        return self.created_by.profile.username
