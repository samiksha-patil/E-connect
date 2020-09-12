from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Teachercreate(models.Model):
    #Item
    teacher= models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    code= models.CharField(max_length=100,unique=True)  

    def __str__(self):
        return str(self.teacher)

    def get_add_to_cart_url(self):
     return reverse('add_to_cart', kwargs={
            'pk':self.pk
            })

    

class Room(models.Model):
    #/orderItem
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Teachercreate, on_delete=models.CASCADE)
    
    ordered=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{ self.item.code }"

class Studentjoin(models.Model):
    #Order
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items =models.ManyToManyField(Room)
    
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('product', kwargs={
            'pk':self.pk
            })


class Comment(models.Model):
    item = models.ForeignKey(Teachercreate, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('product',kwargs={'pk': self.pk})

class CommentAnswer(models.Model):
    item = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('comment_detail',kwargs={'pk': self.pk})


#Quiz
class Quiz(models.Model):
    subject= models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    item = models.ForeignKey(Teachercreate, on_delete=models.CASCADE, related_name='quiz')
    def __str__(self):
        return self.topic

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text=models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text
class Answer(models.Model):
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text= models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Dashboard(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='+')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField() 
    def __str__(self):
        return str(self.student)

class Assignment(models.Model):
    item=models.ForeignKey(Teachercreate, on_delete=models.CASCADE,related_name='assignment')
    pdf= models.FileField(upload_to='assignments/')
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.item.teacher)

class Studentsolution(models.Model):
    ass=models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='sol_assignment')
    pdf= models.FileField(upload_to='assignmets/solution')
    created_date = models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)


class Gradeassignment(models.Model):
    sol=models.ForeignKey(Studentsolution, on_delete=models.CASCADE, related_name='grade_assignment')
    grade = models.FloatField()
    total = models.FloatField() 
    def __str__(self):
        return str(self.sol.user)

class Announcement(models.Model):
    item = models.ForeignKey(Teachercreate, on_delete=models.CASCADE, related_name='annnouncement')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    docs= models.FileField(upload_to='announcement/docs',null=True,blank=True)
    link=models.URLField(max_length=200,null=True,blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.title)