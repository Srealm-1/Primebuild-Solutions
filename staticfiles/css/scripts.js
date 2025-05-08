ddocument.addEventListener("DOMContentLoaded", function () { 
    const themeToggle = document.getElementById("theme-toggle");
    const htmlElement = document.documentElement;

    // Load saved theme from localStorage
    let savedTheme = localStorage.getItem("theme") || "light";
    htmlElement.setAttribute("data-theme", savedTheme);

    // Update button text (optional)
    themeToggle.innerText = savedTheme === "dark" ? "Light Mode" : "Dark Mode";

    themeToggle.addEventListener("click", function () {
        let currentTheme = htmlElement.getAttribute("data-theme");
        let newTheme = currentTheme === "dark" ? "light" : "dark";

        htmlElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);

        // Update button text (optional)
        themeToggle.innerText = newTheme === "dark" ? "Light Mode" : "Dark Mode";
    });
});
