document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');

    let draggedCard = null;

    cards.forEach(card => {
        card.addEventListener('dragstart', dragStart);
        card.addEventListener('dragend', dragEnd);
    });

    function dragStart() {
        draggedCard = this;
        setTimeout(() => {
            this.style.display = 'none';
        }, 0);
    }

    function dragEnd() {
        draggedCard = null;
        setTimeout(() => {
            this.style.display = '';
        }, 0);
    }

    const columns = document.querySelectorAll('.status-column');

    columns.forEach(column => {
        column.addEventListener('dragover', dragOver);
        column.addEventListener('dragenter', dragEnter);
        column.addEventListener('dragleave', dragLeave);
        column.addEventListener('drop', drop);
    });

    function dragOver(e) {
        e.preventDefault();
    }

    function dragEnter(e) {
        e.preventDefault();
        this.style.backgroundColor = 'rgba(0, 0, 0, 0.2)';
    }

    function dragLeave() {
        this.style.backgroundColor = '';
    }

    function drop(e) {
        e.preventDefault(); // Prevent default behavior
        this.style.backgroundColor = '';
        this.appendChild(draggedCard);
        const applicationId = draggedCard.dataset.applicationId;
        const columnId = this.dataset.columnId;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Send AJAX request to update status
        $.ajax({
            type: 'POST',
            url: '/update_status/',
            contentType: 'application/json',
            data: JSON.stringify({
                applicationId: applicationId,
                columnId: columnId,
            }),
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                console.log('Status updated successfully:', response);
                location.reload();
            },
            error: function(xhr, status, error) {
                console.error('Error updating status:', xhr.responseText);
                alert('Error updating status. Please try again.');
                location.reload();
            }
        });
        
    }
});
