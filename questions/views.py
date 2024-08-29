from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.contrib import messages
from .forms import UserRegistrationForm, QuestionRegisterForm, AnswerForm, QuestionUpdateForm, AnswerUpdateForm, ProfileForm
from django.contrib.auth.decorators import login_required
from prometheus_client import Counter, Histogram

 # Initialize answer counter
answer_count = Counter('answer_count', 'Number of answers')

# Initializing question counter
question_counter = Counter('question_counter', 'Number of questions created')


@login_required
def question_list(request):
    if 'q' in request.GET:
        q = request.GET['q']
        question_lister = Question.objects.filter(title__icontains=q).order_by('-created_at')
        
    else:
        question_lister = Question.objects.all().order_by('-created_at')
    return render(request, 'QList.html', {"question_lister": question_lister})

@login_required
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

            # increment answer counter
            answer_count.inc()
            return redirect('qdetails', slug=question.slug)
        
    else:
        form = AnswerForm()
    return render(request, 'QDetails.html', {'question': question, 'answer_list': answer_list, 'form': form, 'answer_count': answer_count})

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


# Define Histogram for request latency
QUESTION_CREATION_LATENCY = Histogram(
    'question_creation_latency_seconds',
    'Latency of HTTP requests for creating questions',
    buckets=[0.1, 0.5, 1, 2.5, 5, 10]
)

@login_required
def create_question(request):
    # Initialize histogram for request latency
    with QUESTION_CREATION_LATENCY.time():
        if request.method == "POST":
            question_form = QuestionRegisterForm(request.POST)

            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.author = request.user
                question = question_form.save()

                # Increment question counter
                question_counter.inc()


                return redirect('qlist')
        else:
            question_form = QuestionRegisterForm()
        return render(request, 'add_question.html', {"question_form": question_form, "question_counter": question_counter})


@login_required
def update_question(request, slug):
    oldquestion = get_object_or_404(Question, slug=slug)


    update_form = QuestionUpdateForm(request.POST or None, instance=oldquestion)

    if update_form.is_valid():
        update_form.save()
        return redirect('qlist')
        
    return render(request, 'update.html', {"form": update_form})

@login_required
def delete_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    question.delete()
    return redirect('qlist')

@login_required
def update_answer(request, id):
    answer = get_object_or_404(Answer, id=id)

    form = AnswerUpdateForm(request.POST or None, instance=answer)

    if form.is_valid():
        form.save()
        return redirect('qdetails', slug=answer.question.slug)
    return render(request, 'update_question.html', {"form": form})

@login_required
def delete_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    answer.delete()
    return redirect('qdetails', slug = answer.question.slug)

@login_required
def change_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    form = ProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

@login_required
def list_info(request):
    questions = Question.objects.filter(author = request.user).order_by('-created_at')
    answers = Answer.objects.filter(author = request.user).order_by('-created_at')
    return render(request, 'list_info.html', {'questions': questions, 'answers': answers})