"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
import review.views
import authentication.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication.views.login_page, name="login"),
    path('flux/', review.views.flux, name='flux'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('review/create', review.views.create_review, name="create_review"),
    path('ticket/create', review.views.create_ticket, name="create_ticket" ),
    #path('review/<int:review_id>', review.views.display_review, name='display_review'),
    path('ticket/<int:ticket_id>', review.views.display_ticket, name='display_ticket'),
    path('ticket/<int:ticket_id>/edit', review.views.edit_ticket, name='edit_ticket'),
    path('review/<int:review_id>/edit', review.views.edit_review, name='edit_review'),
    path('posts', review.views.display_posts, name='display_posts'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
