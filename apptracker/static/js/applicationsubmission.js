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

document.addEventListener("DOMContentLoaded", function() {
    // Function to show/hide input field based on select option
    function toggleInput(selectId, inputId) {
      const select = document.getElementById(selectId);
      const input = document.getElementById(inputId);
      select.addEventListener("change", function() {
        if (select.value === "other") {
          input.classList.remove("d-none");
        } else {
          input.classList.add("d-none");
        }
      });
    }
  
    // Toggle input fields for employer and location
    toggleInput("employer_id", "other_employer");
    toggleInput("location_id", "other_location");
    toggleInput("source_id", "other_source");

  });
