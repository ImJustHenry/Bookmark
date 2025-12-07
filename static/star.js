// star.js

function getCurrentBookFromPage() {
    const title = document.querySelector(".bookInfo h2")?.textContent.trim();
    const isbnText = document.querySelector(".bookInfo p")?.textContent.trim();
    const linkEl = document.querySelector(".priceElement a");
    const imageEl = document.querySelector(".textbook-image");

    const conditionEl = document.querySelector(".priceElement p:nth-of-type(2)");
    const mediumEl = document.querySelector(".priceElement p:nth-of-type(3)");
    const priceEl = document.querySelector(".priceElement p:nth-of-type(1)");

    if (!title) return null;

    const isbn = isbnText ? isbnText.replace("ISBN:", "").trim() : "";
    const price = priceEl ? priceEl.textContent.replace("$", "").trim() : "";
    const link = linkEl ? linkEl.href : "";
    const image = imageEl ? imageEl.src : "";
    const condition = conditionEl ? conditionEl.textContent.replace("Condition: ", "").trim() : "N/A";
    const medium = mediumEl ? mediumEl.textContent.replace("Medium: ", "").trim() : "N/A";

    return { title, isbn, price, link, image, condition, medium };
}

function showPopup(message) {
    let popup = document.createElement("div");
    popup.textContent = message;
    popup.style.position = "fixed";
    popup.style.bottom = "20px";
    popup.style.left = "50%";
    popup.style.transform = "translateX(-50%)";
    popup.style.background = "#22874f";
    popup.style.color = "#fff";
    popup.style.padding = "10px 20px";
    popup.style.borderRadius = "20px";
    popup.style.boxShadow = "0 4px 12px rgba(0,0,0,0.25)";
    popup.style.zIndex = 1000;
    popup.style.opacity = 0;
    popup.style.transition = "opacity 0.3s ease";

    document.body.appendChild(popup);

    requestAnimationFrame(() => {
        popup.style.opacity = 1;
    });

    setTimeout(() => {
        popup.style.opacity = 0;
        setTimeout(() => popup.remove(), 300);
    }, 2000);
}

function updateStar(currentBook) {
    const starButton = document.getElementById("topFavorite");
    if (!starButton || !currentBook) return;

    let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];

    if (wishlist.some(item => item.isbn === currentBook.isbn)) {
        starButton.classList.add("active");
    } else {
        starButton.classList.remove("active");
    }

    const newStarButton = starButton.cloneNode(true);
    starButton.parentNode.replaceChild(newStarButton, starButton);

    newStarButton.addEventListener("click", () => {
        let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];

        if (wishlist.some(item => item.isbn === currentBook.isbn)) {
            wishlist = wishlist.filter(item => item.isbn !== currentBook.isbn);
            newStarButton.classList.remove("active");
            showPopup("Removed from wishlist ❌");
        } else {
            wishlist.push(currentBook);
            newStarButton.classList.add("active");
            showPopup("Added to wishlist ⭐ Click star to favorite to wishlist!");
        }

        localStorage.setItem("wishlist", JSON.stringify(wishlist));
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const currentBook = getCurrentBookFromPage();
    updateStar(currentBook);
});
