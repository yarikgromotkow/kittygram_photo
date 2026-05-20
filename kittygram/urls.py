from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from cats.views import cat_list, ContestViewSet, EntryViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'contests', ContestViewSet, basename='contest')
router.register(r'entries', EntryViewSet, basename='entry')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cats/', cat_list),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


