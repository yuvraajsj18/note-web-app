import {getNoteSummaryDiv} from './notes.js';
import { loadNotes } from "./notes.js";


export function enableEditing(e, text, markdownText) {
    if (document.querySelector('#edit').innerText === "Edit") {
        document.querySelector('#edit').innerText = "Cancel";
        document.querySelector('#edit-note-text').innerHTML = formatNote(markdownText);
        document.querySelector('#edit-note-text').setAttribute('contenteditable', 'true');
    }
    else {
        document.querySelector('#edit').innerText = "Edit";
        document.querySelector('#edit-note-text').innerHTML = text;
        document.querySelector('#edit-note-text').setAttribute('contenteditable', 'false');
        document.querySelector("#edit-note-box .invalid-feedback").style.display = "none";
    }
}

export async function editNote() {
    const noteToEdit = document.querySelector('#edit-note-box');
    const noteId = noteToEdit.dataset.noteid;

    if (document.querySelector("#edit").innerText === 'Edit') {
        document.querySelector('#edit').click();
    }
    const text = document.querySelector("#edit-note-text").innerText.trim();

    let labels;
    if (document.querySelector("#edit-tags").value.trim() === "") {
        labels = [];
    }
    else {
        labels = document.querySelector("#edit-tags").value.split(',');
    }
    
    const color = document.querySelector("#edit-color").value.toLowerCase();

    if (text === "") {
        document.querySelector("#edit-note-box .invalid-feedback").style.display = "block";
        document.querySelector("#edit-note-text").addEventListener("input", (e) => {
            document.querySelector("#edit-note-box .invalid-feedback").style.display = "none";
        });
        return;
    }

    const res = await fetch('/note/edit', {
        method: "PUT",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
            noteId,
            text,
            color,
            labels,
        }),
    });

    const editedNote = await res.json();

    // replace old note summary with new summary
    document.querySelector(`#note-${noteId}`).innerHTML = getNoteSummaryDiv(editedNote).innerHTML;

    // Go back to the home page
    document.querySelector('#note-box').style.display = "block";
    document.querySelector('#notes').style.display = "block";
    document.querySelector('#edit-note-box').style.display = "none";
}

export async function deleteNote() {
    const noteId = document.querySelector("#edit-note-box").dataset.noteid;

    const res = await fetch('/note/edit', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
            noteId,
        })
    });

    document.querySelector(`#note-${noteId}`).remove();

    // Go back to the home page
    document.querySelector('#note-box').style.display = "block";
    document.querySelector('#notes').style.display = "block";
    document.querySelector('#edit-note-box').style.display = "none";
    document.querySelector('#labels').style.display = "none";
    loadNotes('all');

    // Display delete message for 3 seconds
    document.querySelector('#message').innerText = "Deleted the note.";
    document.querySelector('#message').style.display = "block";
    setTimeout(() => {
        document.querySelector('#message').style.display = "none";
    }, 3000);
}

export async function archiveNote() {
    const noteId = document.querySelector('#edit-note-box').dataset.noteid;

    const res = await fetch('note/edit/archive', {
        method: 'PUT', 
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
            noteId,
        }),
    });

    document.querySelector(`#note-${noteId}`).remove();

    // Go back to the home page
    document.querySelector('#note-box').style.display = "block";
    document.querySelector('#notes').style.display = "block";
    document.querySelector('#edit-note-box').style.display = "none";
    document.querySelector('#labels').style.display = "none";
    loadNotes('all');

    // Display archived message for 3 seconds
    if (document.querySelector('#edit-note-box').dataset.isarchived === 'false') {
        document.querySelector('#message').innerText = "Archived the note.";
    }
    else {
        document.querySelector('#message').innerText = "Unarchived the note.";
    }
    document.querySelector('#message').style.display = "block";
    setTimeout(() => {
        document.querySelector('#message').style.display = "none";
    }, 3000);
}

function formatNote(note) {
     /*
     * The note provided by the markdown consider 1 empty line as new line
     * so,
     *      Line 1
     *      Line 2
     *      Line 3
     * becomes line 1 line 2 line3
     * we need to replace \n with <br>
     * but doing that will insert a <br> for an empty line between paragraphs
     * creating unnecessary space
     * therefore this function adds <br> only to ends of non empty lines
    */

   const lines = note.split('\n');
   note = "";
   let previousLine = '';
   lines.forEach(line => {
       if (line !== '' || previousLine === '') {
           note += line + '<br>';
       }
       previousLine = line;
   });

   return note;
}