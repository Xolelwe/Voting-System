from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Poll, Choice, SurveyResponse

def ensure_default_poll():
    poll, created = Poll.objects.get_or_create(
        title='Accessibility Priorities',
        defaults={'accessibility_note': 'Vote on accessibility areas for learners.'}
    )
    default_choices = ['Accessible Transport', 'Inclusive Education', 'Assistive Technology', 'Healthcare Accessibility', 'Digital Inclusion']
    for c in default_choices:
        Choice.objects.get_or_create(poll=poll, choice_text=c)
    return poll

def welcome(request):
    poll = Poll.objects.first()  # or whatever poll you want
    return render(request, "polls/welcome.html", {"poll": poll})

def menu(request):
    poll = Poll.objects.first()
    return render(request, 'polls/menu.html', {'poll': poll})

def vote_page(request):
    poll = Poll.objects.first()
    return render(request, 'polls/vote.html', {'poll': poll})

@require_POST
def submit_vote(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    choice.votes += 1
    choice.save()
    return redirect('polls:results')

def survey_page(request):
    questions = [
        "Are schools accessible for students with disabilities?",
        "Do workplaces provide reasonable accommodations?",
        "Is public transport disability-friendly?",
        "Do you have access to assistive technology?",
        "Are healthcare facilities inclusive?",
    ]
    return render(request, 'polls/survey.html', {'questions': questions})

@require_POST
def submit_survey(request):
    answers = {k: v for k, v in request.POST.items() if k.startswith('q')}
    SurveyResponse.objects.create(answers=answers)
    return redirect('polls:results')

def results(request):
    poll = Poll.objects.first()
    choices = poll.choice_set.all()
    surveys = SurveyResponse.objects.order_by('-created')[:20]
    return render(request, 'polls/results.html', {'poll': poll, 'choices': choices, 'surveys': surveys})

def welcome(request):
    return render(request, 'polls/welcome.html')