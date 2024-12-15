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

        # self.stdout.write(self.style.SUCCESS('Saving users'))
        # users = [User(username=f'user_{_}_{random.randint(1000, 9999)}') for _ in range(ratio)]
        # for user in users:
        #     user.set_password('password')
        # User.objects.bulk_create(users)
        # self.stdout.write(self.style.SUCCESS('Successfully saved users'))
        
        # saved_users = User.objects.all()

        # self.stdout.write(self.style.SUCCESS('Saving profiles'))
        # profiles = [Profile(user=user) for user in saved_users]
        # Profile.objects.bulk_create(profiles)
        # self.stdout.write(self.style.SUCCESS('Successfully saved profiles'))

        saved_profiles = Profile.objects.all()

        # self.stdout.write(self.style.SUCCESS('Saving tags'))
        # tags = [Tag(name=f'tag_{_}') for _ in range(ratio)]
        # Tag.objects.bulk_create(tags)
        # self.stdout.write(self.style.SUCCESS('Successfully saved tags'))

        # saved_tags = list(Tag.objects.all())

        # questions = []
        # for _ in range(ratio * 10):
        #     author = random.choice(saved_profiles)  
        #     question = Question(author=author, title=f'Question title {_}', text='This is a test question.')
        #     questions.append(question)
        #     self.stdout.write(self.style.SUCCESS(f'Successfully saved question №{_})'))

        # Question.objects.bulk_create(questions)
        saved_questions = list(Question.objects.all())

        # self.stdout.write(self.style.SUCCESS('Adding tags to questions'))

        # for question in saved_questions:
        #     tags_to_add = random.sample(saved_tags, random.randint(1, 5))
        #     question.tags.set(tags_to_add)

        answers = []
        for _ in range(ratio * 100):
            question = random.choice(saved_questions)
            author = random.choice(saved_profiles)
            answer = Answer(author=author, question=question, text='This is a test answer.')
            answers.append(answer)
            if (_ % 10000 == 0):
                Answer.objects.bulk_create(answers)
                answers = []
            self.stdout.write(self.style.SUCCESS(f'Successfully saved answer №{_})'))

        Answer.objects.bulk_create(answers)
        saved_answers = list(Answer.objects.all())


        key_set_question = {(like.user.id, like.question.id) for like in QuestionLike.objects.all()}
        question_likes = []
        for _ in range(ratio * 200):
            question = random.choice(saved_questions)
            user = random.choice(saved_profiles)
            key = (user.id, question.id)
            if key not in key_set_question:
                key_set_question.add(key)
                question_likes.append(QuestionLike(user=user, question=question))
                self.stdout.write(self.style.SUCCESS(f'Successfully saved QuestionLike №{_})'))

        QuestionLike.objects.bulk_create(question_likes)
        self.stdout.write(self.style.SUCCESS(f'Successfully saved {len(question_likes)} QuestionLikes'))


        key_set_answer = {(like.user.id, like.answer.id) for like in AnswerLike.objects.all()}
        answer_likes = []
        for _ in range(ratio * 200):
            answer = random.choice(saved_answers)
            user = random.choice(saved_profiles)
            key = (user.id, answer.id)
            if key not in key_set_answer:
                key_set_answer.add(key)
                answer_likes.append(AnswerLike(user=user, answer=answer))
                self.stdout.write(self.style.SUCCESS(f'Successfully saved AnswerLike №{_})'))

        AnswerLike.objects.bulk_create(answer_likes)
        self.stdout.write(self.style.SUCCESS(f'Successfully saved {len(answer_likes)} AnswerLikes'))

        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))