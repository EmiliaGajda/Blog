from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')

class Post(models.Model):

    title   = models.CharField(max_length=200)
    slug    = models.SlugField(max_length=200, unique_for_date='publish')
    author  = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body    = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)  #auto_now_add dodaje date a auto_now zmienia datę a ie dodaje kolejną
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Roboczy'),
        ('published', 'Opublikowany'),
    )
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])


# Create your models here.



