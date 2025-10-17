document.addEventListener('DOMContentLoaded', () => {
    const diagramNav = document.getElementById('diagram-nav');
    const drakonContainer = document.getElementById('drakon-container');
    const diagramTitle = document.getElementById('diagram-title');
    let drakonWidget = null;
    let currentCanvas = null;

    // Initialize drakon widget
    function initDrakonWidget() {
        if (!drakonWidget) {
            drakonWidget = createDrakonWidget();
        }
    }

    // Build minimal config for read-only viewer
    function buildConfig() {
        return {
            theme: {
                background: '#ffffff',
                color: '#000000',
                lineColor: '#000000',
                font: '16px Arial, sans-serif'
            },
            showContextMenu: function() {
                // No context menu in read-only mode
            },
            startEditContent: function() {
                // No editing in read-only mode
            },
            onItemClick: function(item) {
                console.log('Item clicked:', item);
            },
            drawZones: false,
            canSelect: true,
            canvasIcons: false,
            centerContent: true,
            textFormat: 'plain'
        };
    }

    // Create edit sender (required for setDiagram)
    function createEditSender() {
        return {
            stop: function() {},
            pushEdit: function(edit) {
                console.log('Edit blocked (read-only mode):', edit);
            }
        };
    }

    // Render drakon widget
    function renderDrakonWidget() {
        const rect = drakonContainer.getBoundingClientRect();
        drakonContainer.innerHTML = '';

        const config = buildConfig();
        currentCanvas = drakonWidget.render(
            rect.width || 800,
            rect.height || 600,
            config
        );

        drakonContainer.appendChild(currentCanvas);
    }

    // Load and display diagram
    async function loadDiagram(path, title) {
        try {
            const response = await fetch(path);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const diagramData = await response.json();

            diagramTitle.textContent = title;

            // Initialize widget if needed
            initDrakonWidget();

            // Render widget
            renderDrakonWidget();

            // Set diagram as read-only
            diagramData.access = 'read';
            const sender = createEditSender();

            drakonWidget.setDiagram(
                diagramData.name || 'diagram',
                diagramData,
                sender
            );

        } catch (error) {
            drakonContainer.innerHTML = `<p class="error">Помилка завантаження діаграми: ${error.message}</p>`;
            console.error("Error loading diagram:", error);
        }
    }

    // Load diagrams list
    async function loadDiagrams() {
        try {
            const response = await fetch('/diagrams.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const diagrams = await response.json();

            const steps = diagrams.reduce((acc, diag) => {
                acc[diag.step] = acc[diag.step] || [];
                acc[diag.step].push(diag);
                return acc;
            }, {});

            diagramNav.innerHTML = '';
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
            diagramNav.innerHTML = '<p class="error">Не вдалося завантажити індекс діаграм. Переконайтеся, що файл diagrams.json існує.</p>';
            console.error("Error loading diagrams:", error);
        }
    }

    // Handle diagram selection
    diagramNav.addEventListener('click', async (e) => {
        e.preventDefault();
        if (e.target.tagName === 'A') {
            const path = e.target.dataset.path;
            const title = e.target.dataset.title;

            // Remove active class from previously selected item
            const currentActive = diagramNav.querySelector('.active');
            if (currentActive) {
                currentActive.classList.remove('active');
            }
            // Add active class to current item
            e.target.classList.add('active');

            await loadDiagram(path, title);
        }
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        if (drakonWidget && currentCanvas) {
            renderDrakonWidget();
            drakonWidget.redraw();
        }
    });

    // Initialize
    loadDiagrams();
});
