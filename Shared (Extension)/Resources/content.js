browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getTextareaContent') {
        const textarea = document.querySelector('textarea');
        const content = textarea ? textarea.value : '';
        sendResponse({content: content});
    }
});
