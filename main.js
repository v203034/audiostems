const uploadForm = document.getElementById('uploadForm');
const vocalsPlayer = document.getElementById('vocals');
const kickPlayer = document.getElementById('kick');
const snarePlayer = document.getElementById('snare');
const hihatPlayer = document.getElementById('hihat');
const midiVisual = document.getElementById('midi-visual');
const lyricsDisplay = document.getElementById('lyrics-display');

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('song', document.getElementById('songInput').files[0]);
    const lyricsFile = document.getElementById('lyricsInput').files[0];
    if (lyricsFile) formData.append('lyrics', lyricsFile);

    // POST to Python server
    const response = await fetch('/process', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }

    // Update audio sources
    vocalsPlayer.src = data.vocals;
    kickPlayer.src = data.kick;
    snarePlayer.src = data.snare;
    hihatPlayer.src = data.hihat;

    // Load MIDI
    if (data.midi) {
        fetch(data.midi)
            .then(res => res.arrayBuffer())
            .then(arrayBuffer => {
                console.log('MIDI loaded:', arrayBuffer.byteLength, 'bytes');
                // TODO: render piano roll / karaoke highlights
            });
    }

    // Load lyrics
    if (data.lyrics) {
        fetch(data.lyrics)
            .then(res => res.json())
            .then(json => {
                lyricsDisplay.innerHTML = json.map(word => `<span>${word.text}</span>`).join(' ');
            });
    }
});
