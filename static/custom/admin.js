(function($) {
    $(function() {
        var selectField = $('#id_refund'),
            verified = $('.abcdefg');

        function toggleVerified(value) {
            if (value === 'True') {
                verified.show();
            } else {
                verified.hide();
            }
        }

        // show/hide on load based on pervious value of selectField
        toggleVerified(selectField.checked);

        // show/hide on change
        selectField.change(function() {
            toggleVerified($(this).checked);
        });
    });
})(django.jQuery);