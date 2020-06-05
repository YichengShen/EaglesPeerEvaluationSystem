from django.db import models

# models from other Apps
from account.models import User


# python packages
import datetime


# ------------------------- COURSE MODEL -----------------------------------------
class Course(models.Model):
    course_name = models.CharField("course name", max_length=60)
    course_code = models.IntegerField("course code")
    section_number = models.SmallIntegerField("section number")
    year = models.SmallIntegerField("year of realization")
    semester_choices = (
        ('S', 'Spring'),
        ('F', 'Fall'),
    )
    semester = models.CharField("semester of realization", max_length = 1, choices = semester_choices)
    professors = models.ManyToManyField(User)
    students = models.ManyToManyField(User, related_name="students")
    
    def __str__(self):
        return "{} {}{}".format(self.course_name, self.year, self.semester)

    def is_active(self):
        "Returns whether the course is active."
        if self.year >= datetime.datetime.now().year: # realization year >= current year
            if self.semester == 'S':
                month = 6
            else:
                month = 12
            if month >= datetime.datetime.now().month: # realization month >= current month
                return True
        return False





# ------------------------- TEAM MODEL -----------------------------------------
class Team(models.Model):
    # Primary Key is the auto-generated ID
    team_name = models.CharField("team name", max_length=60)
    
    course = models.ForeignKey(Course, on_delete = models.CASCADE) # a Course object
    student = models.ManyToManyField(User) # a querySet of User objects

    def __str__(self):
        return self.team_name



