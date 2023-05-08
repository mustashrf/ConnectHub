from django.shortcuts import render, redirect
from .models import Profile, Relationship
from django.contrib.auth.models import User
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/user_profile.html"
    context_object_name = 'profile'

    def get_object(self):
        slug = self.kwargs['slug']
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        
        profile = Profile.objects.get(user=user)
        sent_invitations = Relationship.objects.get_sent_invitations(profile)
        received_invitations = Relationship.objects.get_received_invitations(profile)
        friends = profile.get_friends()
        posts = self.get_object().get_posts()

        context['this_user'] = self.request.user
        context['sent_invitations'] = sent_invitations
        context['received_invitations'] = received_invitations
        context['friends'] = [i.user for i in friends]
        context['posts'] = posts
        context['posts_exist'] = True if len(posts)!=0 else False

        return context

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "profiles/profiles_list.html"
    context_object_name = 'profiles'

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        friends = set(profile.get_friends())
        sent_invitations = set(Relationship.objects.get_sent_invitations(profile))
        received_invitations = set(Relationship.objects.get_received_invitations(profile))
        return friends - sent_invitations - received_invitations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        
        profile = Profile.objects.get(user=user)
        sent_invitations = Relationship.objects.get_sent_invitations(profile)
        received_invitations = Relationship.objects.get_received_invitations(profile)
        friends = profile.get_friends()

        context['sent_invitations'] = sent_invitations
        context['received_invitations'] = received_invitations
        context['friends'] = [i.user for i in friends]
        context['is_empty'] = True if len(self.get_queryset())==0 else False

        return context

@login_required
def user_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    # if there is no POST data, None is passed - if there are no uploaded files None is passed
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/my_profile.html', context)

@login_required
def received_invitations_view(request):
    profile = Profile.objects.get(user=request.user)
    invitations = Relationship.objects.get_my_invitations(receiver=profile)
    invitations = [i.sender for i in invitations]
    is_empty = True if len(invitations)==0 else False
    context = {'invitations': invitations, 'is_empty': is_empty}
    return render(request, 'profiles/invitations.html', context)

@login_required
def available_invitations_view(request):
    user = request.user
    availables = Profile.objects.get_available_invitations(user)
    context = {'profiles': availables}
    return render(request, 'profiles/profiles_list.html', context)

@login_required
def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        other_profile = Profile.objects.get(pk=pk)
        this_profile = Profile.objects.get(user=request.user)

        relation = Relationship.objects.get(
                ((Q(sender=other_profile) & Q(receiver=this_profile)) | (Q(sender=this_profile) & Q(receiver=other_profile)))
                , status='accept'
            )
        relation.status='remove'
        relation.save()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('posts: main-view')

@login_required
def add_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        other_profile = Profile.objects.get(pk=pk)
        this_profile = Profile.objects.get(user=request.user)

        relation = Relationship.objects.get(sender=other_profile, receiver=this_profile, status='send')
        relation.status='accept'
        relation.save()

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('posts: main-view')

@login_required
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)
        
        _ = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
    
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('posts: main-view')

@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        
        _ = Relationship.objects.get(sender=sender, receiver=receiver, status='send').delete()
    
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('posts: main-view')

@login_required
def ignore_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(user=request.user)
        receiver = Profile.objects.get(pk=pk)
        
        _ = Relationship.objects.get(sender=sender, receiver=receiver, status='send').delete()
    
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('posts: main-view')
