function showUsername() {
    $.ajax({
        type: 'GET',
        url: '/api/v1/user',
        success: function(data) {
            console.log(data);
            $('#username').html(data.username);
            $('#nav-username').removeClass("hidden");
            $('#nav-login').addClass("hidden");
        },
        error: function(jqXHR, textStatus, errorThrown) {
            $('#nav-login').removeClass("hidden");
            console.log(jqXHR.status);
        }
    });
}

function showHotBooks() {
    $.ajax({
        type: 'GET',
        url: '/api/v1/hotbooks',
        data: {
            'num': 8,
        },
        success: function(data) {
            console.log(data);
            $('#hotbooks div.thumbnail').each(function(index, value) {
                var div = $(value);
                var book = data[index];
                div.find('img').attr('src', book.img_url);
                div.find('h3').html(book.name);
                div.find('p').html(book.description);
                div.find('a.btn').attr('href', book.url);
                div.find('span.download').html('下载量' + book.download_time);
                div.find('span.credit').html(book.score + '积分');
            });
        },
    });
}

showUsername();
showHotBooks();

$('#login-form').on('submit', (function(e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        type: 'POST',
        url: "/login",
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log(data);
            showUsername();
            $('#myModal').modal('hide');
        },
    });
}));
