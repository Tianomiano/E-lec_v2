document.addEventListener("DOMContentLoaded", function () {
    const landingPage = document.querySelector(".landing-page");
    const featuresContainer = document.querySelector(".features-container");

    window.addEventListener("scroll", function () {
        const scrollPosition = window.scrollY;
        const landingPageHeight = landingPage.clientHeight;

        if (scrollPosition >= landingPageHeight) {
            landingPage.classList.add("active");
        } else {
            landingPage.classList.remove("active");
        }
    });
});
const homepageButton = document.getElementById("homepage-button");

// Add a click event listener to the homepage-button
homepageButton.addEventListener("click", function() {
    // Redirect the user to the homepage URL
    window.location.href = '/home';
});

const signInButton = document.getElementById("sign-in-button");
const emailInput = document.getElementById("email-input");

signInButton.addEventListener("click", function() {
    const email = emailInput.value;
    if (email) {
        // Redirect to the login page with the email as a query parameter
        window.location.href = `/login?email=${encodeURIComponent(email)}`;
    }
});