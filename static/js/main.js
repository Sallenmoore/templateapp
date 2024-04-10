import * as utility from 'utility.js';
//===My document.ready() handler...
document.body.addEventListener('htmx:configRequest', utility.form_values());

htmx.onLoad(function (e) {
    // Show/Hide Back to Top Button based on scroll position
    window.addEventListener('scroll', function () {
        var backToTopButton = document.getElementById("back-to-top");
        if (window.scrollY > 300) {
            backToTopButton.style.display = "block";
        } else {
            backToTopButton.style.display = "none";
        }
    });
});