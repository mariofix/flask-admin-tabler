// Bootstrap 5 modal content loader.
// Replaces Flask-Admin's bs4_modal.js which relied on Bootstrap 4 attributes
// (data-toggle / data-target).  Bootstrap 5 uses data-bs-toggle / data-bs-target
// and fires the show.bs.modal event with relatedTarget pointing to the trigger
// element, so we use that to load remote content via AJAX.
$(document).on('show.bs.modal', '.modal', function (event) {
    var trigger = $(event.relatedTarget);
    var url = trigger.attr('href');
    if (url) {
        $(this).find('.modal-content').load(url);
    }
});
