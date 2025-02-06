document.addEventListener('DOMContentLoaded', () => {
    // Query the active tab and send a message to retrieve the textarea content.
    browser.tabs.query({active: true, currentWindow: true})
        .then((tabs) => {
            let activeTab = tabs[0];
            return browser.tabs.sendMessage(activeTab.id, {action: 'getTextareaContent'});
        })
        .then((response) => {
            const content = response.content || 'No textarea found.';
            document.getElementById('textareaContent').textContent = content;
        })
        .catch((error) => {
            document.getElementById('textareaContent').textContent = 'Error: ' + error;
        });
});
