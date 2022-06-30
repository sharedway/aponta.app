
from django.urls import path,include, re_path
from notifications.views import NotificationModelTemplateView,NotificationModelDetailView, NotificationModelListView, NotificationModelUpdateView, NotificationModelDeleteView, NotificationModelCreateView

urlpatterns = [    
    path("", NotificationModelTemplateView.as_view(template_name="notificationmodel/app_templates/notificationmodel_index.html"), name="notificationmodel-index"),    
    path("collection/", NotificationModelListView.as_view(template_name = "notificationmodel/app_templates/notificationmodel_list.html"), name="notificationmodel-list"),
    path("collection/<int:pk>/", NotificationModelDetailView.as_view(template_name = "notificationmodel/app_templates/notificationmodel_detail.html"), name='notificationmodel-detail'),
    path("collection/<int:pk>/editar/", NotificationModelUpdateView.as_view(template_name = "notificationmodel/app_templates/notificationmodel_update.html"), name='notificationmodel-update'),
    path("collection/<int:pk>/remover/", NotificationModelDeleteView.as_view(template_name = "notificationmodel/app_templates/notificationmodel_delete.html"), name='notificationmodel-delete'),    
    path("collection/adicionar/", NotificationModelCreateView.as_view(template_name = "notificationmodel/app_templates/notificationmodel_create.html"), name='notificationmodel-create'),
]