
from django.urls import path,include, re_path
from alertas.views import AlertaModelTemplateView,AlertaModelDetailView, AlertaModelListView, AlertaModelUpdateView, AlertaModelDeleteView, AlertaModelCreateView

urlpatterns = [    
    path("", AlertaModelTemplateView.as_view(), name="alertamodel-index"),    
    path("collection/", AlertaModelListView.as_view(), name="alertamodel-list"),
    path("collection/<int:pk>/", AlertaModelDetailView.as_view(), name='alertamodel-detail'),
    path("collection/<int:pk>/editar/", AlertaModelUpdateView.as_view(), name='alertamodel-update'),
    path("collection/<int:pk>/remover/", AlertaModelDeleteView.as_view(), name='alertamodel-delete'),    
    path("collection/adicionar/", AlertaModelCreateView.as_view(), name='alertamodel-create'),
]