$('#signup-form').validator().on('submit', (function(e) {
    if (!e.isDefaultPrevented()) {
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: '/register',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                console.log(data);
                $('#register-success').click();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $('#used-email').removeClass('hidden');
            }
        });
    }
}));

$('#back').click((function(e) {
    e.preventDefault();
    window.location.href='/';
}));
