import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    
    def test_was_puplished_recently_with_future_questions(self):
        """Must return False for questions whose pub_date is in the future"""    
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(question_text="Question in the future?",pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """
            Must must return false for questions published in the past
        """
        time = timezone.now() - datetime.timedelta(days = 3) 
        q = Question(question_text = "Question in the past?", pub_date = time)
        self.assertFalse(q.was_published_recently())
        

    def test_was_published_recently_with_present_questions(self):
        """
            Must return True for questions published in the present
        """
        self.assertTrue(Question(question_text = "Question in the present?", pub_date = timezone.now()).was_published_recently())


def create_question(question_text, days_offset):
    """
    Creates a question with the given "question_text" and set a time offset.
    positive for questions in the future
    negative for questions in the paset
    """
    time = timezone.now() + datetime.timedelta(days=days_offset)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
class QuestionIndexViewTests(TestCase):

    def test_index_view_latest_polls(self):
        """If therse no latest questions must return an empty list"""
        """The template should contain a text: No polls available"""
        response = self.client.get(reverse("polls:index"))        
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_questions(self):
        """Should display the message: No polls available."""
        create_question("future question?", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No polls available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_questions(self):
        """Should display the past questions"""
        question = create_question("past question", -30)
        response = self.client.get(reverse("polls:index"))
        print(response.context["latest_question_list"])
        self.assertEquals(response.status_code, 200) 
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])