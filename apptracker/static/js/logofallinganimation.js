const logoContainer = document.getElementById('logo-container');

function fetchLogoLinks() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/get_logo_links/', // Replace with the URL to fetch logo links
            method: 'GET',
            success: function(response) {
                resolve(response.links); // Resolve with logo links
            },
            error: function(xhr, status, error) {
                reject(error); // Reject with error message
            }
        })
    })
}

// Function to create logo elements
function createLogoElement(link) {
    const logo = document.createElement('img');
    logo.src = link;
    logo.classList.add('logo');
    logo.style.left = `${Math.random() * 95}vw`; // Random horizontal position
    logoContainer.appendChild(logo);

    // Add event listener for animation iteration end event
    logo.addEventListener('animationiteration', () => {
        logo.style.left = `${Math.random() * 95}vw`; // Randomize horizontal position
    });

    // Add event listener for error handling
    logo.addEventListener('error', () => {
        // Handle error (disable or remove logo)
        logo.style.display = 'none'; // Hide the logo
        console.error('Failed to load logo:', link);
    });

}

// Fetch logo links and create logo elements when the DOM content is loaded
document.addEventListener("DOMContentLoaded", function() {
    fetchLogoLinks()
        .then(links => {
            let index = 0;

            // Function to create a single logo element
            function createSingleLogo() {
                const existingLogo = document.querySelector(`img[src="${links[index]}"]`);
                if (!existingLogo) {
                    createLogoElement(links[index]);
                }
                index = (index + 1) % links.length; // Increment index and cycle back to 0 when it reaches the end
            }

            // Create the first logo immediately
            createSingleLogo();

            // Set interval to create logos at regular intervals
            const interval = setInterval(createSingleLogo, 1750);

        })
        .catch(error => {
            console.error('Error fetching logo links:', error);
        });
});
