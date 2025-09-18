document.addEventListener('DOMContentLoaded', () => {
    const categoryList = document.querySelector('.category-list');
    let draggedItem = null;

    if (categoryList) {
        categoryList.addEventListener('dragstart', e => {
            draggedItem = e.target;
            setTimeout(() => {
                e.target.classList.add('dragging');
            }, 0);
        });

        categoryList.addEventListener('dragend', e => {
            setTimeout(() => {
                draggedItem.classList.remove('dragging');
                draggedItem = null;
            }, 0);
        });

        categoryList.addEventListener('dragover', e => {
            e.preventDefault();
            const afterElement = getDragAfterElement(categoryList, e.clientY);
            const draggable = document.querySelector('.dragging');
            if (afterElement == null) {
                categoryList.appendChild(draggable);
            } else {
                categoryList.insertBefore(draggable, afterElement);
            }
        });

        categoryList.addEventListener('drop', e => {
            e.preventDefault();
            const newOrder = [];
            categoryList.querySelectorAll('li').forEach(li => {
                newOrder.push(li.dataset.category);
            });

            fetch('/reorder_categories', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ newOrder: newOrder })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    // Optionally, refresh or give feedback
                }
            });
        });
    }

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('li:not(.dragging)')];

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }
});
