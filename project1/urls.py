"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# swagger settings
schema_view = get_schema_view(
   openapi.Info(
      title="Infinity Fire solution APIs",
      default_version='v0.2.0',
      description="Welcome to the API Documentation",
   ),
   public=True,
   permission_classes=[permissions.AllowAny]
)

  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('myaap.urls')),

    #swagger links for the api documentation
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
