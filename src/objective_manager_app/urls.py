from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_detail, name="home_detail"),
    path("", views.admin_detail, name="admin_detail"),
    path("themen/", views.themen_list, name="themen_list"),
    # Listen
    path("handlungsfelder/", views.handlungsfelder_list, name="handlungsfelder_list"),
    path("ziele/", views.ziele_list, name="ziele_list"),
    path("massnahmen/", views.massnahmen_list, name="massnahmen_list"),
    path("plan_records/", views.plan_records_list, name="plan_records_list"),
    path("personen/", views.personen_list, name="personen_list"),
    path("organisationen/", views.organisationen_list, name="organisationen_list"),
    # Detail Masken
    path("thema/<int:pk>/", views.thema_detail, name="thema_detail"),
    path(
        "handlungsfeld/<int:pk>/",
        views.handlungsfeld_detail,
        name="handlungsfeld_detail",
    ),
    path("ziel/<int:pk>/", views.ziel_detail, name="ziel_detail"),
    path("massnahme/<int:pk>/", views.massnahme_detail, name="massnahme_detail"),
    path("plan_record/<int:pk>/", views.plan_record_detail, name="plan_record_detail"),
    
    # Edit Masken
    path(
        "handlungsfeld/<int:pk>/edit/",
        views.handlungsfeld_edit,
        name="handlungsfeld_edit",
    ),
    path("ziel/<int:pk>/edit/", views.ziel_edit, name="ziel_edit"),
    path("massnahme/<int:pk>/edit/", views.massnahme_edit, name="massnahme_edit"),
    path("plan_record/<int:pk>/edit/", views.plan_record_edit, name="plan_record_edit"),
    path("person/<int:pk>/edit/", views.person_edit, name="person_edit"),
    path("organisation/<int:pk>/edit/", views.organisation_edit, name="organisation_edit"),
    # Delete Masken
    path('person/<int:pk>/delete/', views.person_delete, name='person_delete'),
    path('organisation/<int:pk>/delete/', views.organisation_delete, name='organisation_delete'),
    # add Record Masken
    path('organisation/create/', views.OrganizationCreateView.as_view(), name='organisation_create'),
    path('massnahme/create/', views.MassnahmeCreateView.as_view(), name='massnahme_create'),
    path('handlungsfeld/create/', views.HandlungsfeldCreateView.as_view(), name='handlungsfeld_create'),
    path('ziel/create/', views.ZielCreateView.as_view(), name='ziel_create'),
    path('person/create/', views.PersonCreateView.as_view(), name='person_create'),
    path('plan_record/create/', views.PlanRecordCreateView.as_view(), name='planrecord_create'),
]
