from django import template

from registration.models import Course, Team
from assessment.models import Assessment, Question, Result_set
from account.models import User

import numpy as np
from math import isnan

register = template.Library()


@register.simple_tag
def get_class_average(course, assessment):
    """Returns the average score of the class"""
    return round(np.mean([result_set.get_overall_average() for result_set in assessment.result_sets.all()]), 2)


@register.simple_tag
def get_class_avg_no_0(course, assessment):
    """Returns the average score of the class (excluding 0s)"""
    scores = [result_set.get_overall_avg_no_0() for result_set in assessment.result_sets.all()]
    scores_no_nan = [score for score in scores if not isnan(score)]
    return round(np.mean(scores_no_nan), 2)


@register.simple_tag
def get_class_std_no_0(course, assessment):
    """Returns the standard deviation of the class (excluding 0s)"""
    scores = [result_set.get_overall_avg_no_0() for result_set in assessment.result_sets.all()]
    scores_no_nan = [score for score in scores if not isnan(score)]
    return round(np.std(scores_no_nan, ddof=1), 2)



@register.simple_tag
def get_team_average(team, assessment):
    """Returns the average score of the team"""
    result_set_list = [result_set for result_set in assessment.result_sets.filter(team=team).all()]
    return round(np.mean([result_set.get_overall_average() for result_set in result_set_list]), 2)


@register.simple_tag
def find_result_set(result_sets, student, team):
    """Returns the Result_set instance of the given student in the given team"""
    return result_sets.filter(student=student, team=team).first()


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
