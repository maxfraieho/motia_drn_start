// ⚙️ Refactored for native drakonWidget API integration
// Added applyExternalEdit() to handle official drakonwidget edits

/**
 * State Manager for DRAKON Editor
 * Manages diagram state, history, and edit mode
 */

class DiagramStateManager {
    constructor() {
        this.currentDiagram = null;
        this.history = [];
        this.historyIndex = -1;
        this.maxHistorySize = 50;
        this.editMode = false;
        this.isDirty = false; // Track unsaved changes
        this.selectedItem = null;
        this.listeners = {
            stateChange: [],
            modeChange: [],
            selectionChange: [],
            historyChange: []
        };
    }

    /**
     * Load a diagram into the editor
     */
    loadDiagram(diagram) {
        this.currentDiagram = this.deepClone(diagram);
        this.history = [this.deepClone(diagram)];
        this.historyIndex = 0;
        this.isDirty = false;
        this.selectedItem = null;
        this.notifyListeners('stateChange');
        this.notifyListeners('historyChange');
        this.notifyListeners('selectionChange');
    }

    /**
     * Get current diagram
     */
    getDiagram() {
        return this.currentDiagram;
    }

    /**
     * Get current diagram as copy (to prevent external mutations)
     */
    getDiagramCopy() {
        return this.deepClone(this.currentDiagram);
    }

    /**
     * Update diagram and save to history
     */
    updateDiagram(newDiagram, saveToHistory = true) {
        this.currentDiagram = this.deepClone(newDiagram);
        this.isDirty = true;

        if (saveToHistory) {
            // Remove any history after current index (for redo)
            this.history = this.history.slice(0, this.historyIndex + 1);

            // Add new state to history
            this.history.push(this.deepClone(newDiagram));

            // Limit history size
            if (this.history.length > this.maxHistorySize) {
                this.history.shift();
            } else {
                this.historyIndex++;
            }

            this.notifyListeners('historyChange');
        }

        this.notifyListeners('stateChange');
    }

    /**
     * Update specific item in diagram
     */
    updateItem(itemId, updates) {
        if (!this.currentDiagram || !this.currentDiagram.items || !this.currentDiagram.items[itemId]) {
            console.warn('Item not found:', itemId);
            return false;
        }

        const newDiagram = this.deepClone(this.currentDiagram);
        Object.assign(newDiagram.items[itemId], updates);
        this.updateDiagram(newDiagram, true);
        return true;
    }

    /**
     * Add new item to diagram
     */
    addItem(item) {
        if (!this.currentDiagram || !this.currentDiagram.items) {
            console.warn('Cannot add item: no diagram loaded');
            return null;
        }

        const newDiagram = this.deepClone(this.currentDiagram);
        const newId = this.generateItemId(newDiagram);

        // Set default properties
        const newItem = {
            id: newId,
            type: item.type || 'action',
            content: item.content || '',
            branchId: item.branchId || 1,
            ...item
        };

        newDiagram.items[newId] = newItem;
        this.updateDiagram(newDiagram, true);
        return newId;
    }

    /**
     * Delete item from diagram
     */
    deleteItem(itemId) {
        if (!this.currentDiagram || !this.currentDiagram.items || !this.currentDiagram.items[itemId]) {
            console.warn('Item not found:', itemId);
            return false;
        }

        const newDiagram = this.deepClone(this.currentDiagram);
        delete newDiagram.items[itemId];

        // Remove references to deleted item
        Object.values(newDiagram.items).forEach(item => {
            if (item.one === itemId) delete item.one;
            if (item.yes === itemId) delete item.yes;
            if (item.no === itemId) delete item.no;
        });

        this.updateDiagram(newDiagram, true);

        if (this.selectedItem === itemId) {
            this.selectItem(null);
        }

        return true;
    }

