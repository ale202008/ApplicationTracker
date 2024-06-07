

// Loads up the latest application into the fields for our application_viewer element.
$(document).ready(function() {
    $.ajax({
        url: '/get_application_json/',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#viewer_application_description').text(data.desc);
            $('#viewer_employer_url_logo').attr('src', "https://logo.uplead.com/" + data.employer_url_logo);
            $('#viewer_employer_url').text(data.employer_url);
            $('#viewer_employer_url').attr('href', data.employer_url);
            $('#viewer_employer').text(data.employer)
            $('#viewer_status').text(data.status)
            $('#viewer_role').text(data.role)
            $('#viewer_pay').text("$" + data.pay + " or " + "$" + data.hourly_pay + "/hr")
            $('#viewer_location').text(data.location)
            $('#viewer_source').text(data.source)
            $('#viewer_application_date').text(data.application_date);
            $('#viewer_employment_type').text(data.employment_type);
            $('#viewer_notes').text(data.notes);
            $('#viewer_update_status_button').attr('data-update-application-id', data.application_id);
            if (data.response_time) {
                $('#viewer_response_time').text(data.response_time);
                $('#viewer_response_time_container').show();
            } else {
                $('#viewer_response_time').text(""); 
                $('#viewer_response_time_container').hide(); 
            }
        },
        error: function(xhr, status, error) {
            console.error('Error fetching the latest application:', error);
        }
    });
});


// When a button is clicked and has the class 'application-card-button', retrieve information for that button's application_id
$(document).ready(function() {
    $('.application-card-button').click(function() {
        var applicationId = $(this).data('application-id');
        fetchApplicationDetails(applicationId);
        $('#status_id').val('');
    });
});


// Function for getting an application details when given an applicationId
function fetchApplicationDetails(applicationId) {
    $.ajax({
        url: '/get_application_json/',
        type: 'GET',
        data: { applicationId: applicationId },
        dataType: 'json',
        success: function(data) {
            $('#viewer_application_description').text(data.desc);
            $('#viewer_employer_url_logo').attr('src', "https://logo.uplead.com/" + data.employer_url_logo);
            $('#viewer_employer_url').text(data.employer_url);
            $('#viewer_employer_url').attr('href', data.employer_url);
            $('#viewer_employer').text(data.employer)
            $('#viewer_status').text(data.status)
            $('#viewer_role').text(data.role)
            $('#viewer_pay').text("$" + data.pay + " or " + "$" + data.hourly_pay + "/hr")
            $('#viewer_location').text(data.location)
            $('#viewer_source').text(data.source)
            $('#viewer_application_date').text(data.application_date);
            $('#viewer_employment_type').text(data.employment_type);
            $('#viewer_notes').text(data.notes);
            $('#viewer_update_status_button').attr('data-update-application-id', data.application_id);
            if (data.response_time) {
                $('#viewer_response_time').text(data.response_time);
                $('#viewer_response_time_container').show();
            } else {
                $('#viewer_response_time').text(""); 
                $('#viewer_response_time_container').hide(); 
            }
        },
        error: function(xhr, status, error) {
            console.error('Error fetching the latest application:', error);
        }
    });
}


// Listener for when 'update-status' button is clicked, call function and update status to given status_id
$(document).ready(function() {
    $('#viewer_update_status_button').click(function() {
        var selectedStatus = $('#status_id').val();
        var applicationId = $(this).data('update-application-id');
        updateStatus(selectedStatus, applicationId);
    });
});


// Function that updates the status of application object by calling endpoint in utils.py, sending the status and applicationid
function updateStatus(selectedStatus, applicationId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: '/update_status/',
        type: 'POST',
        data: { 
            status: selectedStatus,
            applicationId: applicationId
         },
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data) {
            console.log('Status updated successfully.');
            alert("Status updated successfully.")
            fetchApplicationDetails(applicationId)
            updateNavbarStats();
        },
        error: function(xhr, status, error) {
            console.error('Error fetching the latest application:', error);
        }
    });
}


// Function that updates the Navbar stats without needing to reload the page
function updateNavbarStats() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
        url: '/get_navbar_stats/',
        type: 'POST',
        dataType: 'json',
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data) {
            console.log(data)
            $('#avg_resp_time').text(data.responsetime + " Days");
            $('#response_rate').text(data.responserate + "%");
            $('#rejection_rate').text(data.rejectionrate + "%");
            $('#interview_rate').text(data.interviewrate + "%");
            $('#withdrawn_rate').text(data.withdrawnrate + "%");
            $('#offered_rate').text(data.offeredrate + "%");
            $('#accepted_rate').text(data.acceptedrate + "%");
        },
        error: function(xhr, status, error) {
            console.error('Error updating navbar stats.', error);
        }
    });
}


// Replaces logo image with no_logo in the case image fails to load from api
$(document).ready(function() {
    $('#viewer_employer_url_logo').on('error', function() {
        $(this).attr('src', fallbackImageUrl);
    });
});


// Listener for when 'status_filter' is selected, call function and update status to given status_name
$(document).ready(function() {
    $('#status_filter').change(function() {
        var selectedStatus = $(this).val()

        if (selectedStatus) {
            $('.application-card-button').hide()
            $('.application-card-button').each(function() {
                var applicationStatus = $(this).data('status'); 
                if (applicationStatus === selectedStatus) {
                    $(this).show();
                }
            });
        }
        else {
            $('.application-card-button').show()
        }   
    });
});


// Listener for when 'status_search' searchbar is updated via text, filtering through applications
$(document).ready(function() {
    $('#search_filter').on('input', function() {
        var searchText = $(this).val().toLowerCase();
        
        $('.application-card-button').each(function() {
            var status = $(this).data('status').toLowerCase();
            var employer = $(this).data('employer').toLowerCase();
            var location = $(this).data('location').toLowerCase();
            var position = $(this).data('position').toLowerCase();
            
            if (status.includes(searchText) || employer.includes(searchText) || location.includes(searchText) || position.includes(searchText)) {
                $(this).show(); 
            } else {
                $(this).hide(); 
            }
        });
    });

    $('#search_filter_form').submit(function(event) {
        event.preventDefault();
    });
});