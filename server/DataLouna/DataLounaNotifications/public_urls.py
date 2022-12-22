from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from DataLounaNotifications.views import subscriptionPaid, onEnter, updateStatus, sendQuizAnswer

urlpatterns = [
    path("api/onEnter", onEnter.as_view()),
    path("api/updateStatus", updateStatus.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
