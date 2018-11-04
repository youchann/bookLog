$("#searchForm").submit(function(){

    let search = $("#searchWord").val();
    let url = 'https://www.googleapis.com/books/v1/volumes?q=intitle:' + search;

    //検索データの取得
    if(search == ''){
        alert("検索語句を入力してください")
    } else {

        $.getJSON(url, function(data) {

            //2回目以降の検索時のため、要素を削除
            $(".searched_list").remove();

            if (data.totalItems != 0) {

                //検索ヒット数分、要素を追加
                data.items.forEach(function(val, j){

                    //要素の作成
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

                    //「本棚に追加」ボタンの実装(どうしてもFlask側で実装したい為、コードが汚くなった)
                    let singleQuote = "'";
                    let addButton = $('<button onclick="location.href=' + singleQuote + '/add/' + data.items[j].id + singleQuote + '">本棚に追加する</button>');
                    
                    //ページへ表示
                    $("#result").append('<li class="searched_list"></li>');
                    $(".searched_list").eq(j).append(title, authers, publishedDate, thumbnailURL, addButton);
                });
            } else {
                //検索結果が見つからないときの処理(いずれ書く)
            }
            
        });
    }
    return false;
});