// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'Minted';
    const body = data.body || 'Minted - Your personal spending tracker';

    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: 'https://i.imgur.com/vN2CQRD.png'
        })
    );
});