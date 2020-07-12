from django.contrib import admin
from team_up.models import Teams, Recruited_Teammates
# Register your models here.


class Recruited_TeammatesAdmin(admin.ModelAdmin): 
    list_display = ('teamup_advertisement_id', 'teammates') 
  
    def active(self, obj): 
        return obj.is_active == 1
  
    active.boolean = True


admin.site.register(Teams)
admin.site.register(Recruited_Teammates, Recruited_TeammatesAdmin)
