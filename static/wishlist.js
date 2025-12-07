document.addEventListener("DOMContentLoaded", () => {
    const bookListContainer = document.getElementById("bookListContainer");
    const popup = document.getElementById("popupContainer");

    function showPopup(message) {
        popup.textContent = message;
        popup.style.opacity = 1;
        setTimeout(() => { popup.style.opacity = 0; }, 2000);
    }

    function renderWishlist() {
        bookListContainer.innerHTML = "";
        const wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];

        if (wishlist.length === 0) {
            bookListContainer.innerHTML = "<p style='text-align:center; font-size:18px; color:white;'>You have no saved books yet.</p>";
            return;
        }

        wishlist.forEach(book => {
            const card = document.createElement("div");
            card.className = "bookCard";
            card.innerHTML = `
                <img src="${book.image || ''}" alt="${book.title}">
                <h3>${book.title}</h3>
                <p>ISBN: ${book.isbn}</p>
                <div class="price">$${book.price}</div>
                <a href="${book.link}" target="_blank">
                    <button class="goToSiteButton">Go to store</button>
                </a>
                <button class="removeButton">Remove from wishlist</button>
            `;

            card.querySelector(".removeButton").addEventListener("click", () => {
                let updatedWishlist = JSON.parse(localStorage.getItem("wishlist")) || [];
                updatedWishlist = updatedWishlist.filter(item => item.isbn !== book.isbn);
                localStorage.setItem("wishlist", JSON.stringify(updatedWishlist));
                showPopup(`Removed "${book.title}" from wishlist ❌`);
                renderWishlist();
            });

            bookListContainer.appendChild(card);
        });
    }

    renderWishlist();
});