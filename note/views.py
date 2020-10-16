import json
from os import stat
from markdown2 import markdown
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .models import Label, Note, User
from .forms import *

# Create your views here.

@login_required(redirect_field_name="" ,login_url=reverse_lazy('note:login'))
def index(request):
    return render(request, 'note/index.html')

@login_required(redirect_field_name="", login_url=reverse_lazy('note:login'))
def note(request):
    """
        POST: Save a note to database
        GET: Responce with the category's note's summary from database
    """
    if request.method == "POST":
        # Get data from the post request
        note_data = json.loads(request.body)

        # clean the data
        note_data['text'] = note_data['text'].strip()
        note_data['color'] = note_data['color'].lower()
        note_data['labels'] = tuple(label.strip() for label in note_data['labels'])

        # check validity of data
        if note_data['text'] == '':
            return JsonResponse({'error': 'Text field cannot be empty'}, status=400)

        # create the note
        new_note = Note.objects.create(
            user = request.user,
            text = note_data['text'],
            color = note_data['color']
        )        

        if note_data['labels']:
            for label in note_data['labels']:
                new_label, _ = Label.objects.get_or_create(user=request.user, label=label)
                new_note.labels.add(new_label)
                
        new_note.save()

        # Return the note created
        note_created = new_note.serializer()
        note_created['text'] = markdown(note_created['text'], safe_mode="escape")[:300] # First 300 characters

        # because markdown2 does not put <br> when / encounter like markdown
        note_created['text'] = note_created['text'].replace('\\', '<br>')

        return JsonResponse(note_created, status=201)
    if request.method == "GET":
        category = request.GET.get('category')

        if category == 'all':  # all unarchived
            notes = Note.objects.filter(user=request.user, is_archived=False)
        elif category == 'archived':
            notes = Note.objects.filter(user=request.user, is_archived=True)
        else:
            try:
                label = Label.objects.get(user=request.user, label=category)
                notes = Note.objects.filter(user=request.user, labels=label)
            except Label.DoesNotExist:
                return JsonResponse({'error':'Invalid view option'}, status=400)

        notes = notes.order_by("-datetime").all()
        notes_serialized = []
        for note in notes:
            note = note.serializer()
            note['text'] = markdown(note['text'], safe_mode="escape")[:300]
            # because markdown2 does not put <br> when / encounter like markdown
            note['text'] = note['text'].replace('\\', '<br>')
            notes_serialized.append(note)

        return JsonResponse(notes_serialized, safe=False, status=200)

@login_required(redirect_field_name="", login_url=reverse_lazy('note:login'))
def note_edit(request):
    """For Viewing and editing a note
    GET: Returns a single note with the given id, error if id is not valid
    PUT: Edit the note
    DELETE: Deletes a note
    """
    if request.method == 'GET':
        note_id = request.GET['noteId']

        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'note does not exist'}, status=400)

        note = note.serializer()
        note['markdown'] = note['text']
        note['text'] = markdown(note['text'], safe_mode="escape")
        # because markdown2 does not put <br> when / encounter like markdown
        note['text'] = note['text'].replace('\\', '<br>')

        return JsonResponse(note, status=200)
    elif request.method == "PUT":
        # Get data from the post request
        note_data = json.loads(request.body)

        # clean the data
        note_data['text'] = note_data['text'].strip()
        note_data['color'] = note_data['color'].lower()
        note_data['labels'] = tuple(label.strip() for label in note_data['labels'])
        note_data['noteId'] = int(note_data['noteId'])

        # check validity of data
        if note_data['text'] == '':
            return JsonResponse({'error': 'Text field cannot be empty'}, status=400)

        # get the note
        try:
            note = Note.objects.get(id=note_data['noteId'])
        except Note.DoesNotExist:
            return JsonResponse({'error': 'note id is invalid'}, status=400)
        
        # edit note's content
        note.text = note_data['text']
        note.color = note_data['color']

        # delete old labels
        note.labels.clear()
        # add new labels
        if note_data['labels']:
            for label in note_data['labels']:
                new_label, _ = Label.objects.get_or_create(user=request.user, label=label)
                note.labels.add(new_label)
                
        note.save()

        # Return the note edited note
        edited_note = note.serializer()
        edited_note['text'] = markdown(edited_note['text'], safe_mode="escape")[:300] # First 300 characters
        # because markdown2 does not put <br> when / encounter like markdown
        edited_note['text'] = edited_note['text'].replace('\\', '<br>')

        return JsonResponse(edited_note, status=201)
    elif request.method == "DELETE":
        """Deletes a note from database"""
        note_id = int(json.loads(request.body)['noteId'])

        # get the note
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'note id is not valid'}, status=400)
        
        # delete the note
        note.delete()

        return JsonResponse({'message': 'deleted the note'}, status=200)

def note_archive(request):
    """Archive/Unarchive a note"""
    if request.method == "PUT":
        note_id = int(json.loads(request.body)['noteId'])
        
        # get the note
        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'note id is not valid'}, status=400)
        
        # Toggle the archive state
        note.is_archived = not note.is_archived
        note.save()

        return JsonResponse({'message': 'Toggled the archive'}, status=200)

def labels(request):
    """Return all labels"""
    if request.method == "GET":
        labels = Label.objects.filter(user=request.user)

        labels = [label.serializer() for label in labels]

        labels.sort(key=lambda label: label['label'])

        return JsonResponse(labels, safe=False, status=200)

def login_view(request):
    """
        Get: display login form
        Post: login user into a session
    """
    if request.method == "POST":
        # Get details from form
        username = request.POST["username"]
        password = request.POST['password']

        # attempt to sign in
        user = authenticate(request, username=username, password=password)

        # check if authetication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('note:index'))
        else:
            return render(request, 'note/login.html', {
                'message': 'Invalid username and/or password',
            }, status=401)
    if request.method == "GET":
        # if already logged in then goto index
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('note:index'))
        return render(request, 'note/login.html', status=200)


def logout_view(request):
    """Logout user from current session"""

    logout(request)
    return HttpResponseRedirect(reverse('note:login'))


def register(request):
    """
        Get: Display register page
        Post: Register a new user
    """
    if request.method == "POST":
        new_user_details = RegisterForm(request.POST)

        # check for empty fields, unique username, and password match
        if not new_user_details.is_valid():
            return render(request, 'note/register.html', {
                'register_form': new_user_details,
            }, status=400)
    
        # create new user
        new_user = User.objects.create_user(
            new_user_details.cleaned_data['username'],
            new_user_details.cleaned_data['email'],
            new_user_details.cleaned_data['password']
        )
        # save new user to database
        new_user.save()
        
        # login new user
        login(request, new_user)

        return HttpResponseRedirect(reverse('note:index'), status=201)
    elif request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('note:index'))
        return render(request, 'note/register.html', status=200)