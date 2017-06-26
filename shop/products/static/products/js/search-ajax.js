$(document).ready(function() {
    var expr =
    var category = getParameterByName('cat');
    var manufacturers = JSON.parse(getParameterByName('manufs'));
    var colors = JSON.parse(getParameterByName('clrs'));

    if (colors != null) {
        colors = colors.map(function(shortName) {
            return selectColor(shortName, 'select#color option.color');
        });
    }

    $('select#category').selectpicker('val', category);
    $('select#manufacturer').selectpicker('val', manufacturers);
    $('select#color').selectpicker('val', colors);


    $('.filter').on('change', function (e) {
        var category = $('select#category').val();
        var manufacturers = $('select#manufacturer').val();
        var colors = $('select#color').val();
        var hasWifi = $('input#wifi').is(':checked');
        var hasBluetooth = $('input#bluetooth').is(':checked');

        var params = {};

        if (Boolean(category)) {
            params['cat'] = category;
        }

        if (colors != null) {
            colors = colors.map(getColorShortName);
            params['clrs'] = JSON.stringify(colors);
        }

        if (manufacturers != null) {
            params['manufs'] = JSON.stringify(manufacturers);
        }

        if (hasBluetooth) {
            params['has_bluetooth'] = true;
        }

        if (hasWifi) {
            params['has_wifi'] = true;
        }

        $.ajax({
            url: '/search/',
            type: 'GET',
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
    return (name[0] == fs) && (name[name.length-1] == ls);
}


function selectColor(shortName, selector) {
    result = ''

    if (shortName.length == 2) {
        firstSymbol = shortName[0].toUpperCase();
        lastSymbol = shortName[1];

         $(selector).each(function(index, value) {
            colorFullName = $(this).val();

            if (checker(colorFullName, firstSymbol, lastSymbol)) {
                result = colorFullName;
                return false;
            }
         });
    }

    return result;
}