$(document).ready(function() {
    $('select').on('show.bs.select', function() {
        var parent = $(this).parent();
        $(parent).find('div.dropdown-menu.open').first().stop(true, true).slideDown();
    });

    $('select').on('hide.bs.select', function() {
        $('div.dropdown-menu.open').stop(true, true).slideUp();
    });

    $('select').on('change', function() {
        var firstSelOption = $(this).find('option:selected:first').index();
        firstOptionIndex = 1

        if ($(this).attr('multiple') == 'multiple') {
            firstOptionIndex = 0
        }

        if (firstSelOption == firstOptionIndex) {
            $(this).selectpicker('val', []);
        }
    });
});