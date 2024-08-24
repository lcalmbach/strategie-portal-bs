from django.contrib import admin
from .models import BusinessObject, Code, Person, Organisation


# Register the BusinessObject model with a custom admin class if needed
@admin.register(BusinessObject)
class BusinessObjectAdmin(admin.ModelAdmin):
    list_display = (
        'kuerzel',
        'titel',
        'typ',
        'vorgaenger',
        'erstellt_am',
        'erstellt_von',
    )
    search_fields = ('titel', 'kuerzel', 'beschreibung')
    list_filter = ('typ', 'erstellt_am', 'erstellt_von')
    

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = (
        'departement',
        'dienststelle',
        'bereich',
    )
    search_fields = ('departement','dienststelle','bereich')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('vorname', 'nachname', 'username', 'user_id')  # Fields to display in the list view

    def username(self, obj):
        return obj.user.username  # Access the related User model's username field

    def user_id(self, obj):
        return obj.user.pk  # Access the related User model's username field
    
    username.admin_order_field = 'user__username'  # Allows sorting by username
    username.short_description = 'Username'  # Column name in the admin list view

    search_fields = ('vorname','nachname')



admin.site.register(Code)
