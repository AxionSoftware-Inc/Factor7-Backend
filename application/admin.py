from django.contrib import admin
from .models import Category, Tag, Tour, Booking, Inquiry, VisitorLog

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'duration', 'is_published', 'is_featured', 'views')
    list_filter = ('is_published', 'is_featured', 'category', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'tour', 'phone_number', 'booking_date', 'status', 'created_at')
    list_filter = ('status', 'booking_date', 'created_at')
    search_fields = ('full_name', 'phone_number', 'tour__title')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('full_name', 'phone_number', 'message')

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'method', 'timestamp')
    list_filter = ('method', 'timestamp')
    search_fields = ('ip_address', 'path')

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
