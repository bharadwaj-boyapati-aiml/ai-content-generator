function generateContent() {
  const topic = document.getElementById("topic").value;
  const contentType = document.getElementById("contentType").value;

  fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ topic, content_type: contentType }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("output").innerText = data.generated_content;
    });
}
