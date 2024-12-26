from django.contrib import admin
from userauths.models import User, Profile
# for this he said refer to django admin section
# for this also his videos
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date']

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)