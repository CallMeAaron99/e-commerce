from django.contrib import admin
from django.contrib.auth import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from account.views import accountActivate

admin.site.site_header = settings.SITE_HEADER

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('account.urls')),
    path('api/products/', include('product.urls')),

    # Account activation
    path('account-activate/', accountActivate, name='account_activate'),

    # Password reset
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(extra_context={"site_header": admin.site.site_header}), name="password_reset_confirm"),
    path('reset/done/', views.PasswordResetCompleteView.as_view(extra_context={"site_header": admin.site.site_header}), name="password_reset_complete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
