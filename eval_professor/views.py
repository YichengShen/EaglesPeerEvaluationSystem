from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse

# models imported from other apps
from registration.models import Course, Team
from assessment.models import Assessment, Question, Answer, Result_set
from account.models import User

# import Python packages
from re import search as regex_search
import datetime
import csv

import smtplib
from email.message import EmailMessage

import numpy as np
from math import isnan




# Instructor Dashboard Page
def professor_dashboard(request):
    return render(request, 'eval_professor/professor-dashboard.html')


# All Assessments Page
def all_assessments(request):
    team_list = Team.objects.all()
    assessment_list = Assessment.objects.all()
    filtered_list = [assessment for assessment in assessment_list.all() if request.user in assessment.course.professors.all()]
    context = {
        'team_list': team_list,
        'assessment_list': filtered_list,
    }
    return render(request, 'eval_professor/all-assessments.html', context = context)


# Create New Assessment Page
def create_new_assessment(request):
    course_list = Course.objects.all()
    context = {
        'course_list': course_list,
    }
    return render(request, 'eval_professor/create-new-assessment.html', context = context)


# My Courses Page
def my_courses(request):
    course_list = Course.objects.all()
    context = {
        'course_list': course_list,
    }
    return render(request, 'eval_professor/my-courses.html', context = context)


# Create New Course Page
def create_new_course(request):
    return render(request, 'eval_professor/create-new-course.html')

    
# Teams & Students Page
def teams_students(request):
    team_list = Team.objects.all().order_by('team_name')
    course_list = Course.objects.all() # this info is needed for the dropdown select in creating new team
    context = {
        'team_list': team_list,
        'course_list': course_list,
    }
    return render(request, 'eval_professor/teams-students.html', context = context)




# ----------------------------------- Course Section (functions below are for courses) --------------

# Function: create a new course
def make_new_course(request):
    course_name = request.POST['course name']
    course_code = request.POST['course code']
    section_number = request.POST['section number']
    year = request.POST['year']
    semester = request.POST['semester']
    co_professor_id = request.POST['co-professor ID']
    # CAN CHANGE THIS TO SELECT CURRENT PROF

    course_name = course_name.title()

    # the professor registering must be the current user
    professor = request.user

    # convert text to required format in the model
    if semester == 'Fall':
        semester_initial = 'F'
    else:
        semester_initial = 'S'
 
    # Validations of input formatting are DONE in html templates

    # Validation to prevent duplicate course
    course_valid = False
    if len(Course.objects.filter(course_code=course_code, 
                            section_number=section_number, 
                            year=year, 
                            semester=semester_initial)) > 0:
        messages.error(request, "Error: You cannot create duplicate courses")
        return redirect('create-new-course')
    else:
        course_valid = True

    # Validations for co-professor
    co_prof_valid = False
    if co_professor_id != '':
        co_professor = User.objects.filter(eagle_id=co_professor_id).first()
        if co_professor is None:
            messages.error(request, "Error: You incorrectly entered the co-professor's Eagle ID")
            return redirect('create-new-course')
        elif not co_professor.is_instructor:
            messages.error(request, "Error: The co-professor's Eagle ID you entered is not a professor")
            return redirect('create-new-course')
        elif co_professor_id == request.user.eagle_id:
            messages.error(request, "Error: The co-professor's Eagle ID cannot be the same as your Eagle ID")
            return redirect('create-new-course')
        else:
            co_prof_valid = True
  
    if course_valid:
    # Create an instance of course
        course = Course(
                        course_name = course_name, 
                        course_code = course_code, 
                        section_number = section_number, 
                        year = year, 
                        semester = semester_initial,
                        )
        course.save()

    # Add to Many-to-Many field
    course.professors.add(professor)
    if co_prof_valid:
        course.professors.add(co_professor)
    course.save()

    messages.error(request, 'New course creation is successful')
    print("Create Course Success")
    return my_courses(request)


# Delete a course
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    messages.error(request, 'Course deleted')
    print("Course Deleted")
    return my_courses(request) # refresh page



def add_student(request, course_id):
    # This is add student to course. There is another function add_student_to_team
    id_or_email = request.POST['id or email']
    eagle_id = ''
    email = ''
    valid_student = False
    # check is it email format
    if regex_search(r'@bc.edu', id_or_email) is not None:  
        email = id_or_email  
    # check is it eagle id format       
    elif id_or_email.isdigit() and len(id_or_email) == 8:
        eagle_id = id_or_email
    else:
        messages.error(request, "Error: The format of email or Eagle ID is incorrect")
    
    # get course object
    course = get_object_or_404(Course, pk=course_id)

    # Validate the existance of the student
    if eagle_id != '':
        new_student = User.objects.filter(eagle_id = eagle_id).first()
        valid_student = True
    elif email != '':
        new_student = User.objects.filter(email = email).first()
        valid_student =True
    else:
        messages.error(request, "Error: Student is not found")
    
    if valid_student:
        course.students.add(new_student)
        course.save()
        print("student successfully added")

    return my_courses(request) # refresh page



