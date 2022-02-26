from django.urls import include, path

urlpatterns = [
    path('browsable-api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
]