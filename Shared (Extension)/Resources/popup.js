document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('textareaContent');
    output.textContent = 'Waiting for textarea updates from the active tab...';

    // Query the active tab.
    browser.tabs.query({active: true, currentWindow: true})
        .then((tabs) => {
            if (!tabs.length) {
                output.textContent =
                    'Error: No active tab found. Please open a webpage that contains a <textarea>.';
                return;
            }
            const activeTab = tabs[0];
            console.log('Active tab info:', activeTab);

            // Establish a long-lived connection with the content script.
            const port = browser.tabs.connect(activeTab.id, {name: 'textarea-monitor'});

            // Listen for messages from the content script.
            port.onMessage.addListener(message => {
                if (message.type === 'update' && message.properties) {
                    console.log('Received update from content script:',
                                message.properties);
                    // Update the popup display (here we simply show the formatted JSON).
                    output.textContent = JSON.stringify(message.properties, null, 2);
                } else if (message.type === 'error') {
                    output.textContent = 'Error: ' + message.message;
                }
            });

            // Optionally, you can also request an immediate one‑time update.
            browser.tabs.sendMessage(activeTab.id, {action: 'getTextareaContent'})
                .then(response => {
                    if (response && response.content) {
                        output.textContent = response.content;
                    }
                })
                .catch(error => {
                    console.error('Error retrieving initial textarea content:', error);
                    output.textContent = 'Error: ' + error;
                });
        })
        .catch((error) => {
            console.error('Error querying active tab:', error);
            output.textContent = 'Error: ' + error;
        });
});
