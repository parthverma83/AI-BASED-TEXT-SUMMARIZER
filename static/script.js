document.addEventListener('DOMContentLoaded', () => {
  const inputText = document.getElementById('inputText');
  if (inputText) inputText.focus();

  const copyBtn = document.getElementById('copyBtn');
  const summaryBox = document.getElementById('summaryBox');
  if (copyBtn && summaryBox) {
    copyBtn.addEventListener('click', () => {
      const text = summaryBox.innerText;
      if (text) {
        navigator.clipboard.writeText(text).then(() => {
          copyBtn.innerText = 'Copied!';
          setTimeout(() => { copyBtn.innerText = 'Copy Summary'; }, 1200);
        });
      }
    });
  }
});

document.getElementById('summarizeBtn').addEventListener('click', async () => {
  const inputText = document.getElementById('inputText');
  const summaryBox = document.getElementById('summaryBox');
  const copyBtn = document.getElementById('copyBtn');

  summaryBox.innerText = '';
  summaryBox.style.display = 'none';
  if (copyBtn) copyBtn.style.display = 'none';

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
        if (copyBtn) copyBtn.style.display = 'inline-block';
      }, 200);
      inputText.value = '';
    } else {
      summaryBox.innerText = result.error || "Failed to summarize text. Please try again.";
      summaryBox.style.opacity = 1;
      if (copyBtn) copyBtn.style.display = 'none';
    }
  } catch (error) {
    summaryBox.innerText = `Network error: ${error.message}`;
    summaryBox.style.opacity = 1;
    if (copyBtn) copyBtn.style.display = 'none';
  }
});