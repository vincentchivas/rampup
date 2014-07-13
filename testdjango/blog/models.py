from django.db import models

class  Users(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    def __unicode__(self):
	    return self.username

class Author(models.Model):
    authorname=models.CharField(max_length=50)
    authorage=models.IntegerField()

    def __unicode__(self):
        return self.authorname


class  Book(models.Model):
    title=models.CharField(max_length=50)
    authors=models.ManyToManyField(Author)
    content=models.CharField(max_length=1000)

    def __unicode__(self):
        return self.title


# Create your models here.
