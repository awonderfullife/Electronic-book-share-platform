function book_template(book) {
    var html = [
'<div class="col-md-3 col-sm-4 col-md-8">',
'  <div class="thumbnail">',
'    <a href="' + book.url + '"><img src="' + book.img_url + '"alt="Book image"></a>',
'    <div class="caption">',
'      <h3>' + book.name + '</h3>',
'      <p>' + book.description.slice(0, 30) + '</p>',
'    </div>',
'    <span class="download">下载量' + book.download_times + '</span>',
'    <a href="' + book.url + '"class="btn btn-success" role="button">',
'      <span class="glyphicon glyphicon-shopping-cart" aria-hidden="true"></span>',
'      <span class="credit">' + book.score + '积分</span>',
'    </a>',
'  </div>',
'</div>',
    ].join("\n");
    return html;
}

function showHotBooks() {
    $.ajax({
        type: 'GET',
        url: '/api/v1/hotbooks',
        data: {
            'num': 8,
        },
        success: function(data) {
            $.each(data, function(index, book) {
                var html = book_template(book);
                $("#hotbooks").append(html);
            });
        },
    });
}

showHotBooks();
userManager.run();
