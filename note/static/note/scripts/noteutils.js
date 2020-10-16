export const colors = {
    white: "#ffffff",
    red: "#f28b82",
    green: "#ccff90",
    blue: "#aecbfa",
    purple: "#d7aefb",
};

export function changeNoteColor(event, id) {
    const note = document.querySelector(id);
    note.style.backgroundColor = colors[event.target.value.toLowerCase()];
}

export function formatNote(note) {
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
    lines.forEach(line => {
        if (line !== '') {
            note += line + '<br>';
        }
    });

    return note;
}