// popup.js

document.addEventListener('DOMContentLoaded', () => {
    const treeContainer = document.getElementById('treeContainer');
    const refreshButton = document.getElementById('refreshButton');
    const modalOverlay = document.getElementById('modalOverlay');
    const closeModalButton = document.getElementById('closeModal');
    const modalDetails = document.getElementById('modalDetails');

    let domTree = null;

    /**
     * Recursively builds a tree node element.
     *
     * @param {object} node - The DOM node data.
     * @returns {HTMLElement} - The constructed tree node <li>.
     */
    function buildTree(node) {
        const li = document.createElement('li');
        li.className = 'tree-node';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'node-header';

        // Prepare toggle icon for nodes with children.
        let childUl = null;
        if (node.children && node.children.length > 0) {
            const toggleIcon = document.createElement('span');
            toggleIcon.className = 'toggle-icon';
            toggleIcon.textContent = '▼';  // Initially expanded.
            headerDiv.appendChild(toggleIcon);

            // Event listener to toggle visibility of children.
            toggleIcon.addEventListener('click', (e) => {
                e.stopPropagation();
                if (childUl) {
                    if (childUl.style.display === 'none') {
                        childUl.style.display = 'block';
                        toggleIcon.textContent = '▼';
                    } else {
                        childUl.style.display = 'none';
                        toggleIcon.textContent = '▶';
                    }
                }
            });
        } else {
            // Spacer for alignment if no children.
            const spacer = document.createElement('span');
            spacer.className = 'toggle-icon';
            spacer.textContent = '';
            headerDiv.appendChild(spacer);
        }

        const labelSpan = document.createElement('span');
        labelSpan.className = 'node-label';
        labelSpan.textContent = node.tag;
        if (node.id) {
            labelSpan.textContent += `#${node.id}`;
        }
        if (node.classes && node.classes.length > 0) {
            labelSpan.textContent += `.${node.classes.join('.')}`;
        }
        headerDiv.appendChild(labelSpan);

        // Clicking the header opens the modal with full details.
        headerDiv.addEventListener('click', () => {
            openModal(node);
        });

        li.appendChild(headerDiv);

        // Recursively build children if they exist.
        if (node.children && node.children.length > 0) {
            childUl = document.createElement('ul');
            childUl.className = 'tree-children';
            node.children.forEach(child => {
                childUl.appendChild(buildTree(child));
            });
            li.appendChild(childUl);
        }

        return li;
    }

    /**
     * Renders the DOM tree in the tree container.
     *
     * @param {object} tree - The hierarchical DOM tree data.
     */
    function renderTree(tree) {
        treeContainer.innerHTML = '';
        const ul = document.createElement('ul');
        ul.className = 'tree-root';
        ul.appendChild(buildTree(tree));
        treeContainer.appendChild(ul);
    }

    /**
     * Fetches the DOM tree from the active tab via the content script.
     *
     * @returns {Promise<void>}
     */
    function fetchDomTree() {
        return browser.tabs.query({active: true, currentWindow: true})
            .then(tabs => {
                const activeTab = tabs[0];
                return browser.tabs.sendMessage(activeTab.id, {command: 'getDomTree'})
                    .then(response => {
                        if (response && response.tree) {
                            domTree = response.tree;
                            renderTree(domTree);
                        } else {
                            treeContainer.innerHTML =
                                '<p class=\'error\'>No DOM tree found.</p>';
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching DOM tree', error);
                        treeContainer.innerHTML =
                            '<p class=\'error\'>Error retrieving DOM tree.</p>';
                    });
            })
            .catch(error => {
                console.error('Error querying tabs', error);
                treeContainer.innerHTML = '<p class=\'error\'>Error querying tabs.</p>';
            });
    }

    /**
     * Opens the modal to show full details about a node.
     *
     * @param {object} node - The DOM node data.
     */
    function openModal(node) {
        modalDetails.innerHTML = `
        <h2>${node.tag.toUpperCase()}</h2>
        <p><strong>ID:</strong> ${node.id || 'None'}</p>
        <p><strong>Classes:</strong> ${
            node.classes && node.classes.length > 0 ? node.classes.join(', ') :
                                                      'None'}</p>
        <p><strong>Text Content:</strong></p>
        <pre class="modal-pre">${node.textContent || 'None'}</pre>
        <p><strong>Outer HTML:</strong></p>
        <pre class="modal-pre">${node.outerHTML || 'None'}</pre>
      `;
        modalOverlay.classList.add('open');
    }

    // Refresh button with animation.
    refreshButton.addEventListener('click', () => {
        refreshButton.classList.add('rotating');
        fetchDomTree().finally(() => {
            setTimeout(() => {
                refreshButton.classList.remove('rotating');
            }, 500);
        });
    });

    // Close modal events.
    closeModalButton.addEventListener('click', () => {
        modalOverlay.classList.remove('open');
    });
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.classList.remove('open');
        }
    });

    // Initial fetch of DOM tree.
    fetchDomTree();
});
