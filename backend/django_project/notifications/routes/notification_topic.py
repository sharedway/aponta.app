
from django.urls import path,include, re_path
from notifications.views import NotificationTopicModelTemplateView,NotificationTopicModelDetailView, NotificationTopicModelListView, NotificationTopicModelUpdateView, NotificationTopicModelDeleteView, NotificationTopicModelCreateView

urlpatterns = [    
    path("", NotificationTopicModelTemplateView.as_view(), name="notificationtopicmodel-index"),    
    path("collection/", NotificationTopicModelListView.as_view(), name="notificationtopicmodel-list"),
    path("collection/<int:pk>/", NotificationTopicModelDetailView.as_view(), name='notificationtopicmodel-detail'),
    path("collection/<int:pk>/editar/", NotificationTopicModelUpdateView.as_view(), name='notificationtopicmodel-update'),
    path("collection/<int:pk>/remover/", NotificationTopicModelDeleteView.as_view(), name='notificationtopicmodel-delete'),    
    path("collection/adicionar/", NotificationTopicModelCreateView.as_view(), name='notificationtopicmodel-create'),
]