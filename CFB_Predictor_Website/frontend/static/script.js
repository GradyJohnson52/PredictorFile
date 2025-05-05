import { teamMapping, teamNames } from './teammapping.js';


const datalist = document.getElementById('team-options');

function normalizeTeam(name) {
  return teamMapping[name.trim()] || name.trim();
}

function updateDatalist(inputValue) {
  // Lowercase for case-insensitive matching
  const searchTerm = inputValue.trim().toLowerCase();

  // Find all aliases that contain the input text
  const matchingCanonicalNames = new Set();

  for (const [alias, canonical] of Object.entries(teamMapping)) {
    if (alias.toLowerCase().includes(searchTerm)) {
      matchingCanonicalNames.add(canonical);
    }
  }

  datalist.innerHTML = "";

  matchingCanonicalNames.forEach(team => {
    const option = document.createElement('option');
    option.value = team;
    datalist.appendChild(option);
  });
}

["team1", "team2"].forEach(id => {
  const input = document.getElementById(id);
  input.addEventListener("input", () => {
    updateDatalist(input.value);
  });
});




document.getElementById("predict-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const rawTeam1 = document.getElementById("team1").value;
  const rawTeam2 = document.getElementById("team2").value;
  const team1 = normalizeTeam(rawTeam1);
  const team2 = normalizeTeam(rawTeam2);
  const week = document.getElementById("week").value;

  const response = await fetch("https://predictorfile.onrender.com/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ team1, team2, week }),
  });

  const data = await response.json();
  document.getElementById("result").innerText =
    data.error ? data.error : `Predicted Winner: ${data.winner} (Confidence: ${Math.round(data.confidence * 100)}%)`;
});
