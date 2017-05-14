function book_template(img_url, title) {
    var html = [
'<div class="col-xs-6 col-sm-3">',
    '<div class="thumbnail">',
        '<img src="' + img_url + '" alt="Book image">',
        '<div class="caption">',
            '<h3>' + title + '</h3>',
        '</div>',
        '<a href="#" class="btn btn-info btn-download" role="button"><span class="glyphicon glyphicon-download-alt" aria-hidden="true"></span>',
            '<span class="credit">',
                '下载',
            '</span>',
        '</a>',
    '</div>',
'</div>',
    ].join("\n");
    return html;
}

function showPurchasedBook() {
    $("li.active").removeClass("active");
    $("#book-list").empty();
    $("#purchased-li").addClass("active");
    $("#page-header").html("已购项目");
    $.ajax({
        type: 'GET',
        url: '/api/v1/purchase_list',
        success: function(data) {
            console.log(data);
            $.each(data, function(index, book) {
                var html = book_template(book.img_url, book.name);
                $("#book-list").append(html);
            });
        },
    });
}

function showFavoredBook() {
    $("li.active").removeClass("active");
    $("#book-list").empty();
    $("#favored-li").addClass("active");
    $("#page-header").html("我的收藏");
    $.ajax({
        type: 'GET',
        url: '/api/v1/purchase_list',
        success: function(data) {
            console.log(data);
            $.each(data, function(index, book) {
                var html = book_template(book.img_url, book.name);
                $("#book-list").append(html);
            });
        },
    });
}

function showUploadBook() {
    $("li.active").removeClass("active");
    $("#book-list").empty();
    $("#uploaded-li").addClass("active");
    $("#page-header").html("我的上传");
    $.ajax({
        type: 'GET',
        url: '/api/v1/upload_list',
        success: function(data) {
            console.log(data);
            $.each(data, function(index, book) {
                var html = book_template(book.img_url, book.name);
                $("#book-list").append(html);
            });
        },
    });
}

showPurchasedBook();
$("#purchased-li").click(showPurchasedBook);
$("#favored-li").click(showFavoredBook);
$("#uploaded-li").click(showUploadBook);

function page_num() {
    html = [
'<hr>',
'<nav aria-label="...">',
  '<ul class="pagination">',
    '<li>',
      '<a href="#" aria-label="Previous">',
        '<span aria-hidden="true">&laquo;</span>',
      '</a>',
    '</li>',
    '<li class="active"><a href="#">1 <span class="sr-only">(current)</span></a></li>',
    '<li><a href="#">2</a></li>',
    '<li><a href="#">3</a></li>',
    '<li><a href="#">4</a></li>',
    '<li><a href="#">5</a></li>',
    '<li>',
      '<a href="#" aria-label="Next">',
        '<span aria-hidden="true">&raquo;</span>',
      '</a>',
    '</li>',
  '</ul>',
'</nav>',
    ].join("\n");
    return html;
}
