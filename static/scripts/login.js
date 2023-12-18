$(document).ready(function() {
    // Function to retrieve the email from the query parameter in the URL
    function getEmailFromQuery() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('email') || ''; // If no email query parameter is found, default to an empty string
    }

    // Get the email input field and set its value
    var emailField = $('input[name="email"]');
    emailField.val(getEmailFromQuery());
    
    // Attach a click event handler to the login button
    $('.btn[name="submit"]').click(function(event) {
        event.preventDefault();

        // Get the email and password values from the input fields
        var email = $('input[name="email"]').val();
        var password = $('input[name="password"]').val();

        // Prepare the data to be sent in the POST request
        var data = {
            email: email,
            password: password
        };

        // Send a POST request to the login API endpoint
        $.ajax({
            url: '/api/v1/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                const token = response.token;
                sessionStorage.setItem('token', token);
                console.log('Received token:', token);
                window.location.href = '/home?token=' + token + '&logged_in=true';
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                alert('Login failed');
            }
        });
    });

    // Attach a click event handler to the logout link
    $('.logout-link').click(function(event) {
        event.preventDefault();

        $.ajax({
            url: '/api/v1/logout',
            method: 'POST',
            success: function(response) {
                const token = response.token;
                sessionStorage.setItem('token', token);
                window.location.href = '/home?token=' + token + '&logged_in=false';
                console.log(response);
                alert('Logged out successfully');
                sessionStorage.removeItem('token');
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                alert('Logout failed');
            }
        });
    });
});
