// Helper function that searches the given root for a <textarea> element.
function findTextarea(root) {
    return root.querySelector('textarea');
}

// This function calls sendResponse with the textarea properties.
// It builds the properties object regardless of whether the textarea is visible.
function reportTextarea(sendResponse, textarea) {
    if (!textarea) {
        console.log('No <textarea> element found on the page.');
        sendResponse({content: 'No <textarea> element found on the page.'});
        return;
    }

    let properties = {
        id: textarea.id,
        name: textarea.name,
        classList: Array.from(textarea.classList),
        rows: textarea.rows,
        cols: textarea.cols,
        value: textarea.value,
        placeholder: textarea.placeholder,
        disabled: textarea.disabled,
        readOnly: textarea.readOnly,
        innerHTML: textarea.innerHTML,
        outerHTML: textarea.outerHTML,
        style: textarea.style.cssText,
        attributes: {}
    };

    // Add all attributes from the textarea element.
    for (let attr of textarea.attributes) {
        properties.attributes[attr.name] = attr.value;
    }

    console.log('Textarea properties collected:', properties);
    sendResponse({content: JSON.stringify(properties, null, 2)});
}

// If the document is still loading, wait for DOMContentLoaded.
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

function init() {
    console.log('Content script initialized.');

    // Listen for messages from the popup.
    browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
        console.log('Content script received message:', message);

        if (message.action === 'getTextareaContent') {
            let textarea = findTextarea(document);

            // If no textarea is found immediately, set up a MutationObserver.
            if (!textarea) {
                console.log(
                    'Textarea not found immediately. Setting up MutationObserver...');
                const observer = new MutationObserver((mutations, obs) => {
                    textarea = findTextarea(document);
                    if (textarea) {
                        console.log('Textarea found via MutationObserver.');
                        obs.disconnect();
                        reportTextarea(sendResponse, textarea);
                    }
                });
                observer.observe(document.body, {childList: true, subtree: true});

                // In case the textarea never appears, disconnect after 5 seconds and
                // report nothing.
                setTimeout(() => {
                    observer.disconnect();
                    if (!findTextarea(document)) {
                        console.log('Textarea still not found after waiting.');
                        sendResponse({
                            content:
                                'No <textarea> element found on the page (after waiting).'
                        });
                    }
                }, 5000);
                // Return true to indicate we'll call sendResponse asynchronously.
                return true;
            } else {
                reportTextarea(sendResponse, textarea);
            }
        }
    });
}
