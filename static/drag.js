document.addEventListener('DOMContentLoaded', () => {
    const taskLists = document.querySelectorAll('.task-list');

    taskLists.forEach(taskList => {
        const person = taskList.dataset.person;
        let draggedItem = null;

        taskList.addEventListener('dragstart', e => {
            draggedItem = e.target;
            setTimeout(() => {
                e.target.classList.add('dragging');
            }, 0);
        });

        taskList.addEventListener('dragend', e => {
            setTimeout(() => {
                draggedItem.classList.remove('dragging');
                draggedItem = null;
            }, 0);
        });

        taskList.addEventListener('dragover', e => {
            e.preventDefault();
            const afterElement = getDragAfterElement(taskList, e.clientY);
            const draggable = document.querySelector('.dragging');
            if (afterElement == null) {
                taskList.appendChild(draggable);
            } else {
                taskList.insertBefore(draggable, afterElement);
            }
        });

        taskList.addEventListener('drop', e => {
            e.preventDefault();
            const newOrder = [];
            taskList.querySelectorAll('li').forEach((li, index) => {
                newOrder.push(li.dataset.taskId);
            });

            const category = window.location.pathname.split('/').pop();

            fetch(`/tasks/${category}/reorder`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    person: person,
                    newOrder: newOrder
                })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    // Optionally, refresh or give feedback
                }
            });
        });
    });

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
