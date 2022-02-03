from django.shortcuts import redirect, render, HttpResponse,get_object_or_404
from pybo.models import Question,Answer
from django.utils import timezone
from .forms import QuestionForm
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    page = request.GET.get('page', '1') # 페이지

    question_list = Question.objects.order_by("-create_date")
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
 
    return render(request, 'pybo/question_list.html', context)
    
def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)

    context = {'question' : question}
    return render(request, 'pybo/question_detail.html',context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    content =request.POST.get('content')
    #방법1]
    # answer = Answer(question = question, content =content, create_date = timezone.now())

    # answer.save()
    #방법2] foreignkey 관계인 경우
    question.answer_set.create(content = content,
                            create_date=timezone.now())
    return redirect('pybo:detail',question_id=question_id)

def question_create(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

def answer_create(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
