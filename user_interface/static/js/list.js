function showHotBooks() {
    $.ajax({
        type: 'GET',
        url: '/api/v1/hotbooks',
        data: {
            'num': 18,
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

$(document).ready(function () {
  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });
  showHotBooks();
});
