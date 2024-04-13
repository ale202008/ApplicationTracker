$(document).ready(function() {
  $('.applicationForm').submit(function(event) {
      event.preventDefault(); // Prevent default form submission

      var formData = new FormData(this); // Initialize FormData with the form data

      // Loop through 'other_' fields and append them to formData object
      $('[id^="other_"]').each(function() {
          var fieldName = $(this).attr('id').replace('other_', '');
          var selectField = document.getElementById(fieldName + '_id');
          var selectedValue = selectField.options[selectField.selectedIndex].value;
          if (selectedValue === "other") {
              formData.append(fieldName, $(this).val());
          }
      });

      $.ajax({
        type: 'POST',
        url: '/application_submission/',
        data: formData, // Use formData object
        processData: false, // Prevent jQuery from automatically converting formDataObject to a query string
        contentType: false, // Prevent jQuery from automatically setting Content-Type header
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
        },
        success: function(response) {
            // Handle successful response
            console.log(response);
            alert('Form submitted successfully!');
            $('.applicationForm').trigger('reset');
            $('[id^="other_"]').addClass('d-none');
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
        input.required = true; // Make input required
      } else {
        input.classList.add("d-none");
        input.required = false; // Make input optional
        input.value = ""; // Clear the input field
      }
    });
  }

  // Toggle input fields for employer and location
  toggleInput("employer_id", "other_employer");
  toggleInput("location_id", "other_location");
    toggleInput("source_id", "other_source");

  });
