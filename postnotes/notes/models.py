from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200, default='')

    def __unicode__(self):
        if len(self.email) > 0:
            return 'User ' + self.email
        else:
            return 'User ' + str(self.id)


class Note(models.Model):
    note_text = models.CharField(max_length=10000)
    create_date = models.DateTimeField('date created')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return 'Note ' + str(self.id)

    def to_json(self):
        return {
            'note': self.note_text,
            'create_date': self.create_date,
            'id': self.id
        }
