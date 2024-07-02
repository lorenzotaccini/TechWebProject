$(document).ready(function() {
    $('.watchlist-btn').click(function() {
        var icon = $(this);
        var movie_id = $(this).attr('data-movie-id');
        $.ajax({
            url: icon.data('url'),
            type: 'POST',
            data: {
                movie_id: movie_id,
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (icon.text() === 'Add to Watchlist') icon.text('Remove from Watchlist');
                else icon.text('Add to Watchlist');
            },
            error: function(xhr, status, error) {
                console.log('Errore:', error);
                alert('An error occurred, try again later.');
            }
        });
    });
});
