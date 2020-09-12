from django.shortcuts import render,get_object_or_404, redirect
from .models import Room,Teachercreate,Studentjoin,Comment,CommentAnswer,Quiz,Answer,Question,Dashboard,Assignment,Studentsolution,Gradeassignment,Announcement
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,RedirectView
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView,DeleteView,View
from django.core.exceptions import ObjectDoesNotExist
from .forms import ClassroomForm,CommentForm,CommentAnswerForm,QuestionForm,BaseAnswerInlineFormSet,AssignmentForm,GradeForm
from django.contrib import messages
from django.db.models import Avg, Count
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.contrib.auth.decorators import login_required

@login_required 
def create_classroom(request):
    if request.method=='POST':
        form=ClassroomForm(request.POST)
        if form.is_valid():
            form.instance.teacher=request.user
            form.save()
            return redirect('/')
    else:
        form = ClassroomForm()
    return render(request,'classroom/create_classroom.html',{
        
        'form':form
        })

class ClassroomDetailView(LoginRequiredMixin,DetailView):
    model= Teachercreate
    template_name = "classroom/classroom_detail.html"

class RoomDetailView(LoginRequiredMixin,DetailView):
    model= Teachercreate
    template_name = "classroom/room_detail.html"

class RoomDetailQuizView(LoginRequiredMixin,DetailView):
    model= Teachercreate
    template_name = "classroom/room_detail_quiz.html"

class RoomDetailAssignmentView(LoginRequiredMixin,DetailView):
    model= Teachercreate
    template_name = "classroom/room_detail_assignment.html"

class RoomDetailAnnouncementView(LoginRequiredMixin,DetailView):
    model= Teachercreate
    template_name = "classroom/room_detail_announcement.html"

@login_required 
def StudentJoint(request):
    try:
        if request.method == 'POST':
            data = request.POST
            datas = dict(data)
            text= datas['text'][0]
            item= Teachercreate.objects.get(code=text)
            print(item.id)

            context={
                'item':item
            }
            return redirect("product",pk=item.id)
    except ObjectDoesNotExist:
            messages.warning(request,"code doesnot exist")
            return redirect("/add/")
    return render(request, 'classroom/join.html')  

@login_required 
def add_to_cart(request, pk):
    item =get_object_or_404(Teachercreate, pk=pk)
    order_item, created=Room.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs=Studentjoin.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():  
           
            messages.info(request,"You have already joined the classroom")
            return redirect("order-summary")
        else:
            messages.info(request,"You have joined the classroom")
            order.items.add(order_item)
            return redirect("order-summary")
    else:
        
        order = Studentjoin.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request,"You have already joined the classroom")
        return redirect("order-summary")





def remove_from_cart(request,pk):
    item=get_object_or_404(Teachercreate,pk=pk)
    order_qs=Studentjoin.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item =Room.objects.filter(
                 item=item,
                 user=request.user,
                 ordered=False
            )[0]           
            order.items.remove(order_item)
            messages.info(request,"You sucessfully unenrolled fron this classroom")
            return redirect("order-summary")
        else:
            messages.info(request,"you haven't enrolled in the clssroom")
            return redirect("order-summary")
    else:
        messages.info(request,"you haven't enrolled in the clssroom")
        return redirect("order-summary")

class ClassroomSummaryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            t=Teachercreate.objects.filter(teacher=self.request.user)
            print(t)
            room = Studentjoin.objects.get(user=self.request.user,ordered=False)
            print(room)
            context={
                'object':room,
                'teacher': t
                }
            return render(self.request,'classroom/classroom_summary.html',context)
        except ObjectDoesNotExist:
            t=Teachercreate.objects.filter(teacher=self.request.user)
            context={
                'object':None,
                'teacher': t
                }
            messages.error(self.request,"YOU havent joined any classroom")
            return render(self.request,'classroom/classroom_summary.html',context)

@login_required 
def add_comment_to_room(request, pk):
    item = get_object_or_404(Teachercreate, pk=pk)
    form=CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.item = item
            form.instance.user=request.user
            form.save()
            return redirect('detail', pk=item.pk)
    else:
        form = CommentForm()
    return render(request, 'classroom/add_comment_to_room.html', {'form': form})

class CommentDetailView(LoginRequiredMixin,DetailView):
    model= Comment


@login_required   
def add_answer_to_comment(request, pk):
    item = get_object_or_404(Comment, pk=pk)
    form=CommentAnswerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.item = item
            form.instance.user=request.user
            form.save()
            return redirect('comment_detail', pk=item.pk)
    else:
        form = CommentForm()
    return render(request, 'classroom/add_answer_to_comment.html', {'form': form})


    #Quiz


class QuizCreateView(LoginRequiredMixin,CreateView):
    model = Quiz
    fields = ( 'subject','topic' )
    template_name = 'classroom/quiz_add_form.html'
    

    def form_valid(self, form):
        form.instance.item_id = self.kwargs.get('pk')

        quiz = form.save(commit=False)
        
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('quiz_change', quiz.pk)



class QuizUpdateView(LoginRequiredMixin,UpdateView):
    model = Quiz
    fields = ( 'subject','topic' )
    context_object_name = 'quiz'
    template_name = 'classroom/quiz_change_form.html'
    
    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('quiz_change', kwargs={'pk': self.object.pk})


