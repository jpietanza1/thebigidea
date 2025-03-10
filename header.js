document.addEventListener("DOMContentLoaded", function() {
    fetch("header.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("header-container").innerHTML = data;

            // Ensure elements exist AFTER injecting header.html
            let loginLink = document.getElementById("loginLink");
            let logoutBtn = document.getElementById("logoutBtn");
            let myTeamLink = document.getElementById("myTeamLink");
            let postLink = document.getElementById("postLink");
            let navbar = document.querySelector(".navbar");

            // Check if user is logged in
            let user = localStorage.getItem("loggedInUser");
            if (user) {
                if (loginLink) loginLink.style.display = "none";  // Hide login
                if (logoutBtn) logoutBtn.style.display = "inline"; // Show logout
                if (myTeamLink) myTeamLink.style.display = "inline"; // Show My Team
                if (postLink) postLink.style.display = "inline"; // Show Post

                // Display welcome message
                let welcomeMessage = document.createElement("span");
                welcomeMessage.textContent = `Welcome, ${user}!`;
                welcomeMessage.style.color = "white";
                welcomeMessage.style.marginLeft = "10px";
                navbar.appendChild(welcomeMessage);
            } else {
                if (myTeamLink) myTeamLink.style.display = "none"; // Hide My Team
                if (postLink) postLink.style.display = "none"; // Hide Post
            }

            // Add event listener AFTER ensuring logoutBtn exists
            if (logoutBtn) {
                logoutBtn.addEventListener("click", function() {
                    localStorage.removeItem("loggedInUser");  // Remove user data
                    window.location.href = "index.html";  // Redirect to homepage
                });
            }
        })
        .catch(error => console.error("Error loading header:", error));
});
