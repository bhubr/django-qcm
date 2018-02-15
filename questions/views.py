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
        return redirect('/?done=1&name=' + request.POST['nom'])
    else:
        data = ""

    questions = Question.objects.all()
    done = request.GET.get('done', '')
    name = request.GET['name'] if done else ''
    return render(request, 'home.html', { 'questions': questions, 'data': data, 'done': done, 'name': name })
