from django.contrib import admin
from django.utils.translation import gettext as _, gettext_lazy
from django.conf import settings



class BaseModelAdmin(admin.ModelAdmin):
    # add_form_template = 'admin/auth/user/add_form.html'
    # change_form_template = 'tabbed_admin/change_form.html'
    # change_list_template = 'admin/change_list.htm'
    #add_form_template = None
    #change_form_template = None    
    # change_list_template = None
    # delete_confirmation_template = None
    # delete_selected_confirmation_template = None
    # object_history_template = None
    # popup_response_template = None


    admin_priority = 20
    default_lon = -5372220.98 
    default_lat = -2413950.78
    map_width = 800
    map_height = 600
    default_zoom = 8
    save_on_top = True
    date_hierarchy = "created"
    list_per_page = 200
    list_max_show_all = 300
    actions_on_bottom = True
    EXCLUDE_FROM_ADMIN = []    
    exclude = [
         "criado_por","modificado_por","removido_por","isRemoved",
        "isActive", "isDone", "isComplete", "isPublic", "isProcessed","alterado_por"]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class BaseModelAdminTabular(admin.TabularInline):
    ""


class ProjectAdminSite(admin.AdminSite):
    site_header = settings.SITE_HEADER
    site_title = settings.SITE_TITLE
    index_title = settings.SITE_INDEX_TITLE  
    enable_nav_sidebar = True
    index_template = "admin/admin_api/index.html"
    app_index_template = "admin/admin_api/app_index.html"


    def each_context(self, request):
        self.request= request
        contexto = super().each_context(request)

        contexto.update({
            "map_credits":'Desenvolvido por <a href="https://www.sharedway.app/copyright">SharedWAY&copy;</a> aplicativos e sistemas de alta disponibilidade  Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            "rest_api_address":f"{settings.REST_API_ADDRESS}",
            "socket_api_address":f"{settings.SOCKET_API_ADDRESS}",   
        })
        return contexto

    
project_admin_site = ProjectAdminSite(name="admin")



class ProjectDashBoardSite(admin.AdminSite):
    site_header = settings.SITE_HEADER
    site_title = settings.SITE_TITLE
    index_title = settings.SITE_INDEX_TITLE   
    enable_nav_sidebar = True
    index_template = "admin/admin_dashboard/index.html"
    app_index_template = "admin/admin_dashboard/app_index.html"    
     



    def each_context(self, request):
        self.request= request
        contexto = super().each_context(request)
        contexto.update({          
            "body_class":"manager",    
            "map_credits":'Desenvolvido por <a target="_sharedway" href="https://www.sharedway.app">SharedWAY&copy;</a> aplicativos e sistemas de alta disponibilidade  Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',              
            "rest_api_address":f"{settings.REST_API_ADDRESS}",
            "socket_api_address":f"{settings.SOCKET_API_ADDRESS}",   
        })

        return contexto


project_dashboard_site = ProjectDashBoardSite(name="painel")
