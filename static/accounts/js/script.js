window.addEventListener("load" , function (){
//ドロップダウンの設定を関数でまとめる
function mediaQueriesWin(){
	var width = $(window).width();
	if(width <= 768) {//横幅が768px以下の場合 $(".has-child>a").off('click');	//has-childクラスがついたaタグのonイベントを複数登録を避ける為offにして一旦初期状態へ
		$(".has-child>a").on('click', function() {//has-childクラスがついたaタグをクリックしたら
			var parentElem =  $(this).parent();// aタグから見た親要素のliを取得し
			$(parentElem).toggleClass('active');//矢印方向を変えるためのクラス名を付与して
			$(parentElem).children('ul').stop().slideToggle(500);//liの子要素のスライドを開閉させる※数字が大きくなるほどゆっくり開く
			return false;//リンクの無効化
		});
	}else{//横幅が768px以上の場合
		$(".has-child>a").off('click');//has-childクラスがついたaタグのonイベントをoff(無効)にし
		$(".has-child>a").removeClass('active');//activeクラスを削除
		$('.has-child').children('ul').css("display","");//スライドトグルで動作したdisplayも無効化にする
	}
}
// ページがリサイズされたら動かしたい場合の記述
$(window).resize(function() {
	mediaQueriesWin();/* ドロップダウンの関数を呼ぶ*/
});
// ページが読み込まれたらすぐに動かしたい場合の記述
$(window).on('load',function(){
	mediaQueriesWin();/* ドロップダウンの関数を呼ぶ*/
});

});

window.addEventListener("load" , function (){
    $("#postcode_search").on("click",function(){ search_postcode(); });
});
function search_postcode(){
    //未入力の場合は処理しない。(出来ればここで郵便番号のフォーマットになっているか正規表現でチェックしたほうが良いだろう)
    if (!$("#postcode").val()){
        return false;
    }
    //http://zipcloud.ibsnet.co.jp/doc/api
    //https://zipcloud.ibsnet.co.jp/api/search?zipcode=7830060

    $.ajax({
        url: "https://zipcloud.ibsnet.co.jp/api/search?zipcode=" + $("#postcode").val(),
        type: "GET",
    }).done( function(data, status, xhr ) {
        //このdataは文字列で返ってくるのでまずはJSONに変換させる必要がある。
        json    = JSON.parse(data);

        //都道府県
        console.log(json["results"][0]["address1"])

        //〇〇市
        console.log(json["results"][0]["address2"])

        //〇〇
        console.log(json["results"][0]["address3"])

        $("#prefecture").val(json["results"][0]["address1"]);
        $("#city").val(json["results"][0]["address2"])
        $("#address").val(json["results"][0]["address3"])

    }).fail( function(xhr, status, error) {
        console.log("通信エラー")
    });


}