import {getNoteSummaryDiv} from './notes.js';

export async function createNewNote() {
    const text = document.querySelector("#note-text").innerText.trim();

    let labels;
    if (document.querySelector("#tags").value.trim() === "") {
        labels = [];
    }
    else {
        labels = document.querySelector("#tags").value.split(',');
    }
    const color = document.querySelector("#color").value.toLowerCase();

    if (text === "") {
        document.querySelector(".invalid-feedback").style.display = "block";
        document.querySelector("#note-text").addEventListener("input", (e) => {
            document.querySelector(".invalid-feedback").style.display = "none";
        });
        return;
    }

    const res = await fetch('/note', {
        method: "POST",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
            text,
            color,
            labels,
        }),
    });

    const new_note = await res.json();

    document.querySelector('#message').style.display = "none";
    const noteSummaryDiv = getNoteSummaryDiv(new_note);
    document.querySelector("#notes").prepend(noteSummaryDiv);

    document.querySelector("#note-text").innerText = "";
    document.querySelector("#tags").value = "";
}