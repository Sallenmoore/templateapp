// 📁 main.js



/**
 * @param {String} HTML representing a single element.
 * @param {Boolean} flag representing whether or not to trim input whitespace, defaults to true.
 * @return {Element | HTMLCollection | null}
 */
export function from_html(html, trim = true) {
    // Process the HTML string.
    html = trim ? html.trim() : html;
    if (!html) return null;

    // Then set up a new template element.
    const template = document.createElement('template');
    template.innerHTML = html;
    const result = template.content.children;

    // Then return either an HTMLElement or HTMLCollection,
    // based on whether the input HTML had one or more roots.
    if (result.length === 1) return result[0];
    return result;
}
//===My document.ready() handler...
document.body.addEventListener('htmx:configRequest', function (evt) {
    var parameters = evt.detail.parameters;
    var values = {};
    console.log(parameters);
    for (var key in parameters) {
        //console.log(key);
        if (key.includes("[].")) {
            var attr = key.split("[].")[0];
            var subobjkey = key.split("[].")[1];

            if (!values[attr]) {
                values[attr] = [];
            }
            if (Array.isArray(parameters[key])) {
                Array.from(parameters[key]).forEach((value, index) => {
                    values[attr][index] = values[attr][index] || {};
                    values[attr][index][subobjkey] = value;
                });
            } else {
                values[attr][0] = values[attr][0] || {};
                values[attr][0][subobjkey] = parameters[key];
            }
            console.log({ key: key, params: parameters[key], attr: attr, values: values[attr], subkey: subobjkey });
        } else if (key.includes("[]")) {
            var attr = key.replace("[]", "");
            console.log(attr);
            console.log(parameters[key]);
            values[attr] = Array.isArray(parameters[key]) ? parameters[key] : [parameters[key]];
            values[attr] = values[attr].filter(value => value.trim() !== "");
        } else if (key.includes(".")) {
            var attr = key.split(".")[0];
            var subobjkey = key.split(".")[1];
            values[attr] = values[attr] || {};
            values[attr][subobjkey] = parameters[key];
        } else {
            values[key] = parameters[key];
        }
    }
    console.log(values);
    evt.detail.parameters = values;
});

htmx.onLoad(function (e) {
    //Image Management
    if (document.querySelector("#map-full-screen")) {
        document.querySelector("#map-full-screen").addEventListener("click", () => {
            document.querySelector('#model-battlemap-image').requestFullscreen();
        });
    }
    if (document.querySelector("#num_months_per_year")) {
        document.querySelector("#num_months_per_year").addEventListener("change", () => {
            var num_months = document.querySelector("#num_months_per_year").value;
            var months = document.querySelector("#month-names-container");
            var firstChild = months.firstElementChild;
            months.innerHTML = '';
            for (var i = 0; i < num_months; i++) {
                var clonedElement = firstChild.cloneNode(true);
                clonedElement.value = "";
                months.appendChild(clonedElement);
            }
            if (num_months == 12) {
                var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                var monthElements = document.querySelectorAll("#month-names-container > input");
                monthElements.forEach((element, index) => {
                    element.value = monthNames[index];
                });
            }
        });
        document.querySelector("#num_days_per_week").addEventListener("change", () => {
            var num_days = document.querySelector("#num_days_per_week").value;
            var days = document.querySelector("#day-names-container");
            var firstChild = days.firstElementChild;
            days.innerHTML = '';
            for (var i = 0; i < num_days; i++) {
                var clonedElement = firstChild.cloneNode(true);
                clonedElement.value = "";
                days.appendChild(clonedElement);
            }
            if (num_days == 7) {
                var day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                var day_elements = document.querySelectorAll("#day-names-container > input");
                day_elements.forEach((element, index) => {
                    element.value = day_names[index];
                });
            }
        });
    }
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

///////// Configure editors ///////////

// function battlemap_overlay_adjust() {
//     console.log(this.value);
//     var gridOverlay = document.getElementById('map-grid-overlay');
//     gridOverlay.classList.remove('is-hidden');
//     gridOverlay.style.backgroundSize = `${this.value}px ${this.value}px`;
// }