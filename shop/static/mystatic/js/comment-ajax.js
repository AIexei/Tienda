$(document).ready(function() {
    $('#add-comment form').on('submit', function(e) {
        e.preventDefault();

        var path = window.location.pathname.split('/');
        var id = null;

        var i = path.length;
        while (i--) {
            if (/^id\d+/.test(path[i])) {
                id = +path[i].slice(2);
                break;
            }
        }

        var params = $(this).serialize();
        var url = '/add_comment/' + id + '/';

        $.ajax({
            type: 'POST',
            url: url,
            data: params,

            success: function(data) {
                $('div#cmnts').html(data);
            },

            failure: function() {
                alert('Error')
            }
        });
    });
});