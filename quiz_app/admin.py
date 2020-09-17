from django.contrib import admin
from .models import (Quiz,Question,Answer,
					QuizAnalysis,StoredStudentAnswer)

class QuizAdmin(admin.ModelAdmin):
	"""This helps to customize the admin site for quiz model"""

	list_display = ['title','subject','is_active']
	list_filter  = ['is_active']
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields= ['user']
	search_fields = ['title']

admin.site.register(Quiz,QuizAdmin)

class answer_admin(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
	raw_id_fields = ['quiz']
	inlines       = [answer_admin]
	# made it raw_id_field because when number of quiz inc.
	#it becomes difficult to find a quiz

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(QuizAnalysis)
admin.site.register(StoredStudentAnswer)
