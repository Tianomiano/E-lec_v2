// Select the form and submit button by their IDs
const contactForm = document.getElementById("contact-form");
const submitButton = document.getElementById("submit-button");

// Add a submit event listener to the form
contactForm.addEventListener("submit", function (event) {
event.preventDefault(); // Prevent the default form submission

// Get the form data
const formData = new FormData(contactForm);

// Send a POST request to your Flask API endpoint
fetch("/api/v1/contact", {
    method: "POST",
    body: JSON.stringify(Object.fromEntries(formData)),
    headers: {
    "Content-Type": "application/json",
    },
})
    .then((response) => response.json())
    .then((data) => {
    // Handle the response from the API
    if (data.message) {
        // Email sent successfully
        alert(data.message);
        // Optionally, you can clear the form fields here
        contactForm.reset();
    } else if (data.error) {
        // Error occurred
        alert(data.error);
    } else {
        // Handle other possible responses from the API
        alert("Unknown response from the server");
    }
    })
    .catch((error) => {
    console.error("Error sending email:", error);
    });
});
