// ⚙️ Refactored for native drakonWidget API integration
// All custom insertion logic replaced with official drakonwidget methods

document.addEventListener('DOMContentLoaded', () => {
    const diagramNav = document.getElementById('diagram-nav');
    const drakonContainer = document.getElementById('drakon-container');
    const diagramTitle = document.getElementById('diagram-title');
    const sidebar = document.getElementById('sidebar');
    const sidebarBackdrop = document.getElementById('sidebar-backdrop');
    const menuBtn = document.getElementById('menu-btn');
    const zoomInBtn = document.getElementById('zoom-in-btn');
    const zoomOutBtn = document.getElementById('zoom-out-btn');
    const resetZoomBtn = document.getElementById('reset-zoom-btn');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const zoomLevelDisplay = document.getElementById('zoom-level');
    const editModeBtn = document.getElementById('edit-mode-btn');
    const undoBtn = document.getElementById('undo-btn');
    const redoBtn = document.getElementById('redo-btn');
    const saveBtn = document.getElementById('save-btn');
    const editModeIndicator = document.getElementById('edit-mode-indicator');
    const unsavedIndicator = document.getElementById('unsaved-indicator');
    const editModal = document.getElementById('edit-modal');
    const editContentInput = document.getElementById('edit-content');
    const editTypeSelect = document.getElementById('edit-type');
    const modalClose = document.getElementById('modal-close');
    const modalCancel = document.getElementById('modal-cancel');
    const modalSave = document.getElementById('modal-save');
    const newDiagramBtn = document.getElementById('new-diagram-btn');
    const addNodeButtons = document.getElementById('add-node-buttons');
    const deleteNodeBtn = document.getElementById('delete-node-btn');
    const propertiesPanel = document.getElementById('properties-panel');
    const panelToggle = document.getElementById('panel-toggle');
    const nodePropertiesSection = document.getElementById('node-properties');
    const fileInput = document.getElementById('file-input');
    const floatingPanelBtn = document.getElementById('floating-panel-btn');

    // Properties Panel elements
    const panelNewBtn = document.getElementById('panel-new-btn');
    const panelOpenBtn = document.getElementById('panel-open-btn');
    const panelSaveBtn = document.getElementById('panel-save-btn');
    const panelExportJsonBtn = document.getElementById('panel-export-json-btn');
    const panelExportPngBtn = document.getElementById('panel-export-png-btn');
    const propId = document.getElementById('prop-id');
    const propType = document.getElementById('prop-type');
    const propContent = document.getElementById('prop-content');
    const propBranch = document.getElementById('prop-branch');
    const propApply = document.getElementById('prop-apply');
    const propDelete = document.getElementById('prop-delete');
    const infoName = document.getElementById('info-name');
    const infoNodes = document.getElementById('info-nodes');
    const infoMode = document.getElementById('info-mode');

    let drakonWidget = null;
    let currentEditingItemId = null;
    let currentCanvas = null;
    let zoomLevel = 1.0;
    let panState = {
        isPanning: false,
        startX: 0,
        startY: 0,
        scrollLeft: 0,
        scrollTop: 0
    };
    let loadingTimeout = null;

    // Initialize State Manager
    const stateManager = new DiagramStateManager();

    // ==================== LOADING STATE MANAGEMENT ====================
    function showLoading(message = 'Завантаження...') {
        // Clear any existing timeout
        if (loadingTimeout) {
            clearTimeout(loadingTimeout);
        }

        drakonContainer.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>${message}</p>
            </div>
        `;

        // Set timeout fallback (5 seconds)
        loadingTimeout = setTimeout(() => {
            if (drakonContainer.querySelector('.loading')) {
                showError('Завантаження займає занадто довго. Спробуйте оновити сторінку або створити нову діаграму.');
            }
        }, 5000);
    }

    function hideLoading() {
        if (loadingTimeout) {
            clearTimeout(loadingTimeout);
            loadingTimeout = null;
        }
    }

    function showError(message) {
        drakonContainer.innerHTML = `
            <div style="text-align: center; padding: 40px; color: var(--text-color);">
                <p class="error">❌ ${message}</p>
                <button class="toolbar-btn" onclick="location.reload()" style="margin-top: 20px;">
                    🔄 Оновити сторінку
                </button>
            </div>
        `;
    }

    function showEmptyState() {
        drakonContainer.innerHTML = `
            <div style="text-align: center; padding: 40px; color: var(--text-color);">
                <p style="font-size: 1.2em; margin-bottom: 20px;">Оберіть діаграму зі списку або створіть нову</p>
                <button class="toolbar-btn" id="empty-state-new-btn" style="font-size: 1.1em; padding: 12px 24px;">
                    📄 Створити нову діаграму
                </button>
            </div>
        `;

        // Add event listener for empty state button
        const emptyStateBtn = document.getElementById('empty-state-new-btn');
        if (emptyStateBtn) {
            emptyStateBtn.addEventListener('click', createNewDiagram);
        }
    }

    // ==================== LOCAL STORAGE MANAGEMENT ====================
    const STORAGE_KEY = 'drakon_diagrams';
    const STORAGE_META_KEY = 'drakon_diagrams_meta';

    // Storage utilities
    function saveDiagramToStorage(diagram) {
        try {
            const diagrams = loadDiagramsFromStorage();
            const diagramId = diagram.id || generateDiagramId(diagram.name);
            diagram.id = diagramId;
            diagram.lastModified = new Date().toISOString();

            diagrams[diagramId] = diagram;
            localStorage.setItem(STORAGE_KEY, JSON.stringify(diagrams));

            console.log('Diagram saved to localStorage:', diagramId);
            return diagramId;
        } catch (error) {
            console.error('Error saving to localStorage:', error);
            return null;
        }
    }

    function loadDiagramsFromStorage() {
        try {
            const data = localStorage.getItem(STORAGE_KEY);
            return data ? JSON.parse(data) : {};
        } catch (error) {
            console.error('Error loading from localStorage:', error);
            return {};
        }
    }

    function getDiagramFromStorage(id) {
        const diagrams = loadDiagramsFromStorage();
        return diagrams[id] || null;
    }

    function deleteDiagramFromStorage(id) {
        try {
            const diagrams = loadDiagramsFromStorage();
            delete diagrams[id];
            localStorage.setItem(STORAGE_KEY, JSON.stringify(diagrams));
            console.log('Diagram deleted from localStorage:', id);
            return true;
        } catch (error) {
            console.error('Error deleting from localStorage:', error);
            return false;
        }
    }

    function generateDiagramId(name) {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substring(2, 9);
        const safeName = name.replace(/[^a-zA-Z0-9]/g, '_').substring(0, 20);
        return `${safeName}_${timestamp}_${random}`;
    }

    async function populateDiagramsList() {
        diagramNav.innerHTML = ''; // Clear existing content

        // Load file-based diagrams first
        await loadFileDiagrams();

        // Then load localStorage diagrams
        const diagrams = loadDiagramsFromStorage();
        const diagramIds = Object.keys(diagrams);

        if (diagramIds.length > 0) {
            // Sort by last modified
            diagramIds.sort((a, b) => {
                const dateA = new Date(diagrams[a].lastModified || 0);
                const dateB = new Date(diagrams[b].lastModified || 0);
                return dateB - dateA;
            });

            const details = document.createElement('details');
            details.open = true;
            const summary = document.createElement('summary');
            summary.textContent = 'Мої діаграми';
            details.appendChild(summary);

            const ul = document.createElement('ul');
            diagramIds.forEach(id => {
                const diagram = diagrams[id];
                const li = document.createElement('li');
                li.style.display = 'flex';
                li.style.alignItems = 'center';
                li.style.justifyContent = 'space-between';
                li.style.gap = '8px';

                const a = document.createElement('a');
                a.href = "#";
                a.textContent = diagram.name || 'Unnamed';
                a.dataset.diagramId = id;
                a.style.flex = '1';

                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = '🗑️';
                deleteBtn.title = 'Видалити діаграму';
                deleteBtn.style.background = 'none';
                deleteBtn.style.border = '1px solid var(--border-color)';
                deleteBtn.style.color = 'var(--text-color)';
                deleteBtn.style.cursor = 'pointer';
                deleteBtn.style.padding = '4px 8px';
                deleteBtn.style.borderRadius = '4px';
                deleteBtn.style.fontSize = '12px';
                deleteBtn.style.opacity = '0';
                deleteBtn.style.transition = 'opacity 0.2s';
                deleteBtn.dataset.diagramId = id;

                li.addEventListener('mouseenter', () => {
                    deleteBtn.style.opacity = '1';
                });
                li.addEventListener('mouseleave', () => {
                    deleteBtn.style.opacity = '0';
                });

                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    e.preventDefault();
                    if (confirm(`Видалити діаграму "${diagram.name}"?`)) {
                        deleteDiagramFromStorage(id);
                        populateDiagramsList();

                        // Clear canvas if this was the active diagram
                        const currentDiagram = stateManager.getDiagram();
                        if (currentDiagram && currentDiagram.id === id) {
                            showEmptyState();
                            diagramTitle.textContent = 'DRAKON Viewer';
                            stateManager.loadDiagram(null);
                        }
                    }
                });

                li.appendChild(a);
                li.appendChild(deleteBtn);
                ul.appendChild(li);
            });

            details.appendChild(ul);
            diagramNav.appendChild(details);
        }
    }

    // Load file-based diagrams (from diagrams.json)
    async function loadFileDiagrams() {
        try {
            const response = await fetch('diagrams.json');
            if (!response.ok) {
                console.warn('No diagrams.json found, skipping file-based diagrams');
                return;
            }
            const diagrams = await response.json();

            const steps = diagrams.reduce((acc, diag) => {
                acc[diag.step] = acc[diag.step] || [];
                acc[diag.step].push(diag);
                return acc;
            }, {});

            for (const step in steps) {
                const details = document.createElement('details');
                details.open = true;
                const summary = document.createElement('summary');
                summary.textContent = step;
                details.appendChild(summary);

                const ul = document.createElement('ul');
                steps[step].forEach(diag => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.href = "#";
                    a.textContent = diag.name;
                    a.dataset.path = diag.path;
                    a.dataset.title = `${diag.step} / ${diag.name}`;
                    li.appendChild(a);
                    ul.appendChild(li);
                });
                details.appendChild(ul);
                diagramNav.appendChild(details);
            }
        } catch (error) {
            console.error("Error loading file diagrams:", error);
        }
    }

    // Auto-save current diagram on changes
    stateManager.on('stateChange', () => {
        console.log('💾 stateChange event fired - auto-saving...');

        updateHistoryButtons();
        updateDiagramInfo();

        // Auto-save to localStorage
        const diagram = stateManager.getDiagram();
        if (diagram && diagram.id) {
            console.log('💾 Auto-saving diagram to localStorage:', diagram.id);
            console.log('💾 Total nodes in diagram:', Object.keys(diagram.items || {}).length);
            saveDiagramToStorage(diagram);
        } else {
            console.log('⚠️ Cannot auto-save: no diagram ID');
        }
    });

    // Initialize drakon widget
    function initDrakonWidget() {
        if (!drakonWidget) {
            drakonWidget = createDrakonWidget();
        }
    }

    // Mobile sidebar toggle
    function toggleSidebar() {
        const isOpen = sidebar.classList.toggle('open');
        sidebarBackdrop.classList.toggle('visible', isOpen);
    }

    menuBtn?.addEventListener('click', toggleSidebar);
    sidebarBackdrop?.addEventListener('click', toggleSidebar);

    // Close sidebar when selecting diagram on mobile
    function closeSidebarOnMobile() {
        if (window.innerWidth < 768) {
            sidebar.classList.remove('open');
            sidebarBackdrop.classList.remove('visible');
        }
    }

    // Zoom functions
    function updateZoomLevel(newLevel) {
        zoomLevel = Math.max(0.25, Math.min(3, newLevel));
        zoomLevelDisplay.textContent = Math.round(zoomLevel * 100) + '%';

        if (currentCanvas) {
            currentCanvas.style.transform = `scale(${zoomLevel})`;
            currentCanvas.style.transformOrigin = 'center center';
        }
    }

    function zoomIn() {
        updateZoomLevel(zoomLevel + 0.1);
    }

    function zoomOut() {
        updateZoomLevel(zoomLevel - 0.1);
    }

    function resetZoom() {
        updateZoomLevel(1.0);
        drakonContainer.scrollLeft = 0;
        drakonContainer.scrollTop = 0;
    }

    // Fullscreen toggle
    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            drakonContainer.requestFullscreen().catch(err => {
                console.error('Fullscreen error:', err);
            });
            fullscreenBtn.textContent = '⛶';
        } else {
            document.exitFullscreen();
            fullscreenBtn.textContent = '⛶';
        }
    }

    // Touch and mouse pan/zoom support
    function setupPanZoom() {
        let touchStartDistance = 0;
        let initialZoom = 1.0;

        // Mouse events for panning
        drakonContainer.addEventListener('mousedown', (e) => {
            if (e.target.tagName === 'CANVAS') {
                panState.isPanning = true;
                panState.startX = e.pageX - drakonContainer.offsetLeft;
                panState.startY = e.pageY - drakonContainer.offsetTop;
                panState.scrollLeft = drakonContainer.scrollLeft;
                panState.scrollTop = drakonContainer.scrollTop;
            }
        });

        drakonContainer.addEventListener('mousemove', (e) => {
            if (!panState.isPanning) return;
            e.preventDefault();
            const x = e.pageX - drakonContainer.offsetLeft;
            const y = e.pageY - drakonContainer.offsetTop;
            const walkX = (x - panState.startX) * 1.5;
            const walkY = (y - panState.startY) * 1.5;
            drakonContainer.scrollLeft = panState.scrollLeft - walkX;
            drakonContainer.scrollTop = panState.scrollTop - walkY;
        });

        drakonContainer.addEventListener('mouseup', () => {
            panState.isPanning = false;
        });

        drakonContainer.addEventListener('mouseleave', () => {
            panState.isPanning = false;
        });

        // Mouse wheel zoom
        drakonContainer.addEventListener('wheel', (e) => {
            if (e.ctrlKey || e.metaKey) {
                e.preventDefault();
                const delta = e.deltaY > 0 ? -0.1 : 0.1;
                updateZoomLevel(zoomLevel + delta);
            }
        }, { passive: false });

        // Touch events for pinch-to-zoom
        drakonContainer.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                e.preventDefault();
                const touch1 = e.touches[0];
                const touch2 = e.touches[1];
                touchStartDistance = Math.hypot(
                    touch2.pageX - touch1.pageX,
                    touch2.pageY - touch1.pageY
                );
                initialZoom = zoomLevel;
            } else if (e.touches.length === 1) {
                const touch = e.touches[0];
                panState.isPanning = true;
                panState.startX = touch.pageX;
                panState.startY = touch.pageY;
                panState.scrollLeft = drakonContainer.scrollLeft;
                panState.scrollTop = drakonContainer.scrollTop;
            }
        }, { passive: false });

        drakonContainer.addEventListener('touchmove', (e) => {
            if (e.touches.length === 2) {
                e.preventDefault();
                const touch1 = e.touches[0];
                const touch2 = e.touches[1];
                const touchDistance = Math.hypot(
                    touch2.pageX - touch1.pageX,
                    touch2.pageY - touch1.pageY
                );
                const scale = touchDistance / touchStartDistance;
                updateZoomLevel(initialZoom * scale);
            } else if (e.touches.length === 1 && panState.isPanning) {
                e.preventDefault();
                const touch = e.touches[0];
                const walkX = touch.pageX - panState.startX;
                const walkY = touch.pageY - panState.startY;
                drakonContainer.scrollLeft = panState.scrollLeft - walkX;
                drakonContainer.scrollTop = panState.scrollTop - walkY;
            }
        }, { passive: false });

        drakonContainer.addEventListener('touchend', () => {
            panState.isPanning = false;
            touchStartDistance = 0;
        });
    }

    // Setup toolbar events
    zoomInBtn?.addEventListener('click', zoomIn);
    zoomOutBtn?.addEventListener('click', zoomOut);
    resetZoomBtn?.addEventListener('click', resetZoom);
    fullscreenBtn?.addEventListener('click', toggleFullscreen);
    editModeBtn?.addEventListener('click', toggleEditMode);
    undoBtn?.addEventListener('click', performUndo);
    redoBtn?.addEventListener('click', performRedo);
    saveBtn?.addEventListener('click', saveDiagram);
    newDiagramBtn?.addEventListener('click', createNewDiagram);
    deleteNodeBtn?.addEventListener('click', deleteSelectedNode);

    // Add node buttons
    document.querySelectorAll('#add-node-buttons button[data-type]').forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-type');
            addNode(type);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Zoom shortcuts
        if (e.ctrlKey || e.metaKey) {
            if (e.key === '+' || e.key === '=') {
                e.preventDefault();
                zoomIn();
            } else if (e.key === '-' && !e.shiftKey) {
                e.preventDefault();
                zoomOut();
            } else if (e.key === '0') {
                e.preventDefault();
                resetZoom();
            }
        }

        // Undo/Redo shortcuts (only in edit mode)
        if (stateManager.isEditMode()) {
            if ((e.ctrlKey || e.metaKey) && !e.shiftKey && e.key === 'z') {
                e.preventDefault();
                performUndo();
            } else if ((e.ctrlKey || e.metaKey) && (e.shiftKey && e.key === 'z' || e.key === 'y')) {
                e.preventDefault();
                performRedo();
            } else if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                saveDiagram();
            } else if (e.key === 'Delete' && stateManager.getSelectedItem()) {
                e.preventDefault();
                deleteSelectedNode();
            }
        }

        // New diagram shortcut
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            createNewDiagram();
        }
    });

    // Modal functions
    function openEditModal(itemId, item) {
        currentEditingItemId = itemId;
        editContentInput.value = item.content || '';
        editTypeSelect.value = item.type || 'action';
        editModal.classList.add('active');
        editContentInput.focus();
    }

    function closeEditModal() {
        editModal.classList.remove('active');
        currentEditingItemId = null;
        editContentInput.value = '';
    }

    function saveEditModal() {
        if (!currentEditingItemId) return;

        const newContent = editContentInput.value;
        const newType = editTypeSelect.value;

        // Update item via state manager
        stateManager.updateItem(currentEditingItemId, {
            content: newContent,
            type: newType
        });

        // Reload diagram
        reloadCurrentDiagram();

        closeEditModal();
    }

    // Modal event listeners
    modalClose?.addEventListener('click', closeEditModal);
    modalCancel?.addEventListener('click', closeEditModal);
    modalSave?.addEventListener('click', saveEditModal);

    // Close modal on backdrop click
    editModal?.addEventListener('click', (e) => {
        if (e.target === editModal) {
            closeEditModal();
        }
    });

    // Close modal on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && editModal.classList.contains('active')) {
            closeEditModal();
        }
    });

    // Build config for drakon viewer
    function buildConfig() {
        const isEditMode = stateManager.isEditMode();

        return {
            theme: {
                background: '#ffffff',
                color: '#000000',
                lineColor: '#000000',
                font: '16px Arial, sans-serif'
            },
            showContextMenu: function() {
                // Context menu for edit mode could be added here
                if (isEditMode) {
                    console.log('Context menu in edit mode');
                }
            },
            startEditContent: function(item) {
                if (!isEditMode) {
                    console.log('Edit blocked (read-only mode)');
                    return;
                }

                console.log('Editing item:', item);
                openEditModal(item.id, item);
            },
            onItemClick: function(item) {
                console.log('Item clicked:', item);
                stateManager.selectItem(item.id);
            },
            drawZones: false,
            canSelect: true,
            canvasIcons: false,
            centerContent: true,
            textFormat: 'plain'
        };
    }

    // Create edit sender (required for setDiagram)
    // Delegates all edit operations to stateManager
    function createEditSender() {
        return {
            stop: function() {
                console.log('🛑 EditSender.stop() called');
            },
            pushEdit: function(edit) {
                console.log('📝 EditSender.pushEdit() called');
                console.log('📝 Edit mode:', stateManager.isEditMode());
                console.log('📝 Edit data:', JSON.stringify(edit, null, 2));

                if (!stateManager.isEditMode()) {
                    console.warn('❌ Edit blocked (read-only mode)');
                    return Promise.resolve();
                }

                // Get current diagram reference that drakonWidget is using
                const diagram = stateManager.getDiagram();
                if (!diagram || !diagram.items) {
                    console.error('❌ No diagram available for edit');
                    return Promise.reject(new Error('No diagram available'));
                }

                console.log('📝 Current diagram nodes BEFORE edit:', Object.keys(diagram.items).length);

                // Apply changes directly to the diagram that drakonWidget is using
                try {
                    if (edit.changes && Array.isArray(edit.changes)) {
                        for (const change of edit.changes) {
                            console.log(`📝 Processing change: ${change.op} on node ${change.id || 'new'}`);

                            switch (change.op) {
                                case 'insert': {
                                    const id = change.id || stateManager.generateItemId(diagram);
                                    diagram.items[id] = change.fields;
                                    console.log(`✅ Inserted node ${id}:`, change.fields);
                                    break;
                                }
                                case 'update': {
                                    if (diagram.items[change.id]) {
                                        Object.assign(diagram.items[change.id], change.fields);
                                        console.log(`✅ Updated node ${change.id}:`, change.fields);
                                    } else {
                                        console.warn(`⚠️ Cannot update - node ${change.id} not found`);
                                    }
                                    break;
                                }
                                case 'delete': {
                                    delete diagram.items[change.id];
                                    console.log(`✅ Deleted node ${change.id}`);
                                    break;
                                }
                                default:
                                    console.warn('⚠️ Unknown operation:', change.op);
                            }
                        }
                    }

                    console.log('📝 Current diagram nodes AFTER edit:', Object.keys(diagram.items).length);
                    console.log('📝 All node IDs:', Object.keys(diagram.items).join(', '));

                    // Save to history through stateManager
                    console.log('💾 Calling stateManager.updateDiagram() to save to history...');
                    stateManager.updateDiagram(diagram, true);

                    console.log('✅ Edit applied successfully, diagram saved to history');
                    return Promise.resolve();
                } catch (err) {
                    console.error('❌ Error applying edit:', err);
                    return Promise.reject(err);
                }
            }
        };
    }

    // Edit mode toggle
    function toggleEditMode() {
        const newMode = !stateManager.isEditMode();
        stateManager.setEditMode(newMode);

        if (newMode) {
            editModeBtn.textContent = '👁️ Перегляд';
            editModeBtn.title = 'Вимкнути режим редагування';
            editModeIndicator.style.display = 'inline';
            saveBtn.style.display = 'inline-block';
            addNodeButtons.style.display = 'flex';
            addNodeButtons.style.alignItems = 'center';
            addNodeButtons.style.gap = '4px';
        } else {
            editModeBtn.textContent = '✏️ Редагувати';
            editModeBtn.title = 'Увімкнути режим редагування';
            editModeIndicator.style.display = 'none';
            addNodeButtons.style.display = 'none';

            if (!stateManager.hasUnsavedChanges()) {
                saveBtn.style.display = 'none';
            }
        }

        // Reload diagram with new mode
        if (stateManager.getDiagram()) {
            reloadCurrentDiagram();
        }
    }

    // Create new diagram
    function createNewDiagram() {
        const diagramName = prompt('Назва нової діаграми:', 'New Diagram');
        if (!diagramName) return;

        const newDiagram = {
            name: diagramName,
            access: 'write',
            params: [],
            items: {
                '1': {
                    id: '1',
                    type: 'header',
                    content: diagramName,
                    branchId: 1,
                    one: '2'
                },
                '2': {
                    id: '2',
                    type: 'end',
                    content: '',
                    branchId: 1
                }
            }
        };

        // Generate ID and save to storage
        const diagramId = saveDiagramToStorage(newDiagram);
        if (diagramId) {
            newDiagram.id = diagramId;
        }

        diagramTitle.textContent = diagramName;
        stateManager.loadDiagram(newDiagram);
        stateManager.setEditMode(true);

        // Update UI
        editModeBtn.textContent = '👁️ Перегляд';
        editModeIndicator.style.display = 'inline';
        saveBtn.style.display = 'inline-block';
        addNodeButtons.style.display = 'flex';

        // Initialize widget if needed
        initDrakonWidget();

        // Render
        reloadCurrentDiagram();
        resetZoom();

        // Refresh sidebar list
        populateDiagramsList();

        // Close sidebar on mobile
        closeSidebarOnMobile();
    }

    // ==================== NODE INSERTION ====================
    // Uses native drakonWidget.showInsertionSockets() API
    //
    // Add new node using DrakonWidget's built-in insertion socket system
    function addNode(type) {
        if (!stateManager.isEditMode()) {
            alert('Увімкніть режим редагування для додавання вузлів');
            return;
        }

        const diagram = stateManager.getDiagram();
        if (!diagram || !diagram.items) {
            alert('Спочатку відкрийте або створіть діаграму');
            return;
        }

        // Check if drakonWidget is available
        if (!drakonWidget) {
            console.error('DrakonWidget not initialized');
            return;
        }

        // Use DrakonWidget's built-in showInsertionSockets method
        // This will display visual '+' markers on all edges where the node can be inserted
        // imageData can be null for standard nodes
        drakonWidget.showInsertionSockets(type, null);
    }

    // Delete selected node
    function deleteSelectedNode() {
        const selectedId = stateManager.getSelectedItem();
        if (!selectedId) {
            alert('Виберіть вузол для видалення');
            return;
        }

        if (confirm('Ви впевнені, що хочете видалити цей вузол?')) {
            stateManager.deleteItem(selectedId);
            reloadCurrentDiagram();
        }
    }

    // Undo/Redo functions
    function performUndo() {
        if (stateManager.undo()) {
            reloadCurrentDiagram();
        }
    }

    function performRedo() {
        if (stateManager.redo()) {
            reloadCurrentDiagram();
        }
    }

    // Update undo/redo button states
    function updateHistoryButtons() {
        const historyInfo = stateManager.getHistoryInfo();
        undoBtn.disabled = !historyInfo.canUndo;
        redoBtn.disabled = !historyInfo.canRedo;

        // Update unsaved changes indicator
        if (stateManager.hasUnsavedChanges()) {
            unsavedIndicator.style.display = 'inline';
            saveBtn.disabled = false;
        } else {
            unsavedIndicator.style.display = 'none';
            saveBtn.disabled = true;
        }
    }

    // Reload current diagram from state manager
    function reloadCurrentDiagram() {
        // IMPORTANT: Use getDiagram() not getDiagramCopy()
        // We need to pass the same reference that editSender will mutate
        const diagram = stateManager.getDiagram();
        if (!diagram) {
            console.warn('⚠️ reloadCurrentDiagram: No diagram to reload');
            return;
        }

        console.log('🔄 Reloading diagram:', diagram.name);
        console.log('🔄 Total nodes:', Object.keys(diagram.items || {}).length);
        console.log('🔄 Node IDs:', Object.keys(diagram.items || {}).join(', '));
        console.log('🔄 Edit mode:', stateManager.isEditMode());

        // Set access mode based on edit mode
        diagram.access = stateManager.isEditMode() ? 'write' : 'read';

        renderDrakonWidget();

        const sender = createEditSender();
        drakonWidget.setDiagram(
            diagram.name || 'diagram',
            diagram,
            sender
        );

        // Force redraw to ensure diagram appears
        console.log('🔄 Calling redraw()...');
        drakonWidget.redraw();
        console.log('✅ Diagram reloaded successfully');
    }

    // Save diagram changes
    async function saveDiagram() {
        const diagram = stateManager.getDiagram(); // Use getDiagram() to get current state with all changes
        if (!diagram) {
            alert('Немає діаграми для збереження');
            return;
        }

        console.log('💾 Saving diagram:', diagram.name);
        console.log('💾 Total nodes:', Object.keys(diagram.items || {}).length);
        console.log('💾 Diagram data:', JSON.stringify(diagram, null, 2));

        try {
            // Export as JSON file (for both localStorage and file-based diagrams)
            const exportData = {
                name: diagram.name,
                access: diagram.access || 'write',
                params: diagram.params || [],
                items: diagram.items || {}
            };

            const json = JSON.stringify(exportData, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = (diagram.name || 'diagram').replace(/[^a-zA-Z0-9]/g, '_') + '.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            // Also save to localStorage if it has an ID
            if (diagram.id) {
                saveDiagramToStorage(diagram);
            }

            stateManager.markAsSaved();
            updateHistoryButtons();
            alert('Діаграму збережено! (завантажено як файл)');
        } catch (error) {
            console.error('Error saving diagram:', error);
            alert('Помилка збереження діаграми: ' + error.message);
        }
    }

    // State manager event listeners (stateChange already handled above with auto-save)
    stateManager.on('historyChange', () => {
        updateHistoryButtons();
    });

    stateManager.on('selectionChange', () => {
        updatePropertiesPanel();
    });

    stateManager.on('modeChange', () => {
        updateDiagramInfo();
    });

    // Update diagram info
    function updateDiagramInfo() {
        const diagram = stateManager.getDiagram();
        if (diagram) {
            infoName.textContent = diagram.name || 'Unnamed';
            const itemCount = diagram.items ? Object.keys(diagram.items).length : 0;
            infoNodes.textContent = itemCount;
        } else {
            infoName.textContent = '-';
            infoNodes.textContent = '0';
        }

        infoMode.textContent = stateManager.isEditMode() ? 'Редагування' : 'Перегляд';
    }

    // Update properties panel for selected node
    function updatePropertiesPanel() {
        const selectedId = stateManager.getSelectedItem();
        const selectedData = stateManager.getSelectedItemData();

        if (selectedId && selectedData) {
            nodePropertiesSection.style.display = 'block';
            propId.value = selectedId;
            propType.value = selectedData.type || 'action';
            propContent.value = selectedData.content || '';
            propBranch.value = selectedData.branchId || 1;
        } else {
            nodePropertiesSection.style.display = 'none';
        }
    }

    // Apply properties changes
    function applyPropertiesChanges() {
        const selectedId = stateManager.getSelectedItem();
        if (!selectedId) return;

        stateManager.updateItem(selectedId, {
            type: propType.value,
            content: propContent.value,
            branchId: parseInt(propBranch.value)
        });

        reloadCurrentDiagram();
    }

    // Properties panel toggle
    function togglePropertiesPanel() {
        const isCollapsed = propertiesPanel.classList.toggle('collapsed');

        // Show/hide floating button based on panel state
        if (floatingPanelBtn) {
            floatingPanelBtn.style.display = isCollapsed ? 'flex' : 'none';
        }
    }

    // Restore panel (from floating button)
    function restorePropertiesPanel() {
        propertiesPanel.classList.remove('collapsed');
        if (floatingPanelBtn) {
            floatingPanelBtn.style.display = 'none';
        }
    }

    // File operations
    function openFile() {
        fileInput.click();
    }

    function handleFileOpen(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const diagramData = JSON.parse(e.target.result);
                diagramData.path = file.name;

                // Save to localStorage
                const diagramId = saveDiagramToStorage(diagramData);
                if (diagramId) {
                    diagramData.id = diagramId;
                }

                diagramTitle.textContent = diagramData.name || file.name;
                stateManager.loadDiagram(diagramData);

                initDrakonWidget();
                reloadCurrentDiagram();
                resetZoom();
                updateHistoryButtons();

                // Refresh sidebar list
                populateDiagramsList();

                closeSidebarOnMobile();
            } catch (error) {
                alert('Помилка відкриття файлу: ' + error.message);
                console.error('Error opening file:', error);
            }
        };
        reader.readAsText(file);

        // Reset input
        fileInput.value = '';
    }

    function exportDiagramAsJson() {
        const diagram = stateManager.getDiagramCopy();
        if (!diagram) {
            alert('Немає діаграми для експорту');
            return;
        }

        const json = JSON.stringify(diagram, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = (diagram.name || 'diagram') + '.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function exportDiagramAsPng() {
        const diagram = stateManager.getDiagramCopy();
        if (!diagram) {
            alert('Немає діаграми для експорту');
            return;
        }

        if (!currentCanvas) {
            alert('Canvas не знайдено. Спочатку відкрийте діаграму.');
            return;
        }

        try {
            // Convert canvas to PNG data URL
            const dataURL = currentCanvas.toDataURL('image/png');

            // Create download link
            const a = document.createElement('a');
            a.href = dataURL;
            a.download = (diagram.name || 'diagram') + '.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            console.log('PNG exported successfully');
        } catch (error) {
            console.error('Error exporting PNG:', error);
            alert('Помилка експорту PNG: ' + error.message);
        }
    }

    // Icon palette click handlers
    document.querySelectorAll('.icon-item').forEach(item => {
        item.addEventListener('click', () => {
            const type = item.getAttribute('data-type');
            addNode(type);
        });
    });

    // Properties panel event listeners
    panelToggle?.addEventListener('click', togglePropertiesPanel);
    floatingPanelBtn?.addEventListener('click', restorePropertiesPanel);
    panelNewBtn?.addEventListener('click', createNewDiagram);
    panelOpenBtn?.addEventListener('click', openFile);
    panelSaveBtn?.addEventListener('click', saveDiagram);
    panelExportJsonBtn?.addEventListener('click', exportDiagramAsJson);
    panelExportPngBtn?.addEventListener('click', exportDiagramAsPng);
    fileInput?.addEventListener('change', handleFileOpen);
    propApply?.addEventListener('click', applyPropertiesChanges);
    propDelete?.addEventListener('click', deleteSelectedNode);

    // Enable PNG export button
    if (panelExportPngBtn) {
        panelExportPngBtn.disabled = false;
        panelExportPngBtn.title = 'Експортувати діаграму як PNG зображення';
    }

    // Render drakon widget
    function renderDrakonWidget() {
        const rect = drakonContainer.getBoundingClientRect();
        drakonContainer.innerHTML = '';

        const config = buildConfig();

        // Create canvas with extra space for zooming (3x size to accommodate 3x zoom)
        // This prevents diagram from being cut off when zoomed in
        const canvasWidth = (rect.width || 800) * 3;
        const canvasHeight = (rect.height || 600) * 3;

        console.log('🎨 Rendering canvas:', canvasWidth, 'x', canvasHeight);

        currentCanvas = drakonWidget.render(
            canvasWidth,
            canvasHeight,
            config
        );

        // Apply initial zoom transform
        if (currentCanvas) {
            currentCanvas.style.transform = `scale(${zoomLevel})`;
            currentCanvas.style.transformOrigin = 'center center';
        }

        drakonContainer.appendChild(currentCanvas);
    }

    // Load and display diagram
    async function loadDiagram(path, title) {
        try {
            // Show loading state with timeout
            showLoading('Завантаження діаграми...');

            const response = await fetch(path);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const diagramData = await response.json();

            // Store path for saving
            diagramData.path = path;

            diagramTitle.textContent = title;

            // Load into state manager
            stateManager.loadDiagram(diagramData);

            // Initialize widget if needed
            initDrakonWidget();

            // Render widget
            renderDrakonWidget();

            // Set diagram access mode based on edit mode
            diagramData.access = stateManager.isEditMode() ? 'write' : 'read';
            const sender = createEditSender();

            drakonWidget.setDiagram(
                diagramData.name || 'diagram',
                diagramData,
                sender
            );

            // Hide loading state
            hideLoading();

            // Reset zoom after loading new diagram
            resetZoom();

            // Update UI
            updateHistoryButtons();

            // Close sidebar on mobile
            closeSidebarOnMobile();

        } catch (error) {
            showError(`Помилка завантаження діаграми: ${error.message}`);
            console.error("Error loading diagram:", error);
        }
    }


    // Handle diagram selection
    diagramNav.addEventListener('click', async (e) => {
        e.preventDefault();
        if (e.target.tagName === 'A') {
            const diagramId = e.target.dataset.diagramId;

            if (diagramId) {
                // Load from localStorage
                const diagramData = getDiagramFromStorage(diagramId);
                if (diagramData) {
                    // Remove active class from previously selected item
                    const currentActive = diagramNav.querySelector('.active');
                    if (currentActive) {
                        currentActive.classList.remove('active');
                    }
                    // Add active class to current item
                    e.target.classList.add('active');

                    diagramTitle.textContent = diagramData.name || 'Unnamed';
                    stateManager.loadDiagram(diagramData);

                    initDrakonWidget();
                    reloadCurrentDiagram();
                    resetZoom();
                    updateHistoryButtons();

                    closeSidebarOnMobile();
                } else {
                    alert('Діаграму не знайдено');
                }
            } else {
                // Fallback to old path-based loading for compatibility
                const path = e.target.dataset.path;
                const title = e.target.dataset.title;
                if (path) {
                    // Remove active class from previously selected item
                    const currentActive = diagramNav.querySelector('.active');
                    if (currentActive) {
                        currentActive.classList.remove('active');
                    }
                    // Add active class to current item
                    e.target.classList.add('active');

                    await loadDiagram(path, title);
                }
            }
        }
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        if (drakonWidget && currentCanvas) {
            renderDrakonWidget();
            drakonWidget.redraw();
        }
    });

    // Swipe gestures for sidebar on mobile
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeThreshold = 50;
        const swipeDistance = touchEndX - touchStartX;

        if (window.innerWidth < 768) {
            // Swipe right to open sidebar
            if (swipeDistance > swipeThreshold && touchStartX < 50) {
                sidebar.classList.add('open');
                sidebarBackdrop.classList.add('visible');
            }
            // Swipe left to close sidebar
            if (swipeDistance < -swipeThreshold && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                sidebarBackdrop.classList.remove('visible');
            }
        }
    }

    // ==================== TESTING API ====================
    // Expose functions for automated testing
    window.DrakonTestAPI = {
        createDiagram: (name) => {
            // Ensure name is a string
            const diagramName = String(name || 'Test Diagram');

            const newDiagram = {
                name: diagramName,
                access: 'write',
                params: [],
                items: {
                    '1': {
                        id: '1',
                        type: 'header',
                        content: String(diagramName),
                        branchId: 1,
                        one: '2'
                    },
                    '2': {
                        id: '2',
                        type: 'end',
                        content: '',
                        branchId: 1
                    }
                }
            };

            const diagramId = saveDiagramToStorage(newDiagram);
            if (diagramId) {
                newDiagram.id = diagramId;
            }

            diagramTitle.textContent = diagramName;
            stateManager.loadDiagram(newDiagram);
            stateManager.setEditMode(true);

            editModeBtn.textContent = '👁️ Перегляд';
            editModeIndicator.style.display = 'inline';
            saveBtn.style.display = 'inline-block';
            addNodeButtons.style.display = 'flex';

            initDrakonWidget();
            reloadCurrentDiagram();
            resetZoom();
            populateDiagramsList();

            return newDiagram;
        },

        enableEditMode: () => {
            if (!stateManager.isEditMode()) {
                toggleEditMode();
            }
        },

        disableEditMode: () => {
            if (stateManager.isEditMode()) {
                toggleEditMode();
            }
        },

        addNode: (type) => {
            return addNode(type);
        },

        getDiagram: () => {
            return stateManager.getDiagram();
        },

        saveDiagram: () => {
            return saveDiagram();
        },

        getNodeCount: () => {
            const diagram = stateManager.getDiagram();
            return diagram && diagram.items ? Object.keys(diagram.items).length : 0;
        },

        isEditMode: () => {
            return stateManager.isEditMode();
        }
    };

    // Initialize all features
    setupPanZoom();
    populateDiagramsList();

    // Show empty state initially
    showEmptyState();
});
