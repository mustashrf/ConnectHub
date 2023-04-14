from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import PostForm
from profiles.models import Profile
from .forms import PostForm, CommentForm
from django.views.generic import UpdateView, DeleteView

# Create your views here.
def main_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    post_form = PostForm()
    comment_form = CommentForm()
    post_added = False

    if 'submit_post_form' in request.POST:
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            ''' 
            when commit=False, the form data will not be saved to the database immediately.
            Instead, an instance of the model will be returned,
            which allows performing additional operations or validations on the instance
            before saving it to the database manually using the save() method
            '''
            instance = post_form.save(commit=False)
            instance.author = profile
            instance.save()
            # restart the form
            post_form = PostForm()
            post_added = True

    elif 'submit_comment_form' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            comment_form = CommentForm()

    context = {
        'posts': posts,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added,
    }
    return render(request, 'posts/main.html', context)

def like_unlike_post(reuqest):
    user = reuqest.user
    if reuqest.method == 'POST':
        post_id = reuqest.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                print('yes')
                like.value == 'Unlike'
            else:
                like.value == 'Like'
        else:
            like.value = 'Like'

        post.save()
        like.save()

    return redirect('posts:main-view')

class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/confirm_del.html"
    success_url = reverse_lazy('posts:main-view')

    def get_object(self, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if post.author.user != self.request.user:
            messages.warning(self.request, 'In order to proceed with this action, you need to be the author of the post')
        print(messages)
        return post

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'In order to proceed with this action, you need to be the author of the post')
            return super().form_invalid(form)

