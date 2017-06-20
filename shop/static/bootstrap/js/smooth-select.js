$(document).ready(function() {
    $('select').on('show.bs.select', function() {
        var parent = $(this).parent();
        $(parent).find('div.dropdown-menu.open').first().stop(true, true).slideDown();
    });

    $('select').on('hide.bs.select', function() {
        $('div.dropdown-menu.open').stop(true, true).slideUp();
    });
});