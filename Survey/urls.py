from django.urls import path, include

urlpatterns = [
    path('api/', include('surveyAPI.urls')),
    path('api/admin/', include('admin.urls'))
]
