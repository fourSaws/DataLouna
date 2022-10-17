from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import subscriptionPaid, onEnter, updateStatus

urlpatterns = [
    path("api/onEnter", onEnter.as_view()),
    path("api/subscriptionPaid", subscriptionPaid.as_view()),
    path("api/updateStatus", updateStatus.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
