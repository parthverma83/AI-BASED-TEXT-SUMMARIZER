document.getElementById('summarizeBtn').addEventListener('click', async () => {
  const inputText = document.getElementById('inputText').value.trim();
  const summaryBox = document.getElementById('summaryBox');
  const summaryText = document.getElementById('summaryText');

  if (!inputText) {
    summaryText.innerText = "Please enter text to summarize.";
    summaryBox.style.display = 'block';
    return;
  }

  summaryText.innerText = "Summarizing... Please wait.";
  summaryBox.style.display = 'block';

  try {
    const response = await fetch('/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inputText })
    });

    const result = await response.json();
    if (response.ok && result.summary) {
      summaryText.innerText = result.summary;
    } else {
      summaryText.innerText = result.error || "Failed to summarize text. Please try again.";
    }
  } catch (error) {
    summaryText.innerText = `Error: ${error.message}`;
  }
});
