import datetime

from django.http import response
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question , Choice



def create_choice(pk, choice_text, votes=0): 
    """Create a choice that have the pk(primary key is a number) of a specific question
    with the given "choice_text" and with the given "votes"(votes starts in zero)"""
    question = Question.objects.get(pk=pk)
    return question.choice_set.create(choice_text=choice_text, votes=votes)

def create_question(question_text, days):    
    """Create a question whit the given question_text, and published the given number
    of days offset to now(negative for quest90n published in the past, 
    positive for questions that have to be published)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase): 
    def setUp(self):
        self.question = Question(question_text="Who are you?")

    def test_was_published_recently_with_future_questions(self): 
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
        
    def test_was_published_recently_with_past_questions(self): 
        """was_published_recently() returns False for question pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
        
    def test_was_published_recently_with_present_questions(self): 
        """was_published_recently() returns TRue for quetion pub_date is in the present"""
        time = timezone.now() - datetime.timedelta(hours=21)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
        
        
class QuestionIndexViewTests(TestCase):
    def test_no_quetion(self):
        """if no question exist, an approate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["lates_question_list"], [])
        
    def test_no_future_question_are_displayed(self):
        """If a future question is create in the database this inst display until 
        his pub_date is on the present time"""
        create_question("future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["lates_question_list"], [])
        
    def test_question_published_in_the_past_displayed(self):
        """If a question was published un the past it should ve display on index page"""
        question = create_question("pasat question", days=-30)
        choice1 = create_choice(pk=question.id, choice_text="1", votes=0)
        choice2 =create_choice(pk=question.id, choice_text="2", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["lates_question_list"], [question])
        
    def test_feature_question_and_past_question(self):
        """ Even is both past and future question exist, only past question are displayed"""
        future_question = create_question(question_text="Who is the best minecraft player" , days=2)
        past_question = create_question(question_text="pastquestion",days=-1)
        choice1 = create_choice(pk=past_question.id, choice_text="1", votes=0)
        choice2 =create_choice(pk=past_question.id, choice_text="2", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lates_question_list"],
            [past_question]
            )
    
    def test_two_past_question(self):
        """The question index page may display multiples question"""
        past_question1 = create_question(question_text="pastquestion1",days=-10)
        past_question2 = create_question(question_text="pastquestion2",days=-10)
        choice1 = create_choice(pk=past_question1.id, choice_text="1", votes=0)
        choice2 = create_choice(pk=past_question1.id, choice_text="1", votes=0)
        choice3 = create_choice(pk=past_question2.id, choice_text="1", votes=0)
        choice4 = create_choice(pk=past_question2.id, choice_text="1", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lates_question_list"],
            [past_question1, past_question2]
        )

    def test_two_future_question(self):
        """if we create two question in the future index page may not display any future question"""
        fut_question1 = create_question(question_text="futquestion1",days=1)
        fut_question2 = create_question(question_text="futtquestion2",days=10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["lates_question_list"], []
        )
        
                
    def tests_question_without_choice(self):
        """Question have no dhoices arent displayed in the index view"""
        question = create_question("Question without", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["lates_question_list"], [])
    
    def tests_question_with_choice(self):
        """Questions whit choice are displayed in the index view"""
        question =create_question("Question with", days=-10)
        choice1 = create_choice(pk=question.id, choice_text="1", votes=0)
        choice2 =create_choice(pk=question.id, choice_text="2", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["lates_question_list"], [question])
        


        
class QuestionDetailViewTests(TestCase):
    
    def tests_future_question(self):
        """THe datail view of a question whit a pub_date in the future returns a 404"""
        future_question = create_question(question_text="Future question" , days=2)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        

    def test_past_question(self):
        """The detail view of a question with the pub_date in the past returns the question text"""
        question = create_question(question_text="past question" , days=-20)
        choice1 = create_choice(pk=question.id, choice_text="1", votes=0)
        choice2 =create_choice(pk=question.id, choice_text="2", votes=0)
        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)
        
        
        
class QuestionResultsViewTest(TestCase):
    
    def tests_whit_past_question(self):
        """ The result view with a pub date in the past display the 
        question's text"""
        past_question = create_question(question_text="past question" , days=-20)
        choice1 = create_choice(pk=past_question.id, choice_text="1", votes=0)
        choice2 =create_choice(pk=past_question.id, choice_text="2", votes=0)
        url = reverse("polls:result", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    def tests_future_question(self):
        """THe datail view of a question whit a pub_date in the future returns a 404"""
        future_question = create_question(question_text="Future question" , days=2)
        url = reverse("polls:result", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

                                   
                                   
