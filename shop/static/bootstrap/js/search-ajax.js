$(document).ready(function() {
    $('select').on('change', function () {
        var category = $('select#category').val();
        var manufacturer = $('select#manufacturer').val();

        var color = $('select#color').val();

        if (color != null) {
            color = color[0] + color[color.length-1];
        }

        console.log(category);
        console.log(color);
        console.log(manufacturer);

        $.ajax({
            url: '/search/',
            type: 'get',
            data: {
                'cname': category
            },

            success: function(data) {
                $('#ajax-div').html(data);
            },

            failure: function() {
                alert('Invalid data');
            }
        });
    });
});