$(document).ready(function() {
  $('.applicationForm').submit(function(event) {
      event.preventDefault(); // Prevent default form submission

      var formData = new FormData(this); // Initialize FormData with the form data

      $.ajax({
        type: 'POST',
        url: '/application_submission/',
        data: formData, 
        processData: false, 
        contentType: false, 
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
        },
        success: function(response) {
            // Handle successful response
            console.log(response);
            alert('Form submitted successfully!');
            location.reload();
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(xhr.responseText);
            alert('Error submitting form!');
        }
    });
    

  });
});

