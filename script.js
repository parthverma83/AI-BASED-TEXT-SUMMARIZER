document.getElementById('summarizeBtn').addEventListener('click', async () => {
  const inputText = document.getElementById('inputText').value.trim();
  const summaryBox = document.getElementById('summaryBox');
  const summaryText = document.getElementById('summaryText');

  if (!inputText) {
    summaryText.innerText = "Please enter text to summarize.";
    summaryBox.classList.remove('hidden');
    return;
  }

  summaryText.innerText = "Summarizing... Please wait.";
  summaryBox.classList.remove('hidden');

  try {
    const response = await fetch('http://localhost:5000/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inputText })
    });

    const result = await response.json();
    if (response.ok && result.summary) {
      summaryText.innerText = result.summary;
    } else {
      summaryText.innerText = "Failed to summarize text. Please try again.";
    }
  } catch (error) {
    summaryText.innerText = `Error: ${error.message}`;
  }
});
