from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.annotate(like_count=Count('questionlike')).order_by('-created_at')

    def like_count(self, question):
        return QuestionLike.objects.filter(question=question).count()

    def sorted_by_likes(self):
        return self.annotate(like_count=Count('questionlike')).order_by('-like_count', '-created_at')
    
    def get_tags(self, tag):
        return self.annotate(like_count=Count('questionlike')).filter(tags = tag).order_by('-created_at')

class AnswerManager(models.Manager):
    def answers(self):
        return self.annotate(like_count=Count('answerlike')).order_by('-created_at')

    def like_count(self, answer):
        return AnswerLike.objects.filter(answer=answer).count()

    def sorted_by_likes(self):
        return self.annotate(like_count=Count('answerlike')).order_by('-like_count', '-created_at')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="uploads", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='questions')
    title = models.CharField(max_length=256)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = QuestionManager()  


    @property
    def answer_count(self):
        return self.answers.count() 

    def __str__(self):
        return self.title

class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AnswerManager()

    def __str__(self):
        return f'Answer by {self.author.user.username} to {self.question.title}'

class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f'Like from {self.user.user.username} to {self.question.title}'

class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f'Like from {self.user.user.username} to {self.answer}'