def remove_student(request, course_id, eagle_id):
    course = Course.objects.get(pk=course_id)
    student = User.objects.get(eagle_id=eagle_id)
    course.students.remove(student)
    course.save()
    messages.error(request, "Student removed")
    return my_courses(request) # refresh page



# ----------------------------------- Team Section (functions below are for teams) --------------
def add_new_team(request):
    team_name = request.POST['team name']
    course_id = request.POST['course id']

    # Cap the first letter
    team_name = team_name[0].upper() + team_name[1:]

    # Validations
    team_valid = False

    # Check for duplicate names
    if len(Team.objects.filter(team_name=team_name)) > 0:
         messages.error(request, "Error: The team name you entered has already been taken")

    else:
        team_valid = True

    # Create an instance of team
    if team_valid:
        team = Team(
                    team_name = team_name, 
                    course = Course.objects.filter(id=course_id).first(), 
                    )
        team.save()

    return teams_students(request) # refresh page


# Delete a team
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    messages.error(request, 'Team deleted')
    return teams_students(request) # refresh page


# Add a student to a team
def add_student_to_team(request, team_id):
    name_id = request.POST['name_id']
    eagle_id = name_id[-8:]
    
    valid_student = False
    
    # get team object
    team = get_object_or_404(Team, pk=team_id)

    # Validate the existance of the student
    if eagle_id != '':
        new_student = User.objects.filter(eagle_id = eagle_id).first()
        valid_student = True
    else:
        messages.error(request, "Error: Student is not found")

    # Validate if the student is in the course
    if valid_student:
        if new_student not in team.course.students.all():
            messages.error(request, "Error: The student is not in this course")
            valid_student = False

    # Validate if the student is already in another team
    if valid_student:
        course = team.course # the course object
        team_list = Team.objects.filter(course=course) # list of teams in this course
        for each_team in team_list:
            if len(each_team.student.filter(eagle_id=eagle_id)) > 0:
                messages.error(request, "Error: This student is already in a team ({})".format(each_team.team_name))
                valid_student = False
    
    if valid_student:
        team.student.add(new_student)
        team.save()

    return teams_students(request) # refresh page


# remove a student from a team
def remove_student_from_team(request, team_id, eagle_id):
    team = Team.objects.get(pk=team_id)
    student = User.objects.get(eagle_id=eagle_id)
    team.student.remove(student)
    team.save()
    messages.error(request, "Student removed")
    return teams_students(request) # refresh page




# ----------------------------------- Assessment Section (functions below are for assessments) --------------
# Function: create a new assessment
def make_new_assessment(request):
    name = request.POST['Assessment name']
    description = request.POST['description']
    course_id = request.POST['course id']
    start_dt = request.POST['start date']
    end_dt = request.POST['end date']

    valid = False
    
    # Validate Date Format
    if regex_search(r'[0-9]+\-[0-9]+\-[0-9]+', start_dt) and regex_search(r'[0-9]+\-[0-9]+\-[0-9]+', end_dt):
        st_dt_list = start_dt.split('-')
        end_dt_list = end_dt.split('-')
        valid = True
    else:
        messages.error(request, "Error: Incorrect date format. Use yyyy-mm-dd")
        return make_new_assessment(request)

    if valid:
    # -----------if starts here -------------------------   
        # Create an instance of assessment
        assessment = Assessment(
                        name = name.title(), 
                        description = description, 
                        start_date = start_dt, 
                        end_date = end_dt, 
                        course = Course.objects.get(pk=course_id),
                        )
        assessment.save()
        
        # Add questions to the assessment
        idx = 0
        more_questions = True
        # while more_questions: # keeps checking if more questions
        for idx in range(1000):
            try:
                question_text = request.POST['question-{}'.format(idx)]
                answer_type = request.POST['answer type-{}'.format(idx)]
            except MultiValueDictKeyError: # this error means no more questions
                question_text = False
                answer_type = False
            if question_text == False: # if no more questions - break
                more_questions = False
                # break
            else:
                # Check which answer type
                if answer_type == "Free Response":
                    type_answer = Question.TYPE_TEXT
                else:
                    type_answer = Question.TYPE_Rating
                # Create an instance of question
                new_question = Question(
                                        question_text=question_text,
                                        type_answer=type_answer,
                                        )
                new_question.save()
                # Save this new question into the assessment's ManytoMany field
                assessment.questions.add(new_question)
                assessment.save()
            # # update counter
            # idx += 1

        messages.error(request, 'New assessment created')
    # ---------------if ends here-------------

    # messages.error(request, 'New course creation is successful!')

    return all_assessments(request) # go to all assessment page


# Delete an assessment
def delete_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id)
    assessment.delete()
    messages.error(request, 'Assessment deleted')
    return all_assessments(request) # refresh page


