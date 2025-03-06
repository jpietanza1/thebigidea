document.addEventListener("DOMContentLoaded", function() {
    fetch("header.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("header-container").innerHTML = data;

            // Check if the user is logged in
            let user = localStorage.getItem("loggedInUser");
            if (user) {
                document.getElementById("loginLink").style.display = "none";  // Hide login
                document.getElementById("signupLink").style.display = "none"; // Hide signup
                document.getElementById("logoutBtn").style.display = "inline"; // Show logout button
                document.getElementById("myTeamLink").style.display = "inline"; // Show My Team link

                // Display a welcome message
                let navbar = document.querySelector(".navbar");
                let welcomeMessage = document.createElement("span");
                welcomeMessage.textContent = `Welcome, ${user}!`;
                welcomeMessage.style.color = "white";
                welcomeMessage.style.marginLeft = "10px";
                navbar.appendChild(welcomeMessage);
            } else {
                document.getElementById("myTeamLink").style.display = "none"; // Hide My Team if not logged in
            }

            // Logout functionality
            document.getElementById("logoutBtn").addEventListener("click", function() {
                localStorage.removeItem("loggedInUser");  // Remove user data
                window.location.href = "index.html";  // Redirect to homepage
            });
        })
        .catch(error => console.error("Error loading header:", error));
});
