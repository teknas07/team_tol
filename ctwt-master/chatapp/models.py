from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ['name']

    # def get_absolute_url(self):
    #     return reverse("group_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.name}'


class GroupMember(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse("group_members_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.pk}'


class Message(models.Model):
    from_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='to_user')
    text = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False)

    # def get_absolute_url(self):
    #     return reverse("message_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.pk}'


class GroupMessage(models.Model):
    from_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user_id = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='to_user')
    text = models.TextField(max_length=500)

    # def get_absolute_url(self):
    #     return reverse("group_message_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.pk}'
