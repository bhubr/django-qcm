from django.shortcuts import redirect, render
from questions.models import Question, Answer, StudentSubmission
import json

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        data = json.dumps(request.POST)
        print(data)
        StudentSubmission.objects.create(
          name=request.POST['nom'],
          email=request.POST['email'],
          data=data
        )
        return redirect('/')
    else:
        data = ""

    questions = Question.objects.all()
    return render(request, 'home.html', { 'questions': questions, 'data': data })

def view_list(request, username):
    print(request.user.id if request.user else 'no auth')
    movies = Movie.objects.all().filter(user_id=request.user.id)
    return render(request, 'library.html', {'movies': movies})
