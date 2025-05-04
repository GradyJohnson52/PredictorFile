document.getElementById("predict-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const team1 = document.getElementById("team1").value;
  const team2 = document.getElementById("team2").value;
  const week = document.getElementById("week").value;

  const response = await fetch("https://predictorfile.onrender.com", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ team1, team2, week }),
  });

  const data = await response.json();
  document.getElementById("result").innerText =
    data.error ? data.error : `Predicted Winner: ${data.winner} (Confidence: ${Math.round(data.confidence * 100)}%)`;
});
