let currentWord = "";
let attempts = 0;
let level = 1;

async function startGame() {
  const res = await fetch('/random-word');
  const data = await res.json();
  currentWord = data.word;
  attempts = 0;
  document.getElementById("level").textContent = `Level ${level}`;
  document.getElementById("result").textContent = "";
  document.getElementById("attempts").textContent = "";
  document.getElementById("guessInput").value = "";
}

async function submitGuess() {
  const guess = document.getElementById("guessInput").value.toLowerCase();
  if (guess.length !== 5) {
    alert("Please enter a 5-letter word.");
    return;
  }

  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({secret: currentWord, guess})
  });

  const data = await res.json();

  if (res.status !== 200) {
    alert(data.error);
    return;
  }

  attempts++;
  document.getElementById("attempts").textContent = `Attempt: ${attempts}/10`;

  if (data.correct) {
    document.getElementById("result").textContent = "🎉 Correct! Moving to next level...";
    level++;
    setTimeout(startGame, 2000);
  } else {
    document.getElementById("result").textContent =
      `✅ ${data.position_match} correct position, 🔄 ${data.character_match} misplaced`;
    if (attempts >= 10) {
      alert("😢 You failed this level. Reload to try again.");
      location.reload();
    }
  }
}

startGame();
