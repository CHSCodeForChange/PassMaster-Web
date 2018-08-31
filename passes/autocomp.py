from dal import autocomplete
from django.db.models import Q

from .models import Teacher


class TeacherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Teacher.objects.none()

        qs = Teacher.objects.all()

        if self.q:
            query = Q(profile__user__username__contains=self.q)
            qs = qs.filter(query)

        return qs