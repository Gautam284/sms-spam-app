document.getElementById("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = document.getElementById("message").value;
  const resultElement = document.getElementById("result");

  resultElement.innerText = "Analyzing...";
  resultElement.className = "loading";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await response.json();

    if (data.prediction) {
      if (data.prediction === "Spam") {
        resultElement.innerText = "🚨 Spam Message Detected!";
        resultElement.className = "spam";
      } else {
        resultElement.innerText = "✅ Not Spam (Safe Message)";
        resultElement.className = "not-spam";
      }
    } else {
      resultElement.innerText = "Error: " + data.error;
      resultElement.className = "error";
    }
  } catch (err) {
    resultElement.innerText = "Error connecting to server";
    resultElement.className = "error";
  }
});
