async function generateContent() {
  const prompt = document.getElementById('prompt').value;
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = "Generating...";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    resultDiv.textContent = data.content || "No content generated.";
  } catch (err) {
    resultDiv.textContent = "Error generating content.";
    console.error(err);
  }
}
