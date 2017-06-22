$(document).ready(function() {
    $(document).on('click', '.like',function() {
        var path = window.location.pathname.split('/');
        var id = null;

        var i = path.length;
        while (i--) {
            if (/^id\d+/.test(path[i])) {
                id = +path[i].slice(2);
                break;
            }
        }

        params = {'id': id, 'action': $(this).attr('id')};

        console.log(params);

        if (id != null) {
            $.ajax({
                url: '/like/',
                type: 'GET',
                data: params,

                success: function(data) {
                    $('#btns').html(data);
                },

                failure: function() {
                    alert('Error');
                }
            });
        }
    });
});