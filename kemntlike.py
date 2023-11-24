from django.contrib.contenttypes.models import ContentType
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='post/picture/', null=True, blank=True)
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=False)
    publish_date = models.DateField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    # categories = models.ManyToManyField(Category, related_name='categories_post')
    # page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_posts')

    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title



class PostLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=((1, 'Like'), (-1, 'Dislike')))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)
