from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image


class Post(models.Model):
    field_type = models.TextChoices('field_type', 'Technology, Entairnment')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.CharField(choices=field_type.choices, max_length=20)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    about_blog = models.CharField(max_length=500)
    starting_image = models.ImageField(upload_to='profile_pics')
    image_description = models.CharField(blank = True, max_length=300)
    main_content = models.TextField()
    about_you = models.TextField()
    votes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.starting_image.path)
        q = img.resize((700,450))
        q.save(self.starting_image.path)

    def get_absolute_url(self):
        return reverse('post-detail' , kwargs={'slug': self.slug})


class PostDetail(models.Model):
    p_title = models.ForeignKey(Post, on_delete=models.CASCADE)
    topic_heading = models.CharField(blank=True, max_length=200)
    content = models.TextField(blank=True)
    url_title = models.CharField(blank=True, max_length=500)
    urls_links = models.URLField(blank=True, max_length=500)
    image = models.ImageField(blank=True, null = True, upload_to='profile_pics')
    
    def __str__(self):
        return self.topic_heading
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            q = img.resize((700,450))
            q.save(self.image.path)

    def get_absolute_url(self):
        return reverse('post-detail' , kwargs={'slug': slugify(self.p_title)})

class AddingComment(models.Model):
    c_title = models.ForeignKey(Post, on_delete=models.CASCADE)
    C_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('post-detail' , kwargs={'slug': slugify(self.c_title)})


class Suggestion(models.Model):
    s_author = models.ForeignKey(User, on_delete=models.CASCADE)
    suggest = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.s_author.username} Suggestion'

    def get_absolute_url(self):
        return reverse('blog_home')

class Bookmark(models.Model):
    b_title = models.ForeignKey(Post, on_delete=models.CASCADE)
    b_author = models.ForeignKey(User, on_delete=models.CASCADE)
    bookmark = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.bookmark}'
    