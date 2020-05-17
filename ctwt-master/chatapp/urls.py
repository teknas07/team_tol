from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('conversation/<slug:obj>/', views.conversation,name='conversation'),
    # path(r'^conversation/<str:obj>/',views.conversation,name='conversation')
    path('createGroup', views.createGroup,name='createGroup'),
    path('groupDetail/<int:gid>/', views.groupDetail,name='groupDetail'),
    path('userAdded/<int:gid>/',views.AddMemberToGroup, name='user_added')
]
