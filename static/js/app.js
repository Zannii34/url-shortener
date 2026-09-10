document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        const original = btn.textContent;
        btn.textContent = 'Copied ✓';
        setTimeout(() => { btn.textContent = original; }, 1500);
      } catch (e) {
        window.prompt('Copy this link:', text);
      }
    });
  });
});
