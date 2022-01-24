$( document ).on( 'click', '.details a', function(event) {
    if (event.target.hasAttribute('href')) {
        var link = event.target.href + 'ajax/';
        var link_array = link.split('/');
        if (link_array[4] == 'category') {
            $.ajax({
                url: link,
                success: function (data) {
                    $('.details').html(data.result);
                },
            });

            event.preventDefault();
        }
    }
});
