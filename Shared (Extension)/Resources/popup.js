document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('textareaContent');
    output.textContent = 'Loading textarea properties from the active tab...';

    // Query the active tab. Make sure a webpage (such as ChatGPT) is open.
    browser.tabs.query({active: true, currentWindow: true})
        .then((tabs) => {
            if (!tabs.length) {
                output.textContent =
                    'Error: No active tab found. Please open a webpage that contains a <textarea>.';
                return;
            }
            const activeTab = tabs[0];
            console.log('Active tab info:', activeTab);

            // Send a message to the content script to retrieve the textarea properties.
            return browser.tabs.sendMessage(activeTab.id, {action: 'getTextareaContent'});
        })
        .then((response) => {
            if (response && typeof response.content !== 'undefined') {
                console.log('Received textarea properties:', response.content);
                output.textContent = response.content;
            } else {
                output.textContent =
                    'No content returned. Ensure the current page includes a <textarea> element.';
            }
        })
        .catch((error) => {
            console.error('Error retrieving textarea properties:', error);
            output.textContent = 'Error retrieving textarea properties: ' + error;
        });
});
