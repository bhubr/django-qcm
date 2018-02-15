from django.shortcuts import redirect, render
from questions.models import Question, Answer

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Question.objects.create(question=request.POST['question-text'])
        return redirect('/')

    questions = Question.objects.all()
    return render(request, 'home.html', { 'questions': questions, 'name': 'Guest' })

def view_list(request, username):
    print(request.user.id if request.user else 'no auth')
    movies = Movie.objects.all().filter(user_id=request.user.id)
    return render(request, 'library.html', {'movies': movies})
