from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=200)
    draft = models.BooleanField(default=True)
    comments_enable = models.BooleanField(default=False, 
                                          verbose_name="Comments")
    body = models.TextField()
    pub_date = models.DateTimeField(verbose_name="Time stamp")
    
    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    name = models.CharField(max_length=200)
    body = models.TextField()
    hide = models.BooleanField()
    pub_date = models.DateTimeField(verbose_name="Time stamp")
    
    def __unicode__(self):
        return self.name
