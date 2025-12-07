// star.js

function getCurrentBookFromPage() {
    const bookInfo = document.querySelector(".bookInfo h2")?.textContent;
    const priceText = document.querySelector(".priceElement p")?.textContent;
    const linkEl = document.querySelector(".priceElement a");
    const imageEl = document.querySelector(".textbook-image");

    if (!bookInfo) return null;

    const [title, isbn] = bookInfo.split(" - ").map(s => s.trim());
    const price = priceText ? priceText.replace("$", "").trim() : "";
    const link = linkEl ? linkEl.href : "";
    const image = imageEl ? imageEl.src : "";

    return { title, isbn, price, link, image };
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

    // Fade in
    requestAnimationFrame(() => {
        popup.style.opacity = 1;
    });

    // Fade out and remove after 2 seconds
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

    // Remove old listeners
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
            showPopup("Added to wishlist ⭐");
        }

        localStorage.setItem("wishlist", JSON.stringify(wishlist));
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const currentBook = getCurrentBookFromPage();
    updateStar(currentBook);
});
