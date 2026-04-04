from django.urls import path # ต้องมีบรรทัดนี้
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'archive'

urlpatterns = [
    path('', views.home_view, name='home'),          # หน้าแรก (Landing)
    path('list/', views.list_view, name='list'),    # หน้ารายการทั้งหมด
    path('add/', views.add_view, name='add'),
    path('delete/<int:pk>/', views.delete_view, name='delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)