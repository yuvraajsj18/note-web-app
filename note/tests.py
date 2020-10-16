"""Contains test for models and client requests"""

from django.test import Client, TestCase

from django.urls.base import reverse

from .models import Label, Note, User

# Create your tests here.


class NoteTestCase(TestCase):
    """Creates setup for test classes"""

    def setUp(self):

        # Create Users
        user1 = User.objects.create_user('user1', 'user1@note.com', 'password')
        user2 = User.objects.create_user(
            username='user2',
            email='user2@note.com',
            password='password')

        # Create Notes
        note1 = Note.objects.create(
            user=User.objects.get(username="user1"),
            text="Some text in note 1",
        )
        note2 = Note.objects.create(
            user=User.objects.get(username="user1"),
            text="Some text in note 2",
        )

        # Create Labels
        label1 = Label.objects.create(user=user1, label="label1")
        label2 = Label.objects.create(user=user1, label="label2")

class NoteModelsTestCase(NoteTestCase):
    """Tests model"""

    def test_users_count(self):
        """Tests successful user creation"""
        users = User.objects.count()

        self.assertEqual(users, 2)

    def test_note_creation(self):     
        """Tests successful creation of a basic note with just text"""
        note_count = Note.objects.count()

        self.assertEqual(note_count, 2)

    def test_label_creation(self):
        """Tests successful creation of labels"""
        label_count = Label.objects.count()

        self.assertEqual(label_count, 2)

    def test_note_valid_color_change(self):
        """Tests addition of an valid color to a note"""
        allowed_colors = ('red', 'green', 'blue', 'purple', 'white', '')

        for color in allowed_colors:
            note = Note.objects.get(pk=1)
            note.color = color
            note.save()
            note = Note.objects.get(pk=1)   # Requery to see the change
            self.assertEqual(note.color, color, f"Not working for color {color}")

    def test_note_invalid_color_change(self):
        """Tests addition of an invalid color to a note"""
        note = Note.objects.get(pk=1)
        color_name = "some_invalid_color"
        note.color = color_name
        note.save()     # Save will not complete if the color is invalid
        note = Note.objects.get(pk=1)  # Requery to see the change
        # Make sure the color didn't changed to invalid color
        self.assertNotEqual(note.color, color_name)    

    def test_note_add_labels(self):
        """Tests successful addition of labels to note"""
        user = User.objects.get(username="user1")
        label, label_created = Label.objects.get_or_create(user=user, label="newLabel") 

        note = Note.objects.get(pk=1)
        note.labels.add(label)
        note.save()

        note = Note.objects.get(pk=1)        
        self.assertTrue(note.labels.filter(label="newLabel").exists())

        
class NoteClientTestCase(NoteTestCase):
    """Tests Client requests and page rendering"""

    def test_register(self):
        """Tests successful registration of user"""
        c = Client()

        response = c.get('/register')

        self.assertEqual(response.status_code, 200)

        response = c.post('/register', {
            'username': 'user',
            'email': 'user@email.com',
            'password': 'password',
            'password_confirmation': 'password',
        })

        self.assertEqual(response.status_code, 201)

    def test_invalid_register(self):
        """Tests failed registration of a user if some fields are not provided"""

        c = Client()

        response = c.post('/register', {
          'username': '',
          'email': '',
          'password': '',
        })

        self.assertEqual(response.status_code, 400)

    def test_login(self):
        """Tests successful login by user"""
        c = Client()

        response = c.get('/login')
        self.assertEqual(response.status_code, 200)

        response = c.post('/login', {
            'username': 'user1',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        c = Client()

        response = c.post('/login', {
            'username': '',
            'password': '',
        })
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        """Test successful logout of user"""

        c = Client()
        response = c.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_index_not_login(self):
        c = Client()

        # accessing without login in
        response = c.get("")

        # Redirect to login page: 302
        self.assertEqual(response.status_code, 302)

    def test_index_login(self):
        c = Client()

        # login
        c.post("/login", {
            'username': 'user1',
            'password': 'password',
        })

        # get index
        response = c.get("")

        # index page loaded
        self.assertEqual(response.status_code, 200)

    def test_note_post(self):
        c = Client()

        # without login
        response = c.post(reverse('note:note'), {
            'text': 'Some text in the note',
            'color': 'red',
            'labels': '',
        }, content_type="application/json")

        self.assertEqual(response.status_code, 302, "Without Login Case")   # Redirect

        # login
        c.post("/login", {
            'username': 'user1',
            'password': 'password',
        })

        response = c.post(reverse('note:note'), {
            'text': 'Some text in the note',
            'color': 'red',
            'labels': '',
        }, content_type="application/json")

        self.assertEqual(response.status_code, 201, "Successful creation case")

        # without text field
        response = c.post(reverse('note:note'), {
            'text': '',
            'color': 'red',
            'labels': 'tag1, tag2',
        }, content_type="application/json")

        self.assertEqual(response.status_code, 400, "Without required text field")


