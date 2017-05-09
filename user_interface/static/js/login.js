function showUsername() {
    $.ajax({
        type: 'GET',
        url: '/api/v1/user',
        success: function(data) {
            console.log(data);
            $('#username').html(data.username);
            $('#nav-username').removeClass('hidden');
            $('#nav-login').addClass('hidden');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $('#nav-login').removeClass('hidden');
            console.log(jqXHR.status);
        }
    });
}

showUsername();

$('#login-form').on('submit', (function(e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        type: 'POST',
        url: '/login',
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log(data);
            showUsername();
            $('#myModal').modal('hide');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $('#login-error').removeClass('hidden');
        }
    });
}));
