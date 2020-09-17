from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('common_pages.urls')),
    path('',include('quiz_app.urls')),
    path('',include('my_auth.urls')),
    path('',include('user_related.urls')),
    #third party
    path('api-auth/', include('rest_framework.urls')),

]



if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
