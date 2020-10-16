import { loadNotes } from "./notes.js";

export async function loadLabels() {
    document.querySelector('#label-btns').innerHTML = "";
    document.querySelector('#message').style.display = "none";
    document.querySelector('#labels .message').style.display = "none";

    const res = await fetch('labels');
    const labels = await res.json();

    if (labels.length === 0) {
        document.querySelector('#labels .message').innerText = "No labels to show";
        document.querySelector('#labels .message').style.display = "block";
    }

    labels.forEach(label => {
        const labelDiv = makeLabelDiv(label);
        document.querySelector('#label-btns').append(labelDiv);
    }); 
}

function makeLabelDiv(label) {
    const labelDiv = document.createElement('div');
    labelDiv.className = "col-6 col-md-4 text-center";

    const labelBtn = document.createElement('button');
    labelBtn.className = "btn btn-outline-dark label-btn";
    
    if (label.label === "") {
        labelBtn.innerText = "No Label";
    }
    else {
        labelBtn.innerText = label.label;
    }

    labelBtn.addEventListener('click', (e) => {
        loadNotes(label.label);
        document.querySelector('#note-box').style.display = "none";
        document.querySelector('#labels').style.display = "none";
        document.querySelector('#notes').style.display = "block";
        document.querySelector('#edit-note-box').style.display = "none";
    });

    labelDiv.append(labelBtn);

    return labelDiv;
}