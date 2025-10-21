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

document.getElementById('go_button').addEventListener('click', () => {
    const searchInput = document.getElementById('search_input').value.trim();
    if (!searchInput) return;

    // Add to localStorage
    let searches = JSON.parse(localStorage.getItem("searches") || "[]");
    searches.push(searchInput);
    localStorage.setItem("searches", JSON.stringify(searches));

    updateHistoryDisplay();

    socket.emit('Go_button_pushed', { search: searchInput });

    document.getElementById('search_input').value = "";
});
