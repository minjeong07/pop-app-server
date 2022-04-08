from django.contrib import admin
from card.models import Gift, Message, Decoration


# Register your models here.
@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ("id", "gift_name", "gift_desc")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "to_user_id", "gift_id", "updated_at")


@admin.register(Decoration)
class GiftAdmin(admin.ModelAdmin):
    list_display = ("id", "deco_name")
