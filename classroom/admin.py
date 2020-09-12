from django.contrib import admin

# Register your models here.
from .models import Room,Studentjoin,Teachercreate,CommentAnswer,Comment,Question,Answer,Quiz,Assignment,Studentsolution,Announcement,Dashboard

admin.site.register(Teachercreate)
admin.site.register(Room)
admin.site.register(Studentjoin)
admin.site.register(Comment)
admin.site.register(CommentAnswer)

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Assignment)
admin.site.register(Studentsolution)
admin.site.register(Announcement)
admin.site.register(Dashboard)