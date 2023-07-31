from django.db import models
import random
import string




class codeVote (models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=1000, default=' ')
    is_voted = models.BooleanField(default=False)


