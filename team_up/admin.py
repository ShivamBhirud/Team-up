from django.contrib import admin
from team_up.models import Teams
from team_up.models import RecruitedTeammates
from team_up.models import ApplicationStatus
# Register your models here.


class RecruitedTeammatesAdmin(admin.ModelAdmin): 
    list_display = ('teamup_advertisement_id', 'teammates') 
  
    def active(self, obj): 
        return obj.is_active == 1
  
    active.boolean = True


admin.site.register(Teams)
admin.site.register(RecruitedTeammates, RecruitedTeammatesAdmin)
admin.site.register(ApplicationStatus)