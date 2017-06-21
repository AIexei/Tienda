$(document).ready(function() {
    console.log('ready');


    var category = getParameterByName('cat');
    var manufacturers = JSON.parse(getParameterByName('manufs'));

    console.log(category);
    console.log(manufacturers);

    var colors = JSON.parse(getParameterByName('clrs'))

    if (colors != null) {
        colors = colors.map(function(shortName) {
            return selectColor(shortName, 'select#color option.color');
        });
    }


    console.log(colors);



    $('select#category').selectpicker('val', category);
    $('select#manufacturer').selectpicker('val', manufacturers);
    $('select#color').selectpicker('val', colors);


    /*
    $('input[type=checkbox]').on('change', function() {
        var wifi = $('input#wifi').val();
        var bluetooth = $('input#bluetooth').val();
    });
    */


    $('select').on('change', function () {
        var category = $('select#category').val();
        var manufacturers = $('select#manufacturer').val();
        var colors = $('select#color').val();

        var params = {}

        if (category != null) {
            params['cat'] = category;
        }

        if (colors != null) {
            colors = colors.map(getColorShortName);
            params['clrs'] = JSON.stringify(colors);
        }

        if (manufacturers != null) {
            params['manufs'] = JSON.stringify(manufacturers);
        }

        $.ajax({
            url: '/search/',
            type: 'get',
            data: params,

            success: function(data) {
                history.pushState('', '', this.url)
                $('#ajax-div').html(data);
            },

            failure: function() {
                alert('Error');
            }
        });
    });
});


function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}


function getColorShortName(longName) {
    longName = longName.toLowerCase();
    return longName[0] + longName[longName.length-1];
}


function checker(name, fs, ls) {
    return (name[0] == fs) && (name[name.length == ls])
}


function selectColor(shortName, selector) {
    if (shortName.length == 2) {
        firstSymbol = shortName[0].toUpperCase();
        lastSymbol = shortName[1];

         $(selector).each(function(index, value) {
            colorFullName = $(this).val();

            if (checker(colorFullName, firstSymbol, lastSymbol)) {
                return colorFullName;
            }
         });
    }

    return '';
}