# Update start date and due date for assessment
def update_dates(request, assessment_id):
    start_dt = request.POST['start date']
    end_dt = request.POST['end date']

    valid = False
    
    # Validate Date Format
    if regex_search(r'[0-9]+\-[0-9]+\-[0-9]+', start_dt) and regex_search(r'[0-9]+\-[0-9]+\-[0-9]+', end_dt):
        st_dt_list = start_dt.split('-')
        end_dt_list = end_dt.split('-')
        valid = True
    else:
        messages.error(request, "Error: Incorrect date format. Use yyyy-mm-dd")

    if valid:
        assessment = get_object_or_404(Assessment, pk=assessment_id) # get the assessment instance
        assessment.start_date = start_dt
        assessment.end_date = end_dt
        assessment.save()

    return all_assessments(request) # refresh page


# Close assessment and release results
def close_and_release(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id) # get the assessment instance
    
    if assessment.start_date > datetime.datetime.now().date():
        messages.error(request, "Error: Cannot close an assessment that has not started")
        return all_assessments(request)

    assessment.open_status = False # when this is False, results will be released on student site
    assessment.save()

    # All students who did not complete the survey by this time
    # will auto receive 0
    # overriding what their teammates gave them
    not_completed_students = [student for student in assessment.course.students.all() if student not in assessment.completed_students.all()]

    for student in not_completed_students:

        if len(assessment.result_sets.filter(student=student)) == 0: # if such Result_set does not exist, create one
            for team in Team.objects.filter(course=assessment.course):
                if student in team.student.all():
                    the_team = team # team found
                    break
            # create the result_set
            result_set = Result_set(
                                student = student,
                                team = the_team,            
                        )
            result_set.save()

            for evaluator in team.student.all():
                if evaluator != student:
                    # add answers
                    for question in assessment.questions.all():
                        # create answer instances 
                        if question.type_answer == question.TYPE_Rating:
                            answer = Answer(
                                        question = question,
                                        evaluator = evaluator,
                                        team_member = student,
                                        answer_text = None,
                                        answer_rating = 0,
                                    )
                            answer.save()
                            # add the answer to the Result_set.rating_answers
                            result_set.rating_answers.add(answer)
                            result_set.save()
                        else:
                            answer = Answer(
                                        question = question,
                                        evaluator = evaluator,
                                        team_member = student,
                                        answer_text = None,
                                        answer_rating = None,
                                    )
                            answer.save()
                            # add the answer to the Result_set.text_answers
                            result_set.text_answers.add(answer)
                            result_set.save()
            # add the Result_set to this assessment
            assessment.result_sets.add(result_set)
            assessment.save()

        result_set = assessment.result_sets.filter(student=student).first()
        for answer in result_set.rating_answers.all():
            answer.answer_rating = 0
            answer.save()
        result_set.save()
        assessment.save()

    messages.error(request, "Assessment closed and results are now visible to students")
    return all_assessments(request) # refresh page


def download_csv(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id) # get the assessment instance
    file_name = "Results_" + assessment.name

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(file_name)

    writer = csv.writer(response)
    first_row = ['Eagle ID', 'Student Name']
    for question in assessment.questions.all():
        first_row.append(question.question_text)
    first_row.append('Average')
    writer.writerow(first_row)

    for result_set in assessment.result_sets.all():
        row = []
        # add name and eagle id
        row.append(result_set.student.eagle_id)
        row.append(result_set.student.get_full_name())

        for question in assessment.questions.all():
            if question.type_answer == question.TYPE_Rating:
                # add per-question score(average)
                scores = [answer.answer_rating for answer in result_set.rating_answers.all() if answer.question.id == question.id]
                row.append(round(np.mean(scores), 2))
            else:
                # add free response answers
                text = ''
                for answer in result_set.text_answers.all():
                    if answer.question.id == question.id and answer.get_answer() != None:
                        text += answer.get_answer()
                        text += '\n'
                row.append(text)

        # add average
        average = result_set.get_overall_avg_no_0()
        if isnan(average):
            average = 0
        row.append(average)
        writer.writerow(row)

    return response


def send_email_reminders(request, assessment_id):
    assessment = get_object_or_404(Assessment, pk=assessment_id) # get the assessment instance

    print("Send email reminders")
    EMAIL_ADDRESS = 'theEaglesInstructor@gmail.com'
    EMAIL_PASSWORD = 'jiujiu1016'
    #Check for students who havent completed assesment
    recipients = []


    if assessment.is_current and assessment.is_open:
        for student in assessment.course.students.all():
            if student not in assessment.completed_students.all():
                recipients.append(student)

    for r in recipients:
        print(r.email)
        msg = EmailMessage()
        msg['Subject'] = 'REMINDER: Complete {} [DO NOT REPLY]'.format(assessment.name)
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = r.email
        print("Hello "+ r.first_name + ", please complete " + assessment.name)
        msg.set_content("Hi {}, please complete {}.".format(r.first_name, assessment.name))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email reminder sent")

    #Collect emails of students 

    #Send emails to students 
    messages.error(request, "Reminders sent successfully")
    return all_assessments(request)
