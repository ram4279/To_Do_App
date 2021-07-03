from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (SignUpView, TaskCreateView, TaskDeleteView, TaskListView, TaskDetailView, TaskUpdateView,
    UserLoginView
)



urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='task-detail'), # to override pk to something like id there is option
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('update/<int:pk>', TaskUpdateView.as_view(), name='task-update'),
    path('delete/<int:pk>', TaskDeleteView.as_view(), name='task-delete')
]