from django.shortcuts import render
from .models import Profile
from .forms import ProfileModelForm

# Create your views here.
def user_profile_view(request, slug):
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
    return render(request, 'profiles_app/user_profile.html', context)
