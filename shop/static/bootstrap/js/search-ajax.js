$(document).ready(function() {
    $('select').on('change', function () {
        //history.pushState('', '', '?pis=os')

        var category = $('select#category').val();
        var manufacturers = $('select#manufacturer').val();
        var colors = $('select#color').val();
        var params = {}

        if (category != null) {
            params['cname'] = category;
        }


        console.log(manufacturers);
        console.log(colors);


        if (color != null) {
            color = color[0] + color[color.length-1];
        }

        $.ajax({
            url: '/search/',
            type: 'get',
            data: params,

            success: function(data) {
                $('#ajax-div').html(data);
            },

            failure: function() {
                alert('Invalid data');
            }
        });
    });
});