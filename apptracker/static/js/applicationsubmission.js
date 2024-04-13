$(document).ready(function() {
    $('.applicationForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        var formData = $(this).serialize(); // Serialize form data
        $.ajax({
            type: 'POST',
            url: '/application_submission/',
            data: formData,
            success: function(response) {
                // Handle successful response
                console.log(response);
                alert('Form submitted successfully!');
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.error(xhr.responseText);
                alert('Error submitting form!');
            }
        });
    });
});