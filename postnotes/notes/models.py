from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=200)


class Note(models.Model):
    note_text = models.CharField(max_length=10000)
    create_date = models.DateTimeField('date created')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
