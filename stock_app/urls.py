from django.urls import path
from .views import home_view, stock_view, analysis_view, plot_view, news_view

urlpatterns = [
    path('', home_view, name='home_view'),
    path('stock/', stock_view, name='stock_view'),
    path('analysis/', analysis_view, name='analysis_view'),
    path('plot/', plot_view, name='plot_view'),
    path('news/', news_view, name='news_view'),
]
