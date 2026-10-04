from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Customer, Lead, Deal, Ticket, Note, Activity


# ============================================================
# CUSTOMER ADMIN
# ============================================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "email", "phone_number",
        "company", "city", "status", "created_at",
    )
    list_filter = ("status", "city", "country", "created_at")
    search_fields = (
        "first_name", "last_name", "email",
        "phone_number", "company",
    )
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (_("اطلاعات شخصی"), {
            "fields": ("first_name", "last_name", "email", "phone_number")
        }),
        (_("اطلاعات مکانی"), {
            "fields": ("city", "country", "address")
        }),
        (_("اطلاعات تجاری"), {
            "fields": ("company", "status")
        }),
        (_("یادداشت‌ها"), {
            "fields": ("notes",),
            "classes": ("collapse",),
        }),
        (_("متادیتا"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


# ============================================================
# LEAD ADMIN
# ============================================================

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "first_name", "last_name", "email",
        "company", "source", "status", "created_at",
    )
    list_filter = ("status", "source", "created_at")
    search_fields = ("first_name", "last_name", "email", "company")
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")


# ============================================================
# DEAL ADMIN
# ============================================================

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        "title", "customer", "amount",
        "stage", "probability", "expected_close_date", "created_at",
    )
    list_filter = ("stage", "created_at")
    search_fields = ("title", "customer__first_name", "customer__last_name")
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("customer",)


# ============================================================
# TICKET ADMIN
# ============================================================

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id", "subject", "customer",
        "priority", "status", "created_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("subject", "description", "customer__first_name")
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "resolved_at")
    autocomplete_fields = ("customer",)


# ============================================================
# NOTE ADMIN
# ============================================================

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "lead", "deal", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content",)
    readonly_fields = ("created_at",)
    autocomplete_fields = ("customer", "lead", "deal")


# ============================================================
# ACTIVITY ADMIN
# ============================================================

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "id", "activity_type", "subject",
        "customer", "lead", "due_date", "is_done", "created_at",
    )
    list_filter = ("activity_type", "is_done", "created_at")
    search_fields = ("subject", "description")
    list_per_page = 25
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    autocomplete_fields = ("customer", "lead")