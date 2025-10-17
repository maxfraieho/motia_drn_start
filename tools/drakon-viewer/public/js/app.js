document.addEventListener('DOMContentLoaded', () => {
    const diagramNav = document.getElementById('diagram-nav');
    const drakonContainer = document.getElementById('drakon-container');
    const diagramTitle = document.getElementById('diagram-title');
    let drakonEditor;

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

            try {
                const response = await fetch(path);
                 if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const diagramData = await response.json();

                diagramTitle.textContent = title;
                drakonContainer.innerHTML = ''; // Clear previous diagram

                if (drakonEditor) {
                    drakonEditor.destroy();
                }
                drakonEditor = Drakon.Editor.create(drakonContainer, diagramData);

            } catch (error) {
                drakonContainer.innerHTML = `<p class="error">Помилка завантаження діаграми: ${error.message}</p>`;
                console.error("Error loading diagram:", error);
            }
        }
    });

    loadDiagrams();
});
