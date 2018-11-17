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

                    //長い文字列を省く
                    let titleText = data.items[j].volumeInfo.title;
                    let authorsText = data.items[j].volumeInfo.authors;
                    authorsText = authorsText.join(",");
                    titleText = titleText.length > 15 ? (titleText).slice(0,15)+"…" : titleText;
                    authorsText = authorsText.length > 14 ? (authorsText).slice(0,14)+"…" : authorsText;

                    //要素の作成
                    let title = $('<p class="searched_title">' + titleText + '</p>');
                    let authers = $('<p class="searched_authors">' + authorsText + '</p>');
                    //let publishedDate = $('<p class="searched_publishedDate">' + data.items[j].volumeInfo.publishedDate + '</p>');
                    let thumbnailURL = '';

                    //サムネイル画像の取得
                    if("imageLinks" in data.items[j].volumeInfo == true){
                        thumbnailURL = $('<img src=\"' + data.items[j].volumeInfo.imageLinks.smallThumbnail + '\" />');
                    } else {
                        thumbnailURL = $('<img src=\"' + "/static/Thumbnail_Not_Found.png" + '\" />');
                    }

                    //「本棚に追加」ボタンの実装(どうしてもFlask側で実装したい為、コードが汚くなった)
                    let singleQuote = "'";
                    let addButton = $('<button class="btn btn-success" onclick="location.href=' + singleQuote + '/add/' + data.items[j].id + singleQuote + '">本棚に追加する</button>');
                    
                    //ページへ表示
                    $("#row").append('<div class="searched_list col-md-3 col-sm-4 col-6"></div>');
                    $(".searched_list").eq(j).append(thumbnailURL);
                    $(".searched_list").eq(j).append('<div class="book_info"></div>');
                    $(".book_info").eq(j).append(title, authers, addButton);
                });
            } else {
                //検索結果が見つからないときの処理(いずれ書く)
            }
            
        });
    }
    return false;
});