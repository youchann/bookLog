
//モーダルウィンドウ
$(function () {
    $('.BookThumbnail').click(function(){
        $('.modalArea').fadeIn();
    });
    $('.closeModal , .modalBg').click(function(){
        $('.modalArea').fadeOut();
    });
    });


//該当データがない場合の関数
function addNoneData(classname, eqnum){
    $(classname).eq(eqnum).text("データがありません");
};

//APIからデータの取得
for (let i = 0; i < bookId.length; i++){
    let id = bookId[i];
    let url = 'https://www.googleapis.com/books/v1/volumes?q=id:' + id;
    let isFirstLoop = true;

    //Google Books APIの利用
    $.getJSON(url, function(data) {
    //サムネイル画像の取得
    if("imageLinks" in data.items[0].volumeInfo == true){
        $(".BookThumbnail").eq(i).html('<img src=\"' + data.items[0].volumeInfo.imageLinks.smallThumbnail + '\" />');
    } else {
        $(".BookThumbnail").eq(i).html('<img src=\"' + "/static/Thumbnail_Not_Found.png" + '\" />');
    }

    //題名の取得
    $(".BookTitle").eq(i).text(data.items[0].volumeInfo.title);

    //著者の取得
    if(data.items[0].volumeInfo.authors[0] != ""){
        data.items[0].volumeInfo.authors.forEach(function(val, j){
        if(isFirstLoop){
            $(".BookAuther").eq(i).text(data.items[0].volumeInfo.authors[j]);
            isFirstLoop = false;
        } else {
            $(".BookAuther").eq(i).append("," + data.items[0].volumeInfo.authors[j]);
        }
        });
    } else {
        addNoneData(".BookAuther", i);
    }

    //出版日の取得
    if(data.items[0].volumeInfo.publishedDate != ""){
        $(".PublishedDate").eq(i).text(data.items[0].volumeInfo.publishedDate);
    } else {
        addNoneData(".PublishedDate", i);
    }

    //あらすじの取得
    if(data.items[0].volumeInfo.description != ""){
        $(".BookDescription").eq(i).text(data.items[0].volumeInfo.description);
    } else {
        addNoneData(".BookDescription", i);
    }
    });
}