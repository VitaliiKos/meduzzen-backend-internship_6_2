from collections import defaultdict

from django.db.models import Max

from apps.companies.models import CompanyModel
from apps.quizzes.models import QuizModel
from apps.quizzes.quiz_workflow.models import QuizResultModel


def get_quizzes_with_last_completions(company_id: int):
    """List of quizzes and the time if it’s last completions.(2)"""

    quizzes_list = QuizResultModel.objects.filter(company_id=company_id).values(
        'quiz__id',
        'quiz__title',
        'quiz__company',
    ).annotate(last_created_at=Max('created_at')).order_by('-last_created_at')

    return quizzes_list


def get_average_scores_by_quiz_and_company_over_time():
    """List of average scores for each of the quiz from all companies with dynamics over time.(3)"""
    unique_quizzes = QuizModel.objects.values('id', 'title', 'company_id')

    quiz_results = []
    for quiz in unique_quizzes:
        attempts = (
            QuizResultModel.objects
            .filter(quiz_id=quiz['id'], company_id=quiz['company_id'])
            .values('score', 'created_at')
            .order_by('-created_at')
        )
        formatted_attempts = [
            {
                'score': attempt['score'],
                'created_at': attempt['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            }
            for attempt in attempts
        ]
        quiz_data = {
            'quiz': quiz['id'],
            'company': quiz['company_id'],
            'attempts': formatted_attempts
        }
        quiz_results.append(quiz_data)

    return quiz_results


def get_attempt_results_for_users():
    """List of average scores of all users with dynamics over time.(4)"""

    attempt_results = defaultdict(list)
    all_attempt_results = QuizResultModel.objects.all()

    for result in all_attempt_results:
        attempt_data = {
            'score': result.score,
            'created_at': result.created_at.strftime('%Y, %m, %d')
        }

        attempt_results[result.user_id].append(attempt_data)

    return [{'user': user_id, 'attempt': attempts} for user_id, attempts in attempt_results.items()]


def get_average_scores_by_quizzes_for_user(user_id: int):
    """List of average scores for all quizzes of the selected user with dynamics over time.(5)"""

    user_quizzes_result = (QuizResultModel.objects
                           .filter(user=user_id)
                           .values('quiz', 'user', 'company', 'score', 'created_at')
                           .order_by('quiz', 'created_at')
                           )

    grouped_quiz_results = {}
    for attempt in user_quizzes_result:
        quiz_id = attempt['quiz']
        company = attempt['company']
        user = attempt['user']
        score = attempt['score']
        created_at = attempt['created_at'].strftime('%Y, %m, %d')

        if quiz_id not in grouped_quiz_results:
            grouped_quiz_results[quiz_id] = {'quiz': quiz_id, 'user': user, 'company': company, 'attempt': []}

        grouped_quiz_results[quiz_id]['attempt'].append({'score': score, 'created_at': created_at})
    return grouped_quiz_results


def members_last_attempt(company: CompanyModel):
    """List of users of the company and their time of last completions.(6)"""

    company_members = company.get_members()

    members_list = []
    for member in company_members:
        user_quiz_results = (QuizResultModel.objects
                             .filter(user=member.user, company=company)
                             .order_by('-created_at')
                             .first())
        members_list.append(
            {'member': member.user.email,
             'last_timestamp': user_quiz_results.created_at if user_quiz_results else None})

    return members_list
