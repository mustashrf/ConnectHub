from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .utils import get_random_code

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio', max_length=350)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%y')}"

    def save(self, *args, **kwargs):
        exist = False
        if self.first_name and self.last_name:
            slug = slugify(str(self.first_name) + ' ' + str(self.last_name))

            # if this slug is already exist, then create another one using UUID
            exist = Profile.objects.filter(slug=slug).exists()
            while exist:
                slug = slugify(slug + ' ' + get_random_code())
                exist = Profile.objects.filter(slug=slug).exists()
        else:
            slug = str(self.user)
        
        self.slug = slug
        super().save(*args, **kwargs)

    def get_friends(self):
        return self.friends.all()

    def get_posts(self):
        return self.posts.all()

    @property
    def friends_num(self):
        return self.friends.all().count()

    @property
    def posts_num(self):
        return self.posts.all().count()

    @property
    def likes_given_num(self):
        likes = self.like_set.all()
        total = 0
        for like in likes:
            if like.value == 'Like':
                total += 1
        return total

    @property
    def likes_recieved_num(self):
        posts = self.posts.all()
        total = 0
        for post in posts:
            total += post.likes_num
        return total
        '''from posts.models import Like
        likes = Like.objects.filter(post__author=self, value='Like')
        return likes.count()'''

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'
    