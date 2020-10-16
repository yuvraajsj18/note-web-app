import {colors} from './noteutils.js';
import {enableEditing} from './editnote.js';

export async function loadNotes(category) {
    document.querySelector('#notes').innerHTML = "";
    document.querySelector('#message').style.display = "none";
    const res = await fetch(`note?category=${category}`);
    const notes = await res.json();

    if (notes.length === 0) {
        document.querySelector('#message').innerText = "No notes to show";
        document.querySelector('#message').style.display = "block";
    }

    notes.forEach(note => {
        const noteSummaryDiv = getNoteSummaryDiv(note);
        document.querySelector("#notes").append(noteSummaryDiv);
    });
}

export function getNoteSummaryDiv(note) {
    const noteDiv = document.createElement('div');
    noteDiv.className = "note";
    noteDiv.id = `note-${note.noteId}`;
    
    const noteCard = document.createElement('div');
    noteCard.className = 'card';
    noteCard.style.backgroundColor = colors[note.color];

    const noteBody = document.createElement('div');
    noteBody.className = "card-body pb-2";

    const noteText = document.createElement('div');
    noteText.className = "card-text";

    noteText.innerHTML = note.text.substr(0, 300) + '<strong>  ...More</strong>';   // to make single line break a real line break and do not disturb a real paragraph
    noteBody.append(noteText);

    const noteLabels = document.createElement('div');
    noteLabels.className = "labels mt-2";
    note.labels.forEach(label => {
        const labelSpan = document.createElement('span');
        labelSpan.className = "badge badge-dark mr-2";
        labelSpan.setAttribute("aria-label", "label");
        labelSpan.append(document.createTextNode(label.label));
        noteLabels.append(labelSpan);
    });
    noteBody.append(noteLabels);

    noteCard.append(noteBody);

    noteDiv.append(noteCard);

    // Add Event Listener
    noteDiv.addEventListener('click', (e) => {
        showNote(e, note.noteId);
    });

    return noteDiv;
}

async function showNote(event, noteId) {
    document.querySelector('#notes').style.display = "none";
    document.querySelector('#note-box').style.display = "none";
    document.querySelector('#labels').style.display = "none";
    
    const editNoteBox = document.querySelector('#edit-note-box');
    editNoteBox.setAttribute('data-noteid', noteId);

    const res = await fetch(`/note/edit?noteId=${noteId}`);
    const note = await res.json();

    if (note.isArchived === false) {
        document.querySelector('#archive').innerText = "Archive";
        editNoteBox.setAttribute('data-isarchived', 'false');
    }
    else {
        document.querySelector('#archive').innerText = "Unarchive";   
        editNoteBox.setAttribute('data-isarchived', 'true');     
    }
    editNoteBox.style.backgroundColor = colors[note.color];
    document.querySelector('#edit-note-text').innerHTML = note.text;
    let labels = new Array;
    note.labels.forEach(label => {
        labels.push(label.label);
    });
    labels = labels.toString();
    document.querySelector('#edit-tags').value = labels;
    document.querySelector("#edit-color").value = capitalize(note.color);

    editNoteBox.style.display = "block";

    // NOTE: For removing previous event listeners added to the edit button that were added because of opening different notes
    const oldEditBtn = document.querySelector("#edit");
    const newEditBtn = oldEditBtn.cloneNode(true);
    oldEditBtn.parentNode.replaceChild(newEditBtn, oldEditBtn);
    // ---------------------
    document.querySelector('#edit').innerText = 'Edit';
    document.querySelector('#edit-note-text').setAttribute('contenteditable', 'false');
    document.querySelector('#edit').addEventListener('click', (e) => {
        enableEditing(e, note.text, note.markdown);
    });
}

function capitalize(string) {
    return string[0].toUpperCase() + string.substr(1);
}
