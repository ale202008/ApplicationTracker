// Loads up the latest application into the fields for our application_viewer element.
$(document).ready(function() {
    $.ajax({
        url: '/get_application_json/',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log(data)
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
        console.log(applicationId)
        fetchApplicationDetails(applicationId);
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
            console.log(data)
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
        },
        error: function(xhr, status, error) {
            console.error('Error fetching the latest application:', error);
        }
    });
}