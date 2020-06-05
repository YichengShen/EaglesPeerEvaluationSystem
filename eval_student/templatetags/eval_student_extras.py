from django import template

from registration.models import Course, Team
from assessment.models import Assessment, Question, Result_set
from account.models import User

import numpy as np

register = template.Library()


@register.simple_tag
def get_eval_list(assessment, current_user):
    """Returns the list of teammates who are evaluated"""
    for team in Team.objects.all():
        if current_user in team.student.all() and team.course == assessment.course: # get the team
            evaluated_list = [student for student in team.student.all() if student != current_user]
    return evaluated_list


@register.simple_tag
def get_answer_list(assessment, student, current_user):
    """Returns a list of answers for the student"""
    result_set = assessment.result_sets.filter(student=student).first()
    answer_list = []
    for answer in result_set.rating_answers.all():
        if answer.evaluator == current_user:
            answer_list.append(answer)
    for answer in result_set.text_answers.all():
        if answer.evaluator == current_user:
            answer_list.append(answer)
    return answer_list


@register.simple_tag
def find_result_set(result_sets, student, course):
    """Returns the Result_set instance of the given student in the given team"""
    # find the team that the student is in
    for team in Team.objects.filter(course=course).all():
        if student in team.student.all():
            the_team = team
            break
    return result_sets.filter(student=student, team=the_team).first()


@register.simple_tag
def get_per_question_average(result_set, q_id):
        scores = [answer.answer_rating for answer in result_set.rating_answers.all() if answer.question.id == q_id] # a list of scores of that question
        return round(np.mean(scores), 2)

@register.simple_tag
def get_free_response(result_set, q_id):
        text = ''
        for answer in result_set.text_answers.all():
            if answer.question.id == q_id and answer.get_answer() != None:
                text += answer.get_answer()
                text += ';'
        return text