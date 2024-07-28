const logoContainer = document.getElementById('logo-container');

function fetchLogoLinks() {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: '/get_logo_links/', 
            method: 'GET',
            success: function(response) {
                resolve(response.links); 
            },
            error: function(xhr, status, error) {
                reject(error); 
            }
        })
    })
}

// Function to create logo elements
function createLogoElement(link) {
    const logo = document.createElement('img');
    logo.src = link;
    logo.classList.add('logo');
    logo.style.left = `${Math.random() * 95}vw`; 
    logoContainer.appendChild(logo);

    // Add event listener for animation iteration end event
    logo.addEventListener('animationiteration', () => {
        logo.style.left = `${Math.random() * 95}vw`; 
    });

    // Add event listener for error handling
    logo.addEventListener('error', () => {
        // Handle error (disable or remove logo)
        logo.style.display = 'none'; 
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
                index += 1; // Increment index and cycle back to 0 when it reaches the end
                if (index == links.length) {
                    index = 0
                };
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
