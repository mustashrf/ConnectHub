from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from .utils import get_random_code
from django.db.models import Q

# Create your models here.

class ProfileManager(models.Manager):

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_available_invitations(self, sender):
        all_profiles = self.get_all_profiles(sender)
        my_profile = Profile.objects.get(user=sender)

        my_friends = my_profile.get_friends().values_list('id', flat=True)
        sent_invitations = Relationship.objects.get_sent_invitations(my_profile)
        received_invitations = Relationship.objects.get_received_invitations(my_profile)

        available_profiles = all_profiles.exclude(
            Q(pk__in=my_friends) |
            Q(user__in=sent_invitations) |
            Q(user__in=received_invitations)
        )
        return available_profiles

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio', max_length=350)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField('self', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    initial_first_name = None
    initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_first_name = self.first_name
        self.initial_last_name = self.last_name

    def __str__(self):
        return f"{self.slug}"

    def get_absolute_url(self):
        return reverse("profiles:user-profile-view", kwargs={"slug": self.slug})
    

    def save(self, *args, **kwargs):

        self.first_name = self.user.first_name
        self.last_name = self.user.last_name

        exist = False
        slug = self.slug
        if self.first_name != self.initial_first_name or self.last_name != self.initial_last_name or self.slug == '':
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
    ('accept', 'accept'),
    ('remove', 'remove'),
)

class RelationshipManager(models.Manager):
    def get_my_invitations(self, receiver):
        invitations = Relationship.objects.filter(receiver=receiver, status='send')
        return invitations
    
    def get_sent_invitations(self, me):
        sent_invitations_pks = Relationship.objects.filter(
            sender=me, status='send'
        ).values_list('receiver__user', flat=True)
        sent_invitations = User.objects.filter(pk__in=sent_invitations_pks)

        return sent_invitations

    def get_received_invitations(self, me):
        received_invitations_pks = Relationship.objects.filter(
            receiver=me, status='send'
        ).values_list('sender__user', flat=True)
        received_invitations = User.objects.filter(pk__in=received_invitations_pks)

        return received_invitations

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f'{self.sender}-{self.receiver}-{self.status}'
