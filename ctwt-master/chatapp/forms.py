from django import forms
from .models import Message, Group, GroupMember, GroupMessage, User

class SendMessage(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('text',)

class CreateGroup(forms.ModelForm):

    class Meta:
        model = Group
        fields=('name',)

class SendMessageToGroup(forms.ModelForm):

    class Meta:
        model = GroupMessage
        fields = ('text',)

# class AddMember(forms.ModelForm):

#     class Meta:
#         model = GroupMember
#         fields = ('user_id','group_id')