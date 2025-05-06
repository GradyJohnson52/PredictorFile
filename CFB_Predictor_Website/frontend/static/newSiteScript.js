import { teamMapping, teamNames } from './teammapping.js';

// Normalize input
function normalizeTeam(name) {
  return teamMapping[name.trim()] || name.trim();
}

// Update datalist suggestions
function updateDatalist(inputValue, datalist) {
  const searchTerm = inputValue.trim().toLowerCase();
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

// Initialize each form
document.querySelectorAll('.predict-form').forEach(form => {
  const modelId = form.dataset.model;
  const resultDiv = form.nextElementSibling;
  const team1Input = form.querySelector('input[name="team1"]');
  const team2Input = form.querySelector('input[name="team2"]');
  const datalist = document.getElementById('team-options'); // Shared datalist

  // Attach input listeners for team suggestions
  [team1Input, team2Input].forEach(input => {
    input.addEventListener("input", () => {
      updateDatalist(input.value, datalist);
    });
  });

  // Handle form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const rawTeam1 = team1Input.value;
    const rawTeam2 = team2Input.value;
    const team1 = normalizeTeam(rawTeam1);
    const team2 = normalizeTeam(rawTeam2);
    const week = form.querySelector('input[name="week"]').value;

    // Adjust endpoint based on model (you can change this logic as needed)
    const endpoint = `https://predictorfile.onrender.com/predict?model=${modelId}`;

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ team1, team2, week }),
      });

      const data = await response.json();
      resultDiv.innerText = data.error
        ? data.error
        : `Predicted Winner: ${data.winner} (Confidence: ${Math.round(data.confidence * 100)}%)`;
    } catch (err) {
      resultDiv.innerText = "Error contacting prediction server.";
    }
  });
});
