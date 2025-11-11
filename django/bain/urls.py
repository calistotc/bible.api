from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from bolls.urls import bible_urlpatterns, bible_docs_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('docs/bible/', include(bible_docs_urlpatterns)),  # Bible API documentation at /docs/bible/
    path('bible/', include(bible_urlpatterns)),  # Bible API endpoints under /bible/
    path('', include('bolls.urls')),  # User management at root
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]
