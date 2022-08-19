from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Question
from .forms import QuestionForm

# Create your views here.

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)


def question_create(request):
    if request.method == 'POST':  # '질문 등록' 화면에서 [저장하기] 버튼을 누른 경우 -> 질문 내용을 데이터베이스에 저장해야 함.
        form = QuestionForm(request.POST)
        # request.POST를 인수로 QuestionForm을 생성할 경우에는
        # request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성된다.
        if form.is_valid():
            question = form.save(commit=False)  # 임시저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:  # '질문 목록' 화면에서 [질문 등록하기] 버튼을 누른 경우
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

