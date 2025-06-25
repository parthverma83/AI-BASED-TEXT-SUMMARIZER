document.addEventListener('DOMContentLoaded', () => {
  const inputText = document.getElementById('inputText');
  if (inputText) inputText.focus();
});

document.getElementById('summarizeBtn').addEventListener('click', async () => {
  const inputText = document.getElementById('inputText');
  const summaryBox = document.getElementById('summaryBox');

  summaryBox.innerText = '';
  summaryBox.style.display = 'none';

  const text = inputText.value.trim();
  if (!text) {
    summaryBox.innerText = "Please enter text to summarize.";
    summaryBox.style.display = 'block';
    summaryBox.style.opacity = 1;
    return;
  }

  summaryBox.innerHTML = '<span class="loading-spinner"></span> Summarizing... Please wait.';
  summaryBox.style.display = 'block';
  summaryBox.style.opacity = 1;

  try {
    const response = await fetch('/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    const result = await response.json();
    if (response.ok && result.summary) {
      summaryBox.style.opacity = 0;
      setTimeout(() => {
        summaryBox.innerText = result.summary;
        summaryBox.style.opacity = 1;
      }, 200);
      inputText.value = '';
    } else {
      summaryBox.innerText = result.error || "Failed to summarize text. Please try again.";
      summaryBox.style.opacity = 1;
    }
  } catch (error) {
    summaryBox.innerText = Network error: ${error.message};
    summaryBox.style.opacity = 1;
  }
});