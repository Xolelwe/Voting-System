// static/polls/js/script.js
let audioEnabled = false;

function safeSpeak(text) {
  if (!audioEnabled) return;
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 0.95;
    window.speechSynthesis.speak(u);
  }
}

function toggleAudio() {
  audioEnabled = !audioEnabled;
  const btn = document.getElementById('audioToggle');
  if (btn) btn.innerText = audioEnabled ? '🔊 Audio: ON' : '🔈 Audio: OFF';
  safeSpeak(audioEnabled ? 'Audio guidance on' : 'Audio guidance off');
}

function toggleContrast() {
  document.body.classList.toggle('high-contrast');
}
function increaseFont() {
  document.documentElement.style.fontSize = '120%';
}
function decreaseFont() {
  document.documentElement.style.fontSize = '100%';
}

// Announce headings & buttons when they get focus
document.addEventListener('focusin', (e) => {
  const el = e.target;
  if (el.matches('.card') || el.matches('button') || el.matches('h2') || el.matches('p')) {
    safeSpeak(el.innerText || el.getAttribute('aria-label') || '');
  }
});

// Survey progress update
function updateProgress() {
  const answered = document.querySelectorAll('#survey-form input[type=radio]:checked').length;
  const total = document.querySelectorAll('.survey-question').length;
  const percent = total ? Math.round((answered / total) * 100) : 0;
  const fill = document.getElementById('progressFill');
  if (fill) fill.style.width = percent + '%';
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#survey-form input[type=radio]').forEach(inp => {
    inp.addEventListener('change', () => updateProgress());
    inp.addEventListener('focus', (e) => safeSpeak(e.target.parentElement.innerText));
  });

  // Allow Enter on a focused .card to click its button
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && document.activeElement && document.activeElement.classList.contains('card')) {
      const btn = document.activeElement.querySelector('button');
      if (btn) btn.click();
    }
  });
});