    /**
     * Apply external edits received from drakonWidget.editSender
     * Supports operations: insert, update, delete
     */
    applyExternalEdit(edit) {
        return new Promise((resolve, reject) => {
            try {
                const diagram = this.getDiagramCopy();

                if (!edit.changes || !Array.isArray(edit.changes)) {
                    console.warn('Invalid edit format: missing changes array');
                    return resolve();
                }

                for (const change of edit.changes) {
                    switch (change.op) {
                        case 'insert': {
                            const id = change.id || this.generateItemId(diagram);
                            diagram.items[id] = change.fields;
                            break;
                        }
                        case 'update': {
                            const id = change.id;
                            if (diagram.items[id]) {
                                diagram.items[id] = {
                                    ...diagram.items[id],
                                    ...(change.fields || {})
                                };
                            }
                            break;
                        }
                        case 'delete': {
                            delete diagram.items[change.id];
                            break;
                        }
                        default:
                            console.warn('Unknown operation:', change.op);
                    }
                }

                this.updateDiagram(diagram, true);
                resolve();
            } catch (err) {
                console.error('applyExternalEdit error:', err);
                reject(err);
            }
        });
    }

    /**
     * Undo last change
     */
    undo() {
        if (!this.canUndo()) {
            console.warn('Cannot undo: at beginning of history');
            return false;
        }

        this.historyIndex--;
        this.currentDiagram = this.deepClone(this.history[this.historyIndex]);
        this.isDirty = true;
        this.notifyListeners('stateChange');
        this.notifyListeners('historyChange');
        return true;
    }

    /**
     * Redo last undone change
     */
    redo() {
        if (!this.canRedo()) {
            console.warn('Cannot redo: at end of history');
            return false;
        }

        this.historyIndex++;
        this.currentDiagram = this.deepClone(this.history[this.historyIndex]);
        this.isDirty = true;
        this.notifyListeners('stateChange');
        this.notifyListeners('historyChange');
        return true;
    }

    /**
     * Check if undo is available
     */
    canUndo() {
        return this.historyIndex > 0;
    }

    /**
     * Check if redo is available
     */
    canRedo() {
        return this.historyIndex < this.history.length - 1;
    }

    /**
     * Toggle edit mode
     */
    setEditMode(enabled) {
        if (this.editMode !== enabled) {
            this.editMode = enabled;
            this.notifyListeners('modeChange');
        }
    }

    /**
     * Check if in edit mode
     */
    isEditMode() {
        return this.editMode;
    }

    /**
     * Select an item
     */
    selectItem(itemId) {
        if (this.selectedItem !== itemId) {
            this.selectedItem = itemId;
            this.notifyListeners('selectionChange');
        }
    }

    /**
     * Get selected item
     */
    getSelectedItem() {
        return this.selectedItem;
    }

    /**
     * Get selected item data
     */
    getSelectedItemData() {
        if (!this.selectedItem || !this.currentDiagram || !this.currentDiagram.items) {
            return null;
        }
        return this.currentDiagram.items[this.selectedItem];
    }

    /**
     * Mark as saved
     */
    markAsSaved() {
        this.isDirty = false;
    }

    /**
     * Check if has unsaved changes
     */
    hasUnsavedChanges() {
        return this.isDirty;
    }

    /**
     * Register event listener
     */
    on(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event].push(callback);
        }
    }

    /**
     * Unregister event listener
     */
    off(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }
    }

    /**
     * Notify all listeners for an event
     */
    notifyListeners(event) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => {
                try {
                    callback(this);
                } catch (error) {
                    console.error('Error in listener:', error);
                }
            });
        }
    }

    /**
     * Generate unique item ID
     */
    generateItemId(diagram) {
        const existingIds = Object.keys(diagram.items).map(id => parseInt(id)).filter(n => !isNaN(n));
        const maxId = existingIds.length > 0 ? Math.max(...existingIds) : 0;
        return String(maxId + 1);
    }

    /**
     * Deep clone object
     */
    deepClone(obj) {
        if (obj === null || typeof obj !== 'object') {
            return obj;
        }

        if (obj instanceof Date) {
            return new Date(obj.getTime());
        }

        if (obj instanceof Array) {
            return obj.map(item => this.deepClone(item));
        }

        const cloned = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                cloned[key] = this.deepClone(obj[key]);
            }
        }
        return cloned;
    }

    /**
     * Get history info for UI
     */
    getHistoryInfo() {
        return {
            canUndo: this.canUndo(),
            canRedo: this.canRedo(),
            currentIndex: this.historyIndex,
            totalStates: this.history.length
        };
    }

    /**
     * Clear all state
     */
    clear() {
        this.currentDiagram = null;
        this.history = [];
        this.historyIndex = -1;
        this.isDirty = false;
        this.selectedItem = null;
        this.editMode = false;
    }
}

// Export for use in other scripts
window.DiagramStateManager = DiagramStateManager;
