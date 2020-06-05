from django.contrib import admin

from .models import Assessment, Question, Answer, Result_set


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text', 
                                         'type_answer',
                                        ]}),
    ]

    list_display = ('question_text', 'type_answer')


class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question', 
                                         'evaluator',
                                         'team_member',
                                         'answer_text',
                                         'answer_rating',
                                        ]}),
    ]

    list_display = ('id', 'question', 'evaluator', 'team_member')


class Result_setAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['student', 
                                         'team',
                                         'rating_answers',
                                         'text_answers',
                                        ]}),
    ]

    list_display = ('id', 'student', 'team')



class AssessmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 
                                         'description',
                                         'course',
                                         'completed_students',
                                        ]}),
        ('Date information', {'fields': ['start_date', 'end_date']}),
        ('Questions', {'fields': ['questions']}),
    ]

    list_display = ('name', 'course', 'end_date')



admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result_set, Result_setAdmin)
admin.site.register(Assessment, AssessmentAdmin)
