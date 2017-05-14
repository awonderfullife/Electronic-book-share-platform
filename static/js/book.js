function getBook() {
    var id = + window.location.pathname.split('/')[2];
    $.ajax({
        type: 'GET',
        url: '/api/v1/ebook',
        data: {
            'id': id,
        },
        success: function(data) {
            console.log(data);
            book = data;
            $('#book-img').attr('src', data.img_url);
            $('#name').html(data.name);
            $('#uploader').html(data.uploader);
            $('#upload-time').html(data.created_at);
            $('#download-times').html(data.download_times);
            $('#score').html(data.score);
            $('#need_score').html(data.score);
            $('#confirm-score').html(data.score);
            $('#intro p').html(data.description);
        },
    });
}

function purchase_verify() {
    var id = + window.location.pathname.split('/')[2];
    $.ajax({
        type: 'GET',
        url: '/api/v1/purchase_verify',
        data: {
            'id': id,
        },
        success: function(data) {
            console.log(data);
            $('#book-img').attr('src', data.img_url);
            $('#name').html(data.name);
            $('#uploader').html(data.uploader);
            $('#upload-time').html(data.created_at);
            $('#download-times').html(data.download_times);
            $('#score').html(data.score);
            $('#intro p').html(data.description);
            $('#confirm').modal('show');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            if (jqXHR.status == 400) {
                $('#not-login').modal('show');
            } else if (jqXHR.status == 500) {
                $('#need-more-score').modal('show');
                $('#curr_score').html(jqXHR.responseJSON.current_score);
            }
        },
    });
}

function purchase() {
    var id = + window.location.pathname.split('/')[2];
    $.ajax({
        type: 'GET',
        url: '/api/v1/purchase',
        data: {
            'id': id,
        },
        success: function(data) {
            getBook();
            $('#download').removeClass('hidden');
            $('#purchase').addClass('hidden');
            alert('购买成功');
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            if (jqXHR.status == 400) {
                $('#not-login').modal('show');
            } else if (jqXHR.status == 500) {
                $('#need-more-score').modal('show');
                $('#curr_score').html(jqXHR.responseJSON.current_score);
            }
        },
    });
}

function purchased() {
    var id = + window.location.pathname.split('/')[2];
    $.ajax({
        type: 'GET',
        url: '/api/v1/purchased',
        data: {
            'id': id,
        },
        success: function(data) {
            console.log(data);
            if (data.purchased) {
                $('#download').removeClass('hidden');
            } else {
                $('#purchase').removeClass('hidden');
            }
        },
    });
}

function download() {
    var id = + window.location.pathname.split('/')[2];
    var url = '/download/' + id;
    window.open(url, 'Download');
}

getBook();
purchased();
$('#purchase').on('click', purchase_verify);
$('#download').on('click', download);
$('#confirm-purchase').on('click', purchase);
userManager.run();
