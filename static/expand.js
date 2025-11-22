document.addEventListener("DOMContentLoaded", function() {
    const outer = document.querySelector(".summary-outer");
    const readMore = document.getElementById("readMore");

    readMore.addEventListener("click", function() {
        outer.classList.toggle("expanded");
        readMore.textContent = outer.classList.contains("expanded") ? "Read less" : "Read more";
    });
});
