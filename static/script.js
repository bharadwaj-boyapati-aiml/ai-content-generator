async function generateContent() {
  const prompt = document.getElementById("prompt").value;
  const output = document.getElementById("output");

  if (!prompt.trim()) {
    output.textContent = "Please enter a prompt.";
    return;
  }

  output.textContent = "Generating content...";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: prompt }),
    });

    const data = await response.json();

    if (response.ok) {
      output.textContent = data.content || "No response.";
    } else {
      output.textContent = data.error || "Something went wrong.";
    }
  } catch (err) {
    output.textContent = "Error: " + err.message;
  }
}
