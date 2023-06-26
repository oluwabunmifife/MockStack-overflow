from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import UserRegistrationForm, QuestionRegisterForm, AnswerForm

# Create your views here.
def question_list(request):
    question_lister = Question.objects.all().order_by('-created_at')
    return render(request, 'QList.html', {"question_lister": question_lister})

def question_details(request, slug):
    question = get_object_or_404(Question, slug=slug)
    answer_list = Answer.objects.filter(question=question)

    #Adding answers


    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer = form.save()

            return redirect('qdetails', slug=question.slug)
        
    else:
        form = AnswerForm()
    return render(request, 'QDetails.html', {'question': question, 'answer_list': answer_list, 'form': form})

def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])

            new_user.save()
            return render(request, "register_done.html", {"user_form": user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request, "register.html", {"user_form": user_form})

def create_question(request):
    if request.method == "POST":
       question_form = QuestionRegisterForm(request.POST)

       if question_form.is_valid():
           question = question_form.save(commit=False)
           question.author = request.user
           question = question_form.save()

           return redirect('qlist')
    else:
        question_form = QuestionRegisterForm()
    return render(request, 'add_question.html', {"question_form": question_form})