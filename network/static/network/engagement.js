const engagementContainer = document.querySelector('.posts-container'); 
const post_id = engagementContainer ? parseInt(engagementContainer.dataset.trackPostId) : null;
let lastUpdate = Date.now();

// Sends an update every 20 seconds while user is on the page
const interval = post_id ? setInterval(() => {
    const now = Date.now();
    const elapsed = Math.floor((now - lastUpdate)/ 1000);
    
    if (elapsed > 0) {
        const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
        fetch(`/post/${post_id}/track/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({seconds: elapsed})
        });
        lastUpdate = now;
    }
}, 20000) : null;

window.addEventListener('beforeunload', () => {
    if (!post_id) return;
    const elapsed = Math.floor((Date.now() - lastUpdate) / 1000);
    if (elapsed > 0) {
        navigator.sendBeacon(`/post/${post_id}/track/`, JSON.stringify({seconds: elapsed}));
    }
});

window.addEventListener('pagehide', () => { if (interval) clearInterval(interval); });