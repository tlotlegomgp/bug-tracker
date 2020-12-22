from django.shortcuts import get_object_or_404
from .models import DirectMessage, Alert
from account.models import Profile

def profile_processor(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = get_object_or_404(Profile, user = user)
        user_messages = DirectMessage.objects.filter(receiver = user_profile).order_by('-created_on')[:5]
        user_alerts = Alert.objects.filter(user = user_profile).order_by('-created_on')[:5]
        return {'profile': user_profile, 'direct_messages': user_messages, 'alerts': user_alerts}
    else:
        return{}