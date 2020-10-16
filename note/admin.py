from django.contrib import admin

from .models import User, Note, Label

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text')

class LabelAdmin(admin.ModelAdmin):
    list_display = ('user', 'label')

admin.site.register(User, UserAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Label, LabelAdmin)

