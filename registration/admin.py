from django.contrib import admin

from .models import Course, Team



class TeamInline(admin.StackedInline):
    model = Team
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Course Information',      {'fields': ['course_name', 
                                                'course_code',
                                                'section_number',
                                                'year',
                                                'semester',
                                                ]}),
        ('Professors and Students', {'fields': ['professors', 
                                                'students',
                                                ]}),
    ]

    inlines = [TeamInline]

    list_display = ('course_name', 
                    'course_code',
                    'section_number',
                    'year',
                    'semester',
                    )




admin.site.register(Course, CourseAdmin)
