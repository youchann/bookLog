$("#searchForm").submit(function(){

    let search = $("#searchWord").val();
    let url = 'https://www.googleapis.com/books/v1/volumes?q=intitle:' + search;



    //検索データの取得
    if(search == ''){
        alert("検索語句を入力してください")
    } else {

        $.getJSON(url, function(data) {

            $("#result").text(data.items[0].volumeInfo.authors[0]);
            data.items.forEach(function(val, j){

                let title = $('<h5 class="searched_title">' + data.items[j].volumeInfo.title + '</h5>');
                let authers = $('<p class="searched_authres">' + data.items[j].volumeInfo.authers + '</p>');
                let publishedDate = $('<p class="searched_publishedDate">' + data.items[j].volumeInfo.publishedDate + '</p>');
                let thumbnailURL = '';

                //サムネイル画像の取得
                if("imageLinks" in data.items[j].volumeInfo == true){
                    thumbnailURL = $('<img src=\"' + data.items[j].volumeInfo.imageLinks.smallThumbnail + '\" />');
                } else {
                    thumbnailURL = $('<img src=\"' + "/static/Thumbnail_Not_Found.png" + '\" />');
                }

                //ページへ表示
                $("#result").append('<li class="searched_list"></li>');
                $(".searched_list").eq(j).append(title);
                $(".searched_list").eq(j).append(authers);
                $(".searched_list").eq(j).append(publishedDate);
                $(".searched_list").eq(j).append(thumbnailURL);

            });
        });
    }
    return false;
});