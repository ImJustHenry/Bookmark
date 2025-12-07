const socket = io();

function updateHistoryDisplay() {
    const history = JSON.parse(localStorage.getItem("searches") || "[]");
    const dataList = document.getElementById("history_list");
    dataList.innerHTML = "";
    history.forEach(term => {
        const option = document.createElement("option");
        option.value = term;
        dataList.appendChild(option);
    });
}

document.getElementById('go_button').addEventListener("click", () => {
    const query = document.getElementById("search_input").value.trim();
    if (!query) return;

    // Save search history in localStorage
    let searches = JSON.parse(localStorage.getItem("searches") || "[]");
    searches.push(query);
    localStorage.setItem("searches", JSON.stringify(searches));
    updateHistoryDisplay();

    // Show loading screen
    document.getElementById("loading-screen-overlay").style.display = "flex";

    try {
        socket.emit("Go_button_pushed", { search: query });
    } catch (err) {
        console.warn("Socket error: ", err);
        document.getElementById("loading-screen-overlay").style.display = "none";
    }
});

// Listen for server confirmation before redirecting
socket.on('redirect', (url) => {
    // Hide loading screen and redirect
    document.getElementById("loading-screen-overlay").style.display = "none";
    window.location.href = url;
});

// Optional: handle search errors
socket.on('search_error', (data) => {
    alert(data.error || "Search failed");
    document.getElementById("loading-screen-overlay").style.display = "none";
});

// ENTER key triggers search
document.getElementById("search_input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        document.getElementById("go_button").click();
    }
});

socket.on('set_best_book_cookie', (data) => {
    document.cookie = "best_book=" + encodeURIComponent(data) + "; max-age=" + (60*60*24) + "; path=/";
    console.log("Best book cookie set via SocketIO");
})