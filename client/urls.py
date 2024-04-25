from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import ServiceClientListView, ServiceClientCreateView, ServiceClientDetailView, \
    ServiceClientUpdateView, ServiceClientDeleteView, MessageListView, MessageCreateView, MessageDetailView, \
    MessageUpdateView, MessageDeleteView, NewsletterListView, NewsletterCreateView, NewsletterDetailView, \
    NewsletterUpdateView, NewsletterDeleteView, NewsletterModeratorUpdateView, HomeListView

app_name = ClientConfig.name

urlpatterns = [
    path('home_view/', cache_page(60)(HomeListView.as_view()), name='home_view'),

    path('', ServiceClientListView.as_view(), name='home'),
    path('create/', ServiceClientCreateView.as_view(), name='create'),
    path('view/<int:pk>/', ServiceClientDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', ServiceClientUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ServiceClientDeleteView.as_view(), name='delete'),

    path('message/', MessageListView.as_view(), name='message'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('view_message/<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('edit_message/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('newsletter/', NewsletterListView.as_view(), name='newsletter'),
    path('create_newsletter/', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('view_newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='view_newsletter'),
    path('edit_newsletter/<int:pk>/', NewsletterUpdateView.as_view(), name='edit_newsletter'),
    path('delete_newsletter/<int:pk>/', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('newsletter_moder_edit/<int:pk>/', NewsletterModeratorUpdateView.as_view(), name='newsletter_moder_edit'),
]
