// Open the user profile modal
document.getElementById("profile-button").addEventListener("click", async () => {
    // Fetch current user details
    const token = getSessionToken();
    const headers = {
        "Authorization": token
    };

    try {
        const response = await fetch("/api/v1/getuser", {
            method: "GET",
            headers: headers
        });

        if (response.ok) {
            const userData = await response.json();
            const newUsernameField = document.getElementById("new-username");
            const newEmailField = document.getElementById("new-email");

            // Prefill fields with current username and email
            newUsernameField.value = userData.username;
            newEmailField.value = userData.email;

            // Display the profile modal
            document.getElementById("profile-modal").style.display = "block";
        } else {
            const errorData = await response.json();
            alert("Error updating password: " + errorData.error);
        }
    } catch (error) {
        console.error("Error fetching user details:", error);
    }
});

// Close the user profile modal
document.querySelector(".modal .close").addEventListener("click", () => {
    document.getElementById("profile-modal").style.display = "none";
});

// Save user profile changes
document.getElementById("save-user").addEventListener("click", async () => {
    const newUsername = document.getElementById("new-username").value;
    const newEmail = document.getElementById("new-email").value;

    const token = getSessionToken();
    const headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    };

    const data = {
        new_username: newUsername,
        new_email: newEmail
    };

    try {
        const response = await fetch("/api/v1/getuser/update", {
            method: "PUT",
            headers: headers,
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Profile updated successfully");
        } else {
            alert("Error updating details");
        }
    } catch (error) {
        console.error("Error updating user profile:", error);
    }
});

// Change user password
document.getElementById("change-password").addEventListener("click", async () => {
    const newPassword = document.getElementById("new-password").value;
    const confirmNewPassword = document.getElementById("confirm-new-password").value;

    if (newPassword !== confirmNewPassword) {
        alert("Passwords do not match");
        return;
    }

    const token = getSessionToken();
    const headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    };

    const data = {
        new_password: newPassword,
        confirm_password: confirmNewPassword
    };

    try {
        const response = await fetch("/api/v1/users/passwd/update", {
            method: "PUT",
            headers: headers,
            body: JSON.stringify(data)
        });

        if (response.ok) {
            console.log("password updated successfuly")
            alert("Password updated successfully");
        } else {
            const errorData = await response.json();
            alert("Error updating password: " + errorData.error);
        }
    } catch (error) {
        console.error("Error changing password:", error);
    }
});

// Add an event listener for the "Close Account" button
document.getElementById("close-account").addEventListener("click", () => {
    const passwordInputContainer = document.getElementById("password-input-container");

    // Create password input element
    const passwordInput = document.createElement("input");
    passwordInput.type = "password";
    passwordInput.placeholder = "Enter your password";
    passwordInput.className = "password-input";

    // Create "Confirm" button
    const confirmButton = document.createElement("button");
    confirmButton.textContent = "Confirm";
    confirmButton.className = "confirm-button";

    // Add click event listener to the "Confirm" button
    confirmButton.addEventListener("click", async () => {
        const confirmPassword = passwordInput.value;
        
        if (confirmPassword.trim() === "") {
            // Handle empty password input
            alert("Please enter your password.");
            return;
        }

        const token = getSessionToken();
        const headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        };

        const data = {
            password: confirmPassword
        };

        try {
            const response = await fetch("/api/v1/users/close_account", {
                method: "DELETE",
                headers: headers,
                body: JSON.stringify(data)
            });

            if (response.ok) {
                sessionStorage.removeItem("token");
                localStorage.removeItem("token");
                window.location.href = "/api/v1/logout";
                alert("Sorry to see you go");
            } else {
                const errorData = await response.json();
                alert("Error updating password: " + errorData.error);
            }
        } catch (error) {
            console.error("Error closing account:", error);
        }
    });

    // Append password input and confirm button to the container
    passwordInputContainer.innerHTML = ""; // Clear any previous content
    passwordInputContainer.appendChild(passwordInput);
    passwordInputContainer.appendChild(confirmButton);
});
