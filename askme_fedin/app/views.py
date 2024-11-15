import copy
import random
from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile,Tag,Question,Answer,QuestionLike, AnswerLike

QUESTIONS = [
   {
        'title': f'Totally real person #{i}',
        'id': i,
        'text': f'I am person #{i} and I love communism. I dont know how to tell ny crush but I really like it ',
        'tags': [f'tag{i % 5}', f'tag{i % 3}',  f'tag{i % 10}'],
        'like': random.randint(-20, 100),
        'answers_cnt': 4,
        'answers': [
            {
                'text': f'I am answer #{j} to question #{i} and I understand you',
                'answer_like': random.randint(0, 20)  
            }
            for j in range(0, 4)
        ]
   } for i in range(0,50)
]


def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)

    paginator = Paginator(objects_list, per_page)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

def index(request):
    questions = Question.objects.new_questions()
    page = paginate(questions, request, per_page=5)
    return render(request, 'index.html', context={'questions': page.object_list, "page_obj": page})

def hot(request):
    questions = Question.objects.sorted_by_likes()
    page = paginate(questions, request, per_page=5)
    return render(request, 'hot.html', context={'questions': page.object_list, "page_obj": page})

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    tag_questions = Question.objects.get_tags(tag)
    page = paginate(tag_questions, request, per_page=5)
    return render(request, 'tags.html', context={'questions': page.object_list, "page_obj": page, 'tag_name': tag.name})

def one_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.answers()
    page = paginate(answers, request, per_page=3)  
    return render(request, 'answers.html', context={'question': question,'likes': Question.objects.like_count(question), 'page_obj': page, "answers": answers})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

