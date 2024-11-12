import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for filling entities')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']

        users = [User(username=f'user_{_}_{random.randint(1000, 9999)}') for _ in range(ratio)]
        for user in users:
            user.set_password('password')
            user.save()
        # User.objects.bulk_create(users)

        # profiles = [Profile(user=user) for user in users]
        # Profile.objects.bulk_create(profiles)
        for user in users:
            profile = Profile(user = user)
            profile.save()

        saved_profiles = Profile.objects.all()


        for _ in range(ratio):
            tag = Tag(name=f'tag_{_}')
            tag.save()

        # tags = [Tag(name=f'tag_{_}') for _ in range(ratio)]
        # Tag.objects.bulk_create(tags)

        saved_tags = set(Tag.objects.all())


        for _ in range(ratio * 10):
            author = random.choice(saved_profiles)  
            question = Question(author=author, title=f'Question title {_}', text='This is a test question.')
            question.save()

        saved_questions = Question.objects.all()


        for question in saved_questions:
            tags_to_add = random.sample(saved_tags, random.randint(1, 5))
            question.tags.set(tags_to_add)


        for _ in range(ratio * 100):
            question = random.choice(saved_questions)
            author = random.choice(saved_profiles)  
            answer = Answer(author=author, question=question, text='This is a test answer.')
            answer.save()

        saved_answers = Answer.objects.all()


        key_set = set(QuestionLike.objects.all())
        for _ in range(ratio * 200):
            question = random.choice(saved_questions)
            user = random.choice(saved_profiles)  
            key = (user.id, question.id)
            if key not in key_set:
                key_set.add(key)
                like = QuestionLike(user=user, question=question)
                like.save()


        key_set = set(AnswerLike.objects.all())
        for _ in range(ratio * 200):
            answer = random.choice(saved_answers)
            user = random.choice(saved_profiles)
            key = (user.id, answer.id)
            if key not in key_set:
                key_set.add(key)
                like = AnswerLike(user=user, answer=answer)
                like.save()

        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))