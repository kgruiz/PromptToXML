// Global array to hold any connected ports from the popup.
let ports = [];

// Helper function to search for a <textarea> element.
function findTextarea(root) {
    return root.querySelector('textarea');
}

// Function to build and return a properties object for a textarea element.
function buildProperties(textarea) {
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

    for (let attr of textarea.attributes) {
        properties.attributes[attr.name] = attr.value;
    }
    return properties;
}

// Function to report (send) the current textarea properties to all connected ports.
function reportTextarea(textarea) {
    const props = buildProperties(textarea);
    // Send the full properties (formatted as JSON) via each port.
    ports.forEach(port => {
        port.postMessage({type: 'update', properties: props});
    });
}

// Set up a listener for long‑lived connections from the popup.
browser.runtime.onConnect.addListener(port => {
    if (port.name === 'textarea-monitor') {
        ports.push(port);
        // When the port disconnects, remove it.
        port.onDisconnect.addListener(() => {
            ports = ports.filter(p => p !== port);
        });
    }
});

// Function to initialize monitoring once the DOM is ready.
function init() {
    console.log('Content script initialized.');

    let textarea = findTextarea(document);

    // If no textarea is found immediately, set up a MutationObserver.
    if (!textarea) {
        console.log('Textarea not found immediately. Setting up MutationObserver...');
        const observer = new MutationObserver((mutations, obs) => {
            textarea = findTextarea(document);
            if (textarea) {
                console.log('Textarea found via MutationObserver.');
                obs.disconnect();
                attachListener(textarea);
                reportTextarea(textarea);
            }
        });
        observer.observe(document.body, {childList: true, subtree: true});
        // Optionally disconnect after a timeout if nothing appears.
        setTimeout(() => {
            observer.disconnect();
            if (!findTextarea(document)) {
                ports.forEach(port => port.postMessage({
                    type: 'error',
                    message: 'No <textarea> element found on the page (after waiting).'
                }));
            }
        }, 5000);
    } else {
        attachListener(textarea);
        reportTextarea(textarea);
    }
}

// Attach an "input" event listener to the textarea so that every change triggers an
// update.
function attachListener(textarea) {
    // If not already attached, add an event listener.
    if (!textarea.__monitorAttached) {
        textarea.addEventListener('input', () => {
            reportTextarea(textarea);
        });
        textarea.__monitorAttached = true;
    }
}

// Wait for the document to be ready.
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Also listen for explicit messages from the popup (for one‑time requests).
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getTextareaContent') {
        let textarea = findTextarea(document);
        if (textarea) {
            sendResponse({content: JSON.stringify(buildProperties(textarea), null, 2)});
        } else {
            sendResponse({content: 'No <textarea> element found on the page.'});
        }
    }
});
