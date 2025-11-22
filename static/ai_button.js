const socket = io();

const aiContainer = document.querySelector(".aiRecommendation");
const aiButton = aiContainer.querySelector("#aiButton");
const aiResults = aiContainer.querySelector("#aiResults");

const currentBook = aiContainer.dataset.title;

aiButton.addEventListener("click", () => {
    aiResults.innerHTML = "<p>Loading recommendations...</p>";
    aiButton.style.display = "none"; 

    let history = JSON.parse(localStorage.getItem("searches") || "[]");
    history = history.slice(-5);

    socket.emit("get_ai_recommendations", {
        currentBook,
        history
    });
});

socket.on("ai_recommendations", (books) => {
    aiResults.innerHTML = "";

    books.forEach((book, index) => {
        const container = document.createElement("div");
        container.style.display = "flex";
        container.style.justifyContent = "space-between";
        container.style.alignItems = "center";
        container.style.marginBottom = "10px";
        container.style.padding = "10px";
        container.style.borderBottom = "1px solid #ccc";
        container.style.flexWrap = "wrap";

        const p = document.createElement("p");
        p.style.margin = "0 10px 0 0";
        p.style.flex = "1 1 auto";
        p.innerHTML = `${index + 1}. <strong>${book.title}</strong>: ${book.summary}`;

        const btn = document.createElement("button");
        btn.textContent = "Check Optimal Price";
        btn.className = "goToSiteButton";
        btn.style.height = "30px";
        btn.style.fontSize = "13px";
        btn.style.flex = "0 0 auto";
        btn.style.padding = "5px 10px";

        btn.addEventListener("click", () => {
            socket.emit("Go_button_pushed", { search: book.title });
        });

        container.appendChild(p);
        container.appendChild(btn);
        aiResults.appendChild(container);
    });
});

// Listen for server redirect
socket.on("redirect", (url) => {
    window.location.href = url; 
});

socket.on("ai_error", (msg) => {
    aiResults.innerHTML = `<p style="color:red;">Error: ${msg}</p>`;
});
