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

//document.getElementById('go_button').addEventListener('click', () => {
    //const searchInput = document.getElementById('search_input').value.trim();
    //if (!searchInput) return;

    // Add to localStorage
    //let searches = JSON.parse(localStorage.getItem("searches") || "[]");
    //searches.push(searchInput);
    //localStorage.setItem("searches", JSON.stringify(searches));

    //updateHistoryDisplay();

    //socket.emit('Go_button_pushed', { search: searchInput });

    //document.getElementById('search_input').value = "";
//});

document.getElementById('go_button').addEventListener("click", () => {
    const query = document.getElementById("search_input").value.trim();
    if (!query)
        return;

    //save search
    let searches = JSON.parse(localStorage.getItem("searches") || "[]");
    searches.push(query);
    localStorage.setItem("searches", JSON.stringify(searches));

    updateHistoryDisplay();

    try {
        socket.emit("Go_button_pushed", { search: query});
    } catch (err) {
        console.warn("Socket error: ", err);
    }

    // display loading screen
    document.getElementById("loading-screen-overlay").style.display = "flex";

    // redirect to results page route
    socket.on('redirect', (url) => {
        window.location.href = url;
    });
});

// ENTER key triggers search

document.getElementById("search_input").addEventListener("keydown", (e) => {
    if (e.key == "Enter") {
        document.getElementById("go_button").click();
    }
});

socket.on('set_best_book_cookie', (data) => {
    document.cookie = "best_book=" + encodeURIComponent(data) + "; max-age=" + (60*60*24) + "; path=/";
    console.log("Best book cookie set via SocketIO");
})