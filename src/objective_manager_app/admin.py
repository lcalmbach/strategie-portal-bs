from django.contrib import admin
from .models import BusinessObject, Code, User


# Register the BusinessObject model with a custom admin class if needed
@admin.register(BusinessObject)
class BusinessObjectAdmin(admin.ModelAdmin):
    list_display = (
        "kuerzel",
        "titel",
        "typ",
        "vorgaenger",
        "erstellt_am",
        "erstellt_von",
    )
    search_fields = ("titel", "kuerzel", "beschreibung")
    list_filter = ("typ", "erstellt_am", "erstellt_von")


# If you need to manage the `Code` and `User` models through admin
admin.site.register(Code)
# Note: User is typically managed by Django's built-in admin. If you have a custom user model, you might want to register it differently.
# admin.site.register(User)
