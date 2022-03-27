from django.db import models


# Create your models here.
class MadLib(models.Model):

    def __str__(self):
        return self.mad_lib_name

    mad_lib_name = models.CharField(max_length=200, unique=True)
    mad_lib_desc = models.CharField(max_length=200)
    story = models.TextField()


class WordList(models.Model):

    def __str__(self):
        name = str(self.mad_lib_id) + " " + str(self.id) + " " + str(self.word)
        return name

    mad_lib_id = models.ForeignKey(MadLib, models.CASCADE)
    word = models.CharField(max_length=50)
    position = models.PositiveSmallIntegerField()

