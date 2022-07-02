from django.contrib import admin
from django.urls import path, include, converters
from django.conf import settings
from .views import CustomAuthToken
from project.admin import project_admin_site, project_dashboard_site

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("manager/", 
            include(
            [             
                path("", project_dashboard_site.urls)                
            ]
        ),    
    ),    
    path("api-token-auth/", CustomAuthToken.as_view(), name="get-token-auth"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", 
            include(
            [             
                path("alertas/", include("alertas.web_routes.v1.alerta"))                
            ]
        ),    
    ),    

    path("", include("django.contrib.flatpages.urls")),
]
