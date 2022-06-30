
from django.urls import path,include, re_path
from notifications.views import NotificationTopicModelTemplateView,NotificationTopicModelDetailView, NotificationTopicModelListView, NotificationTopicModelUpdateView, NotificationTopicModelDeleteView, NotificationTopicModelCreateView

urlpatterns = [    
    path("", NotificationTopicModelTemplateView.as_view(template_name="notificationtopicmodel/app_templates/notificationtopicmodel_index.html"), name="notificationtopicmodel-index"),    
    path("collection/", NotificationTopicModelListView.as_view(template_name = "notificationtopicmodel/app_templates/notificationtopicmodel_list.html"), name="notificationtopicmodel-list"),
    path("collection/<int:pk>/", NotificationTopicModelDetailView.as_view(template_name = "notificationtopicmodel/app_templates/notificationtopicmodel_detail.html"), name='notificationtopicmodel-detail'),
    path("collection/<int:pk>/editar/", NotificationTopicModelUpdateView.as_view(template_name = "notificationtopicmodel/app_templates/notificationtopicmodel_update.html"), name='notificationtopicmodel-update'),
    path("collection/<int:pk>/remover/", NotificationTopicModelDeleteView.as_view(template_name = "notificationtopicmodel/app_templates/notificationtopicmodel_delete.html"), name='notificationtopicmodel-delete'),    
    path("collection/adicionar/", NotificationTopicModelCreateView.as_view(template_name = "notificationtopicmodel/app_templates/notificationtopicmodel_create.html"), name='notificationtopicmodel-create'),
]