// popup.js

document.addEventListener('DOMContentLoaded', () => {
    const treeContainer = document.getElementById('treeContainer');
    const refreshButton = document.getElementById('refreshButton');
    const collapseAllButton = document.getElementById('collapseAll');
    const expandAllButton = document.getElementById('expandAll');
    const modalOverlay = document.getElementById('modalOverlay');
    const modalContent = document.getElementById('modalContent');
    const modalClose = document.getElementById('modalClose');

    let domTree = null;

    /**
     * Creates an inline details element for a node.
     *
     * @param {object} node - The node data.
     * @returns {HTMLElement} - The details element.
     */
    function createDetailsElement(node) {
        const details = document.createElement('div');
        details.className = 'node-details';
        details.innerHTML = `
        <p><strong>ID:</strong> ${node.id || 'None'}</p>
        <p><strong>Classes:</strong> ${
            node.classes && node.classes.length > 0 ? node.classes.join(', ') :
                                                      'None'}</p>
        <p><strong>Text Content:</strong></p>
        <pre class="node-pre">${node.textContent || 'None'}</pre>
        <p><strong>Outer HTML:</strong></p>
        <pre class="node-pre">${node.outerHTML || 'None'}</pre>
      `;
        return details;
    }

    /**
     * Builds a breadcrumb list representing the parent chain.
     *
     * @param {Array} parents - Array of parent nodes.
     * @returns {HTMLElement} - The constructed unordered list.
     */
    function buildParentChain(parents) {
        const ul = document.createElement('ul');
        ul.className = 'parent-chain';
        parents.forEach((p) => {
            const li = document.createElement('li');
            li.textContent =
                p.tag + (p.id ? `#${p.id}` : '') +
                (p.classes && p.classes.length > 0 ? `.${p.classes.join('.')}` : '');
            ul.appendChild(li);
        });
        return ul;
    }

    /**
     * Recursively builds a full tree for a node's children (for modal display).
     *
     * @param {object} node - The node data.
     * @returns {HTMLElement} - The constructed list item.
     */
    function buildFullTree(node) {
        const li = document.createElement('li');
        li.className = 'modal-tree-node';
        const label = document.createElement('span');
        label.textContent =
            node.tag + (node.id ? `#${node.id}` : '') +
            (node.classes && node.classes.length > 0 ? `.${node.classes.join('.')}` : '');
        li.appendChild(label);
        if (node.children && node.children.length > 0) {
            const ul = document.createElement('ul');
            ul.className = 'modal-tree-children';
            node.children.forEach((child) => {
                ul.appendChild(buildFullTree(child));
            });
            li.appendChild(ul);
        }
        return li;
    }

    /**
     * Opens a modal displaying the parent chain and children tree of a node.
     *
     * @param {object} node - The node data.
     * @param {Array} parents - The array of parent nodes.
     */
    function openModalForNode(node, parents) {
        modalContent.innerHTML = '';
        const parentHeading = document.createElement('h2');
        parentHeading.textContent = 'Parent Chain';
        modalContent.appendChild(parentHeading);
        if (parents.length > 0) {
            const parentChain = buildParentChain(parents);
            modalContent.appendChild(parentChain);
        } else {
            const noParents = document.createElement('p');
            noParents.textContent = 'No parents (this is the root).';
            modalContent.appendChild(noParents);
        }
        const childrenHeading = document.createElement('h2');
        childrenHeading.textContent = 'Children Tree';
        modalContent.appendChild(childrenHeading);
        if (node.children && node.children.length > 0) {
            const ul = document.createElement('ul');
            ul.className = 'modal-tree-root';
            node.children.forEach((child) => {
                ul.appendChild(buildFullTree(child));
            });
            modalContent.appendChild(ul);
        } else {
            const noChildren = document.createElement('p');
            noChildren.textContent = 'No children.';
            modalContent.appendChild(noChildren);
        }
        modalOverlay.style.display = 'block';
    }

    // Close modal when the close button or overlay is clicked.
    modalClose.addEventListener('click', () => {
        modalOverlay.style.display = 'none';
    });
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.style.display = 'none';
        }
    });

    /**
     * Recursively builds a tree node element with lazy loading.
     *
     * @param {object} node - The DOM node data.
     * @param {Array} parents - The array of parent nodes.
     * @returns {HTMLElement} - The constructed list item.
     */
    function buildTree(node, parents = []) {
        const li = document.createElement('li');
        li.className = 'tree-node';
        li.style.position = 'relative';

        const headerDiv = document.createElement('div');
        headerDiv.className = 'node-header';

        const hasChildren = node.children && node.children.length > 0;

        const arrowIcon = document.createElement('span');
        arrowIcon.className = 'toggle-icon';
        arrowIcon.textContent = hasChildren ? '▶' : '';
        headerDiv.appendChild(arrowIcon);

        const labelSpan = document.createElement('span');
        labelSpan.className = 'node-label';
        labelSpan.textContent =
            node.tag + (node.id ? `#${node.id}` : '') +
            (node.classes && node.classes.length > 0 ? `.${node.classes.join('.')}` : '');
        headerDiv.appendChild(labelSpan);

        const detailsDiv = createDetailsElement(node);
        li.appendChild(headerDiv);
        li.appendChild(detailsDiv);

        if (hasChildren) {
            // Single-click toggles the immediate child container.
            arrowIcon.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleChildren(li, node, arrowIcon, parents);
            });
            labelSpan.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleChildren(li, node, arrowIcon, parents);
            });
        } else {
            // For leaf nodes, single-click toggles inline details.
            labelSpan.addEventListener('click', (e) => {
                e.stopPropagation();
                detailsDiv.classList.toggle('expanded');
            });
        }

        // Double-click on any node shows the modal.
        li.addEventListener('dblclick', (e) => {
            e.stopPropagation();
            openModalForNode(node, parents);
        });

        return li;
    }

    /**
     * Toggles the display of a node's immediate child container and handles the vertical
     * collapse line.
     *
     * @param {HTMLElement} li - The list item element.
     * @param {object} node - The node data.
     * @param {HTMLElement} arrowIcon - The arrow icon element.
     * @param {Array} parents - The array of parent nodes.
     */
    function toggleChildren(li, node, arrowIcon, parents) {
        let childContainer = li.querySelector('ul.tree-children');
        let collapseLine = li.querySelector('.collapse-line');

        if (!childContainer) {
            // Create child container lazily.
            childContainer = document.createElement('ul');
            childContainer.className = 'tree-children';
            const frag = document.createDocumentFragment();
            node.children.forEach((child) => {
                frag.appendChild(buildTree(child, parents.concat([node])));
            });
            childContainer.appendChild(frag);
            li.appendChild(childContainer);
            arrowIcon.textContent = '▼';

            // Create the vertical collapse line, shifted down 2px.
            collapseLine = document.createElement('div');
            collapseLine.className = 'collapse-line';
            const headerDiv = li.querySelector('.node-header');
            if (headerDiv) {
                collapseLine.style.top = (headerDiv.offsetHeight + 2) + 'px';
                collapseLine.style.left = '0';
            }
            collapseLine.addEventListener('click', (e) => {
                e.stopPropagation();
                childContainer.style.display = 'none';
                arrowIcon.textContent = '▶';
                collapseLine.remove();
                const headerDiv = li.querySelector('.node-header');
                if (headerDiv) {
                    headerDiv.scrollIntoView({behavior: 'smooth', block: 'nearest'});
                }
            });
            li.appendChild(collapseLine);
        } else {
            // Toggle only the immediate container.
            if (childContainer.style.display === 'none' ||
                childContainer.style.display === '') {
                childContainer.style.display = 'block';
                arrowIcon.textContent = '▼';
                // If collapse line doesn't exist, create it.
                if (!collapseLine) {
                    collapseLine = document.createElement('div');
                    collapseLine.className = 'collapse-line';
                    const headerDiv = li.querySelector('.node-header');
                    if (headerDiv) {
                        collapseLine.style.top = (headerDiv.offsetHeight + 2) + 'px';
                        collapseLine.style.left = '0';
                    }
                    collapseLine.addEventListener('click', (e) => {
                        e.stopPropagation();
                        childContainer.style.display = 'none';
                        arrowIcon.textContent = '▶';
                        collapseLine.remove();
                        const headerDiv = li.querySelector('.node-header');
                        if (headerDiv) {
                            headerDiv.scrollIntoView(
                                {behavior: 'smooth', block: 'nearest'});
                        }
                    });
                    li.appendChild(collapseLine);
                }
            } else {
                childContainer.style.display = 'none';
                arrowIcon.textContent = '▶';
                if (collapseLine) {
                    collapseLine.remove();
                    const headerDiv = li.querySelector('.node-header');
                    if (headerDiv) {
                        headerDiv.scrollIntoView({behavior: 'smooth', block: 'nearest'});
                    }
                }
            }
        }
    }

    /**
     * Renders the DOM tree inside the tree container.
     *
     * @param {object} tree - The hierarchical DOM tree data.
     */
    function renderTree(tree) {
        treeContainer.innerHTML = '';
        const ul = document.createElement('ul');
        ul.className = 'tree-root';
        ul.appendChild(buildTree(tree, []));
        treeContainer.appendChild(ul);
    }

    /**
     * Retrieves the DOM tree from the active tab.
     */
    function fetchDomTree() {
        return browser.tabs.query({active: true, currentWindow: true})
            .then((tabs) => {
                const activeTab = tabs[0];
                return browser.tabs.sendMessage(activeTab.id, {command: 'getDomTree'})
                    .then((response) => {
                        if (response && response.tree) {
                            domTree = response.tree;
                            renderTree(domTree);
                        } else {
                            treeContainer.innerHTML =
                                '<p class="error">No DOM tree found.</p>';
                        }
                    })
                    .catch((error) => {
                        console.error('Error fetching DOM tree', error);
                        treeContainer.innerHTML =
                            '<p class="error">Error retrieving DOM tree.</p>';
                    });
            })
            .catch((error) => {
                console.error('Error querying tabs', error);
                treeContainer.innerHTML = '<p class="error">Error querying tabs.</p>';
            });
    }

    /**
     * Collapses all loaded immediate child containers and inline details.
     */
    function collapseAll() {
        const childContainers = treeContainer.querySelectorAll('ul.tree-children');
        childContainers.forEach((ul) => {
            ul.style.display = 'none';
            const parentLi = ul.parentElement;
            const arrow = parentLi.querySelector('.toggle-icon');
            if (arrow) {
                arrow.textContent = '▶';
            }
            const collapseLine = parentLi.querySelector('.collapse-line');
            if (collapseLine)
                collapseLine.remove();
        });
        const details = treeContainer.querySelectorAll('.node-details.expanded');
        details.forEach((d) => {
            d.classList.remove('expanded');
        });
    }

    /**
     * Expands all loaded immediate child containers.
     */
    function expandAll() {
        const childContainers = treeContainer.querySelectorAll('ul.tree-children');
        childContainers.forEach((ul) => {
            ul.style.display = 'block';
            const parentLi = ul.parentElement;
            const arrow = parentLi.querySelector('.toggle-icon');
            if (arrow) {
                arrow.textContent = '▼';
            }
            if (!parentLi.querySelector('.collapse-line')) {
                const collapseLine = document.createElement('div');
                collapseLine.className = 'collapse-line';
                const headerDiv = parentLi.querySelector('.node-header');
                if (headerDiv) {
                    collapseLine.style.top = (headerDiv.offsetHeight + 2) + 'px';
                    collapseLine.style.left = '0';
                }
                collapseLine.addEventListener('click', (e) => {
                    e.stopPropagation();
                    ul.style.display = 'none';
                    arrow.textContent = '▶';
                    collapseLine.remove();
                    const headerDiv = parentLi.querySelector('.node-header');
                    if (headerDiv) {
                        headerDiv.scrollIntoView({behavior: 'smooth', block: 'nearest'});
                    }
                });
                parentLi.appendChild(collapseLine);
            }
        });
    }

    collapseAllButton.addEventListener('click', collapseAll);
    expandAllButton.addEventListener('click', expandAll);

    refreshButton.addEventListener('click', () => {
        refreshButton.classList.add('rotating');
        fetchDomTree().finally(() => {
            setTimeout(() => {
                refreshButton.classList.remove('rotating');
            }, 500);
        });
    });

    fetchDomTree();
});
