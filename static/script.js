document.getElementById("generate-btn").addEventListener("click", async () => {
  const prompt = document.getElementById("prompt").value;
  const resultDiv = document.getElementById("result");

  if (!prompt.trim()) {
    resultDiv.innerText = "Please enter a prompt.";
    return;
  }

  resultDiv.innerText = "Generating...";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt: prompt })
    });

    const data = await response.json();

    if (response.ok && data.content) {
      resultDiv.innerText = data.content;
    } else if (data.error) {
      resultDiv.innerText = "Error: " + data.error;
    } else {
      resultDiv.innerText = "No content generated.";
    }
  } catch (error) {
    resultDiv.innerText = "Request failed: " + error.message;
  }
});
