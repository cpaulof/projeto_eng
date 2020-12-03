# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Navio, Solicitacao, Berco, Atracacao, RegistroSaida


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login', 'user_type')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'name', 'user_type', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'user_type', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)

@admin.register(Navio)
class NavioAdmin(admin.ModelAdmin):
    pass
@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    pass
@admin.register(Berco)
class BercoAdmin(admin.ModelAdmin):
    pass
@admin.register(RegistroSaida)
class RegistroSaidaAdmin(admin.ModelAdmin):
    pass


@admin.register(Atracacao)
class AtracacaoAdmin(admin.ModelAdmin):
    fields = ('solicitacao', 'berco', ('data_entrada', 'data_saida'))

