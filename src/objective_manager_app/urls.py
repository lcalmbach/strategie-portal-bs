from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_detail, name="home_detail"),
    path("themen/", views.themen_list, name="themen_list"),
    path("handlungsfelder/", views.handlungsfelder_list, name="handlungsfelder_list"),
    path("ziele/", views.ziele_list, name="ziele_list"),
    path("massnahmen/", views.massnahmen_list, name="massnahmen_list"),
    path("plan_records/", views.plan_records_list, name="plan_records_list"),
    path("thema/<int:pk>/", views.thema_detail, name="thema_detail"),
    path(
        "handlungsfeld/<int:pk>/",
        views.handlungsfeld_detail,
        name="handlungsfeld_detail",
    ),
    path("ziel/<int:pk>/", views.ziel_detail, name="ziel_detail"),
    path("massnahme/<int:pk>/", views.massnahme_detail, name="massnahme_detail"),
    path("plan_record/<int:pk>/", views.plan_record_detail, name="plan_record_detail"),
    path(
        "handlungsfeld/<int:pk>/edit/",
        views.handlungsfeld_edit,
        name="handlungsfeld_edit",
    ),
    path("ziel/<int:pk>/edit/", views.ziel_edit, name="ziel_edit"),
    path("massnahme/<int:pk>/edit/", views.massnahme_edit, name="massnahme_edit"),
    path("plan_record/<int:pk>/edit/", views.plan_record_edit, name="plan_record_edit"),
]
