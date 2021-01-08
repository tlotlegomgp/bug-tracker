from operator import attrgetter
from django.shortcuts import get_object_or_404
from django.db.models import Q
from account.models import Profile
from .models import DirectMessage, Alert, Conversation
from .forms import ConversationForm


def profile_processor(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = get_object_or_404(Profile, user=user)
        unread_messages_count = DirectMessage.objects.filter(receiver=user_profile).filter(status='UNREAD').count()
        all_alerts = Alert.objects.filter(user=user_profile).filter(status='UNREAD').order_by('-created_on')[:30]
        user_alerts = all_alerts[:4]
        conversations = Conversation.objects.filter(Q(user_1=user_profile) | Q(user_2=user_profile))
        
        unsorted_messages = []
        conv_count = {}
        for conv in conversations:
            latest_message = DirectMessage.objects.filter(conversation = conv).order_by('-created_on').first()
            unsorted_messages.append(latest_message)
            conv_count[conv.slug] = DirectMessage.objects.filter(conversation = conv).filter(status='UNREAD').exclude(author = user_profile).count()

        user_messages = sorted(list(set(unsorted_messages)), key=attrgetter('created_on'), reverse=True)
        nav_messages = DirectMessage.objects.filter(receiver=user_profile).filter(status='UNREAD').order_by('-created_on')[:5]
        form = ConversationForm()
        return {
            'profile': user_profile, 
            'nav_messages': nav_messages,
            'direct_messages': user_messages, 
            'alerts': user_alerts, 
            'all_alerts': all_alerts, 
            'unread_count': unread_messages_count, 
            'conversation_form': form,
            'message_count': conv_count
            }
    else:
        return{}
