from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from rest_framework.documentation import include_docs_urls

v1 = ([
          path('', include('core.urls')),
      ], 'v1')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(v1)),
    path('health', lambda request: HttpResponse(status=200)),
    path('docs/', include_docs_urls(title='Test API', description='', public=True), name='docs'),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
