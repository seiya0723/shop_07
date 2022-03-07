window.addEventListener("load" , function (){

$(function(){
  /*=================================================
  画像切り替え
  ===================================================*/
  // サムネイルの画像をホバーした際の処理
  $('#thumbnail img').on('mouseover', function(){

    // ホバーされた画像のパスを取得
    // $(this)はイベントが発生した要素を指すため、1つ目のサムネイルがホバーされた際は1つ目のsrcを、
    // 2つ目のサムネイルがホバーされた際は2つ目のsrcを取得する
    let img_src = $(this).attr("src");

    // メイン画像と同じサムネイルがホバーされた際は画像切り替えを実行しない
    // （メイン画像のsrcとホバーされた画像のsrcが異なる場合のみ実行）
    if($('#mainvisual img').attr("src") != img_src) {

      // メイン画像を0.5秒かけてフェードアウトし、フェードアウトが完了したら
      // メイン画像のsrcをホバーされたサムネイルのsrcに変更して
      // メイン画像を0.5秒かけてフェードインする
      // ※「フェードアウトが完了した後に実行」のように、何かの処理が終わったあとに実行させたい場合は、
      // 今回のようのコールバック関数を使用します。詳しくは「コールバック関数」で調べてみてください
      $('#mainvisual img').fadeOut(500, function() {
        $("#mainvisual img").attr({src:img_src});
        $("#mainvisual img").fadeIn(500);
      })
    }
  });
});
});

window.addEventListener("load" , function (){

    $(document).on("input", ".input_image" ,function(){ $("#image_area").append('<input class="input_image" type="file" name="image">'); })

    $("#image_submit").on("click", function(){ send_image(this); });
});


function send_image(elem){

    let form_elem   = $(elem).parent("form");
    let raw_data    = new FormData( $(form_elem).get(0) );
    let url         = $(form_elem).prop("action");
    let method      = $(form_elem).prop("method");
    let data        = new FormData();
    let images      = [];


    for (let v of raw_data ){
        console.log(v);
        //image以外を抜き取り、FormDataにセットしておく。
        if (v[0] != "image"){
            data.set(v[0],v[1]);
        }
        else{
            //imageのデータはimagesにまとめておく。
            images.push(v);
        }
    }

    //imagesから1つずつ画像をセットしてAjax送信する。

    for (let image of images ){

        data.set(image[0],image[1]);

        $.ajax({
            url: url,
            type: method,
            data: data,
            processData: false,
            contentType: false,
            dataType: 'json'

        }).done( function(data, status, xhr ) {
            console.log("Done");

        }).fail( function(xhr, status, error) {

            //Fail
        });
    }
}