from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ..models import Profile
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Perfil"
    fields = ("unidade_compra",)  # Apenas exibe o campo uasg

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_uasg",
    )

    def get_uasg(self, obj):
        return obj.profile.unidade_compra
    get_uasg.short_description = "UASG"

# Re-registre o modelo User com o novo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)