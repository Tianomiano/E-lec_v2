$(document).ready(function() {
    // Attach a click event handler to the register button
    $('.btn[name="submit"]').click(function(event) {
        event.preventDefault();

        // Get the input values from the registration form
        var username = $('input[name="username"]').val();
        var email = $('input[name="email"]').val();
        var password = $('input[name="password"]').val();
        var confirmPassword = $('input[name="confirm_password"]').val();

        // Check if passwords match
        if (password !== confirmPassword) {
            $('#password-mismatch-error').show();
            return;
        } else {
            $('#password-mismatch-error').hide();
        }

        // Prepare the data to be sent in the POST request
        var data = {
            username: username,
            email: email,
            password: password,
            confirm_password: confirmPassword
        };

        // Send a POST request to the registration API endpoint
        $.ajax({
            url: '/api/v1/register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                window.location.href = '/login';
                console.log(response);
                alert('Registration successful');
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                alert('Registration failed');
            }
        });
    });
});
