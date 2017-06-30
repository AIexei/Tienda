$(document).ready(function() {
    $('form#buy').on('submit', function(e) {
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
        var cost = $('h4.product-cost b').text();
        var url = '/buy/id' + id + '/c' + cost.slice(1) + '/';

        $.ajax({
            type: 'POST',
            url: url,
            data: params,

            success: function(data) {
                location.reload();
                bootbox.alert('hello');
            },

            failure: function() {
                $('#myModal').modal('hide');
                alert('Error');
            }
        });
    });
});