from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F

class Election(models.Model):
    KIND_SIMPLE = 0
    KIND_MULTI = 1
    KIND_PRIORITY_LIST = 2
    KIND_CHOICES = [
        (KIND_SIMPLE, 'simple'),
        (KIND_MULTI, 'multi'),
        (KIND_PRIORITY_LIST, 'priority_list'),
    ]

    title = models.CharField(max_length=140)
    kind = models.PositiveIntegerField(choices=KIND_CHOICES)

    def __str__(self):
        return self.title

    def vote(self, user, value):
        raise NotImplementedError

    def get_priorities(self, user):
        raise NotImplementedError

    def get_priorities_map(self):
        raise NotImplementedError


class Candidate(models.Model):

    election = models.ForeignKey(
        'Election',
        on_delete=models.CASCADE,
        related_name='candidates',
    )
    slug = models.CharField(max_length=20)
    display_name = models.CharField(max_length=140)

    def __str__(self):
        return self.display_name

    class Meta:
        unique_together = [('election', 'slug')]

class BaseVote(models.Model):
    election = models.ForeignKey(
        'Election',
        on_delete=models.CASCADE,
        related_name='votes',
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='votes',
    )
    candidate = models.ForeignKey(
        'Candidate',
        on_delete=models.CASCADE,
        related_name='votes',
    )

    def __str__(self):
        return self.election.title + " - " + self.value.value

class SimpleVote(BaseVote):

    def clean(self):
        if self.election.kind == 0:
            if Vote.objects.filter(user_id=self.user_id, election_id=self.election_id):
                raise ValidationError("Já votou")
            if self.candidate.election_id != self.election_id:
                raise ValidationError("Opção obscura não válida para votações ortodoxas")

class MultiVote(BaseVote):
    pass
