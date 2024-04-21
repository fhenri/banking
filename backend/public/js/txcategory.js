function updateCategory(thisObj) {
    var $input = thisObj;
    var formId = $input.data('form-id');
    var newCategory = $input.val().toLowerCase();
    if (newCategory.trim() === "") {
        // leave function if category is empty
        return false;
    }
    var $form = $('#' + formId);
    var $parentTd = $input.parent();
    var url = $form.attr('action');
    var method = $form.attr('method');
    var formData = $form.serialize(); 

    // check if we already have the category in the current datalist
    const existingCategory = 
        $(`#categories option[value=${newCategory}]`).val();

    $.ajax({
        url: url,
        type: method,
        data: formData,
        success: function(response) {
            // add the span for this new category
            $spanElt = $("<span class=\"tx-category\">");
            $spanElt.attr('data-form-id', formId);
            $spanElt.text(` ${newCategory} `);
            
            // clean value from input and add new element to list
            $input.val('');
            $parentTd.append($spanElt);
            $spanElt.after("&nbsp; ");

            // add the new category in the datalist
            if (!existingCategory) {
                $categoriesElt = $('#categories');
                $categoriesElt.append(`<option value=\"${newCategory}\">`);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error submitting form:", error);
        }
    });
}

$(document).ready(function () {

    $('#transactionTable').DataTable({
        // Optional: add DataTables configuration options here
        "info": false,  // dont display info
        "lengthChange": false,  // dont allow to change number of items per page
        "pageLength": 50,   // default to 50 items per page
        "paging": true, // Enable pagination
        "searching": true, // Enable searching
        "ordering": true // Enable column ordering
    });

    $('body').on('focusout', 'input[name="txNewCategory"]', function() {
        updateCategory($(this));
        // Prevent the default form submission
        return false;
    });

    $('body').on('keypress', 'input[name="txNewCategory"]', function(e) {
        if ( e.which == 13 ) {
            updateCategory($(this));
            return false;
        }
    } );

    // Attach click event listener to all current and future .tx-category spans
    $('body').on('click', '.tx-category', function() {

        var formId = $(this).data('form-id');

        // Remove the clicked span
        var $removed = $(this).remove();

        // add an input element to store the value being deleted so we can send to server
        var $delCategory = $("<input>").attr("type", "hidden")
        $delCategory.attr('name', "delCategory");
        $delCategory.val($removed.text());

        var $form = $('#' + formId);            
        $form.append($delCategory);

        var url = $form.attr('action');
        var method = $form.attr('method');
        var formData = $form.serialize(); // Serialize the form data for AJAX submission

        // Use AJAX to submit the form data
        $.ajax({
            url: url,
            type: method,
            data: formData,
            success: function(response) {
                // remove the temp category we have added above
                $delCategory.remove();
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });

        // Prevent the default form submission
        return false;
    });
});
