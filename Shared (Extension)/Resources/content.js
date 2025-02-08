// content.js

/**
 * Recursively traverses the DOM to build a hierarchical representation.
 *
 * @param {Element} element - The current DOM element.
 * @returns {object} - The hierarchical representation of the element.
 */
function traverse(element) {
    let text = element.textContent ? element.textContent.trim() : '';
    if (text.length > 50) {
        text = text.substring(0, 50) + '...';
    }
    const node = {
        tag: element.tagName.toLowerCase(),
        id: element.id || '',
        classes: Array.from(element.classList),
        textContent: text,
        outerHTML: element.outerHTML,
        children: []
    };
    Array.from(element.children).forEach(child => {
        node.children.push(traverse(child));
    });
    return node;
}

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.command === 'getDomTree') {
        const tree = traverse(document.documentElement);
        sendResponse({tree});
    }
});
