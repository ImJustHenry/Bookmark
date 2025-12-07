  // Connect to the Socket.IO server
  const socket = io();

  // Listen for the event (replace "redirectNow" with your event name)
  socket.on("search_done", (data) => {
    // data could contain a URL; use it or hardcode a URL
    const targetUrl = data?.url || "/results";

    // Redirect
    window.location.href = targetUrl;
  });