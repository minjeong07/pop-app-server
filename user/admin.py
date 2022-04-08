from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

@admin.register(models.User)
class UserAdmin(UserAdmin):
    
    """ User Admin """
    
 
    fieldsets =(
        (
            "Custom Profile",
            {
                "fields":(
                    'username',
                    'password',
                    "profile_img",
                    'tag',
                )
            }
        ),
    )
    
    list_display = ('username','tag')