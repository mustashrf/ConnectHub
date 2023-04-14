from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, related_name='likes', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return str(self.content[:20])

    @property
    def likes_num(self):
        return self.liked.all().count()

    @property
    def comments_num(self):
        return self.comments.all().count()

    class Meta:
        # order posts, newest in the top
        ordering = ('-created',)

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)
class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.post}-{self.value}'
    