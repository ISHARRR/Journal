from django.urls import path
from .views import TaskList, TaskCreate, TaskUpdate, DeleteTaskView, CustomLoginView, RegisterPage, TaskReorder, \
    ContactList, ContactCreate, ContactUpdate, DeleteContactView
from django.contrib.auth.views import LogoutView


class ContactReorder:
    pass


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    # task
    path('', TaskList.as_view(), name='tasks'),
    # path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteTaskView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),

    # contacts
    path('contact/', ContactList.as_view(), name='contacts'),
    # path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('contact-create/', ContactCreate.as_view(), name='contact-create'),
    path('contact-update/<int:pk>/', ContactUpdate.as_view(), name='contact-update'),
    path('contact-delete/<int:pk>/', DeleteContactView.as_view(), name='contact-delete'),

]
