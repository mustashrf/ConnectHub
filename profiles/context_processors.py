from .models import Profile, Relationship

def get_user_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'profile': profile}
    return {}

def get_invitations_num(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        invitations_num = Relationship.objects.get_my_invitations(profile).count()
        return {'invitations_num': invitations_num}
    return {}