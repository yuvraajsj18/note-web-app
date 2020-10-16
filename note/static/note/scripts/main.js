import { createNewNote } from "./newnote.js";
import { loadNotes } from "./notes.js";
import { changeNoteColor } from "./noteutils.js";
import { editNote, deleteNote, archiveNote } from "./editnote.js";
import { loadLabels } from "./labels.js";

// Navigations and view changes

// On start
document.addEventListener('DOMContentLoaded', (e) => {
    document.querySelector('#note-box').style.display = "block";
    document.querySelector('#labels').style.display = "none";
    document.querySelector('#notes').style.display = "block";
    document.querySelector('#edit-note-box').style.display = "none";
    loadNotes('all');
});

// Index page - Notes
document.querySelector('#index').addEventListener('click', (e) => {
    document.querySelector('#note-box').style.display = "block";
    document.querySelector('#labels').style.display = "none";
    document.querySelector('#notes').style.display = "block";
    document.querySelector('#edit-note-box').style.display = "none";
    loadNotes('all');
});

// Archived page - Archived
document.querySelector('#archived-notes').addEventListener('click', (e) => {
    document.querySelector('#note-box').style.display = "none";
    document.querySelector('#labels').style.display = "none";
    document.querySelector('#notes').style.display = "block";
    document.querySelector('#edit-note-box').style.display = "none";
    loadNotes('archived');
});

// Labels page - Labels
document.querySelector('#labels-notes').addEventListener('click', (e) => {
    document.querySelector('#message').style.display = "none";
    document.querySelector('#note-box').style.display = "none";
    document.querySelector('#labels').style.display = "block";
    document.querySelector('#notes').style.display = "none";
    document.querySelector('#edit-note-box').style.display = "none";

    loadLabels();
});

// Creating Note

document.querySelector("#create-note").addEventListener("click", createNewNote);
document.querySelector("#color").addEventListener("change", (e) => {
    changeNoteColor(e, "#note-box");
});


// Editing Note
// edit is activated by edit button(listener is set in showNote in notes.js)
document.querySelector('#edit-note').addEventListener('click', editNote);
document.querySelector("#edit-color").addEventListener("change", (e) => {
    changeNoteColor(e, "#edit-note-box");
});


// Deleting Note

document.querySelector('#delete').addEventListener('click', deleteNote);

// Archiving Note

document.querySelector('#archive').addEventListener('click', archiveNote);