@login_required 
def question_add(request, pk):
 
    quiz = get_object_or_404(Quiz, pk=pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'classroom/question_add_form.html', {'quiz': quiz, 'form': form})



@login_required 
def question_change(request, quiz_pk, question_pk):

    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'classroom/add_answer.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })



def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions =Question.objects.filter(quiz__id=pk)
    answers = Answer.objects.filter(question__quiz__id=pk)
    student = request.user
    if Dashboard.objects.filter(student_id=student).exists() and Dashboard.objects.filter(quiz__id=pk).exists():
        messages.warning(request, 'You have already given quiz. You cannot give it again')
       
        return render(request,'classroom/already_taken.html')
    return render(request, 'classroom/take_quiz_form.html', {
        'quiz': quiz,
        'questions': questions,
        'answers':answers
        
    })

def result(request,pk):
    answers = Answer.objects.filter(question__quiz__id=pk)
    quiz = get_object_or_404(Quiz, pk=pk)
    print("result page")
    if request.method == 'POST':
        data = request.POST
        datas = dict(data)
        print(datas)
        qid = []
        qans = []
        ans = []
        score = 0
        for key in datas:

            try:
               
                qid.append(int(key))
                qans.append(datas[key][0])
            except:
                print("Csrf")
        #for q in qid:
         #   ans.append((Questions.objects.get(id = q)).answer)

        for answer in answers:
            
            if answer.is_correct:

                ans.append(answer.text)
        print(ans)       
        total = len(ans)
        for i in range(total):
            if ans[i] == qans[i]:
                score += 1
        # print(qid)
        # print(qans)
        # print(ans)
        print(score)
        eff = (score/total)*100
        student = request.user
        Dashboard.objects.create(student=student, quiz=quiz, score=score, total=total)

   
    return render(request,
        'classroom/result.html',
        {'score':score,
        'eff':eff,
        'total':total,

        })

def TakenQuizListView(request,pk):
     dashboards=Dashboard.objects.filter(quiz__id=pk)    
     
     return render(request,'classroom/taken_quiz_list.html',{
        'dashboards' :dashboards
     })  


class AssignmentCreateView(CreateView):
    model = Assignment
    fields = ( 'pdf','description' )
    template_name = 'classroom/assignment_add_form.html'
    

    def form_valid(self, form):
        form.instance.item_id = self.kwargs.get('pk')
        pk=self.kwargs.get('pk')
        form.save()
        messages.success(self.request, 'Assignment is created')
        return redirect('detail', pk)


def solution_assignment(request,pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method=='POST':
        form=AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user= request.user
            form.instance.ass= assignment
            form.save()
            return redirect('detail', assignment.item.pk )
    else:
        form = AssignmentForm()
    return render(request,'classroom/upload_Assignment.html',{
        'form':form
        })

def TakenAssignmentListView(request,pk):
     solutions =Studentsolution.objects.filter(ass__id=pk)
        
     
     return render(request,'classroom/taken_assignment_list.html',{
       'solutions' :solutions,
       
       
    })  


def GradeAssignment(request,pk):
     ass_sol = get_object_or_404(Studentsolution, pk=pk)
     
     if Gradeassignment.objects.filter(sol_id=ass_sol).exists():
        grade = get_object_or_404(Gradeassignment,sol_id=ass_sol)
        print(grade)
        form =GradeForm(request.POST or None, instance=grade)
        if form.is_valid():
            form.instance.sol=ass_sol
            form.save()
        return render(request,'classroom/grade_assignment.html',{
       'ass_sol' : ass_sol,
       'form': form

    }) 
     if request.method=='POST':
        print(request.POST)
        form=GradeForm(request.POST)
        if form.is_valid():
            form.instance.sol=ass_sol
            form.save()
            return redirect('ass_dashboard',ass_sol.ass.pk )
     else:
        form = GradeForm()    
     
     return render(request,'classroom/grade_assignment.html',{
       'ass_sol' : ass_sol,
       'form':form
    })  

def classmates(request,pk):
    student=Room.objects.filter(item_id=pk)
    teacher=Teachercreate.objects.get(pk=pk)
    context={
        'students':student,
        'teacher':teacher
    }
    return render(request,'classroom/classmates.html',context)

class RoomDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model= Teachercreate
    template_name='classroom/item_confirm_delete.html'
    success_url='/'
    def test_func(self):
        item=self.get_object()
        if self.request.user == item.teacher:
            return True
        return False



class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'classroom/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)


    def get_success_url(self):
        question = self.get_object()
        return reverse('quiz_change', kwargs={'pk': question.quiz_id})


class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/quiz_delete_confirm.html'
   
    def get_success_url(self):
        return reverse_lazy('detail_Quiz',kwargs={'pk': self.object.item.pk})
    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.info(request, 'The quiz was deleted with success!')
        return super().delete(request, *args, **kwargs)


class AnnouncementCreateView(CreateView):
    model = Announcement
    fields = ('title','description','docs','link' )
    template_name = 'classroom/announcement_add_form.html'
    

    def form_valid(self, form):
        form.instance.item_id = self.kwargs.get('pk')
        pk=self.kwargs.get('pk')
        form.save()
        messages.warning(self.request, 'Anouncement is created')
        return redirect('detail_announcement', pk)    
