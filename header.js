document.addEventListener("DOMContentLoaded", function() {
    fetch("header.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("header-container").innerHTML = data;

            // Check if the user is logged in
            let user = localStorage.getItem("loggedInUser");
            if (user) {
                // Hide login and signup links if logged in
                let loginLink = document.getElementById("loginLink");
                let signupLink = document.getElementById("signupLink");
                let logoutBtn = document.getElementById("logoutBtn");

                // If login and signup links exist, hide them
                if (loginLink) {
                    loginLink.style.display = "none";
                }
                if (signupLink) {
                    signupLink.style.display = "none";
                }

                // Show logout button
                if (logoutBtn) {
                    logoutBtn.style.display = "inline";
                }

                // Display a welcome message
                let navbar = document.querySelector(".navbar");
                let welcomeMessage = document.createElement("span");
                welcomeMessage.textContent = `Welcome, ${user}!`;
                welcomeMessage.style.color = "white";
                welcomeMessage.style.marginLeft = "10px";
                navbar.appendChild(welcomeMessage);
            }

            // Logout functionality
            let logoutBtn = document.getElementById("logoutBtn");
            if (logoutBtn) {
                logoutBtn.addEventListener("click", function() {
                    localStorage.removeItem("loggedInUser");  // Remove user data
                    window.location.href = "index.html";  // Redirect to homepage
                });
            }
        })
        .catch(error => console.error("Error loading header:", error));
});
