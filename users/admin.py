import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.core.files.storage import get_storage_class

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.action(description="Reset required flags")
def reset_all_required_flags(modeladmin, request, queryset):
    queryset.update(wants_valid_membership=False)
    queryset.update(paid_membership=False)
    queryset.update(has_zpls=False)
    queryset.update(has_fai=False)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # Displays on home page.
    list_display = (
        "first_name", "last_name", "email", "date_born", "has_zpls", "has_fai", "wants_valid_membership",
        "paid_membership", "modified_date")
    # Filter.
    list_filter = ()
    # Specific user view and settings.
    fieldsets = (
        ("User information", {"fields": ("first_name", "last_name", "password")}),
        ("Personal information", {"fields": ("date_born", "social_security_number")}),
        ("Address", {"fields": ("street", "zipcode", "city")}),
        ("Contact information", {"fields": ("email", "phone_number")}),
        ("Licences", {"fields": ("has_zpls", "has_fai", "antidoping_certificate")}),
        ("Membership", {"fields": ("wants_valid_membership", "paid_membership")}),
        ("Roles", {"fields": ("is_staff",)}),
        ("Udpates", {"fields": ("modified_date",)})
    )
    add_fieldsets = (
        ("Sing in information", {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2"
            )}
         ),
        ("Personal information", {
            "classes": ("wide",),
            "fields": (
                "first_name", "last_name", "date_born", "social_security_number"
            )}
         ),
        ("Address", {
            "classes": ("wide",),
            "fields": (
                "street", "zipcode", "city"
            )}
         ),
        ("Contact information", {
            "classes": ("wide",),
            "fields": (
                "phone_number",
            )}
         ),
        ("Licences", {
            "classes": ("wide",),
            "fields": (
                "has_zpls", "has_fai", "antidoping_certificate"
            )}
         ),
        ("Membership", {
            "classes": ("wide",),
            "fields": (
                "wants_valid_membership",
                "paid_membership",
            )}
         ),
        ("Roles", {
            "classes": ("wide",),
            "fields": (
                "is_staff",
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("first_name",)
    readonly_fields = ("modified_date",)

    @admin.action(description="Export for ZPLS")
    def export_for_ZPLS(self, request, queryset):
        meta = self.model._meta
        field_names = ['first_name', 'last_name', 'date_born', 'street', 'city', 'zipcode']

        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename=ZPLS_export.xlsx'
        writer = csv.writer(response)

        writer.writerow(['Ime', 'Priimek', 'Rojen', 'Ulica', 'Mesto', 'Poštna številka'])
        for obj in queryset:
            row = [
                getattr(obj, field) if getattr(obj, "has_zpls") else None
                for field in field_names]
            if row[0] is not None:
                writer.writerow(row)

        return response

    @admin.action(description="Export ALL")
    def export_all(self, request, queryset):
        meta = self.model._meta
        field_names = ['first_name', 'last_name', 'email', 'date_born', 'street', 'city', 'zipcode', 'has_zpls', 'has_fai', 'wants_valid_membership']

        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename=metuljadmin_export.xlsx'
        writer = csv.writer(response)

        writer.writerow(['Ime', 'Priimek', 'Email', 'Rojen', 'Ulica', 'Mesto', 'Poštna številka', 'ZPLS', 'FAI', 'Članarina'])
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            if row[0] is not None:
                writer.writerow(row)

        return response

    @admin.action(description="Export for LZS")
    def export_for_LZS(self, request, queryset):
        meta = self.model._meta
        field_names = ['first_name', 'last_name', 'date_born', 'street', 'city', 'zipcode', 'social_security_number',
                       'has_fai', 'antidoping_certificate']
        media_storage = get_storage_class()()
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename=LZS_export.xlsx'
        writer = csv.writer(response)

        writer.writerow(['Ime', 'Priimek', 'Rojen', 'Ulica', 'Mesto', 'Poštna številka', 'EMŠO', 'FAI', 'Certifikat'])
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            row = ['Da' if v == True else ('Ne' if v == False else v) for v in row]

            # Obtain full s3 link.
            if obj.antidoping_certificate.name != "":
                boto_s3_url = media_storage.url(name=obj.antidoping_certificate.name)
            else:
                boto_s3_url = "missing"
            row[-1] = boto_s3_url

            if row[0] is not None:
                writer.writerow(row)

        return response

    actions = [reset_all_required_flags, export_for_ZPLS, export_for_LZS, export_all]


admin.site.register(CustomUser, CustomUserAdmin)
