document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("resume-form");
  const resultBox = document.getElementById("resume-result");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    resultBox.innerHTML = "<p class='text-gray-500'>Checking resume...</p>";
    resultBox.classList.remove("hidden");

    const formData = new FormData(form);
    console.log("FORM ACTION:", form.action);
console.log("Submitting to URL:", "/enhancements/check_resume");
console.log("Method: POST");

    try {
      const response = await fetch("/enhancements/check_resume", {
  method: "POST",
  body: formData
});
      const data = await response.json();

      if (data.error) {
        resultBox.innerHTML = `<p class="text-red-500 font-medium">${data.error}</p>`;
      } else {
        resultBox.innerHTML = `
          <h3 class="text-lg font-semibold mb-2">ATS Feedback:</h3>
          <div class="bg-gray-100 dark:bg-slate-800 
             text-gray-800 dark:text-gray-200
             p-3 rounded text-sm whitespace-pre-wrap">
   ${data.result}
</div>
        `;
      }
    } catch (err) {
      resultBox.innerHTML = `<p class="text-red-500">Error: ${err.message}</p>`;
    }
  });
});






