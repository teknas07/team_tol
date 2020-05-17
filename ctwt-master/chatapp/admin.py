from django.contrib import admin
from .models import Group, GroupMember, Message, GroupMessage
# Register your models here.

# admin.site.register(User)


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'date_of_birth',)
#     fields = ['first_name', 'last_name', ('date_of_birth')]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


# @admin.register(GroupMember)
# class GroupMemberAdmin(admin.ModelAdmin):
#     list_display = ('group_id',)


# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('from_id', 'to_id',)
#     fields = ['from_id', 'to_id']

admin.site.register(Message)
admin.site.register(GroupMessage)
admin.site.register(GroupMember)
# admin.site.register(Group)


# @admin.register(GroupMessage)
# class GroupMessageAdmin(admin.ModelAdmin):
#     list_display = ('from_id', 'to_id',)
#     fields = ['from_id', 'to_id']
