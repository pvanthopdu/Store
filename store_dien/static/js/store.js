/**
 * Created by pvantho on 4/3/2019.
 */
var current = "";
$(".btn-close").click(function () {
    $(".collapse").collapse('hide');
});
$("#menu_1").click(function () {
    alert(current);
    $(this).addClass("clickmenu_link");
    $(current).removeClass("clickmenu_link");
    current = "#menu_1";

});
$("#menu_2").click(function () {
    alert(current);
    $(this).addClass("clickmenu_link");
    $(current).removeClass("clickmenu_link");
    current = "#menu_2";
});
$("#menu_3").click(function () {
    alert(current);
    $(this).addClass("clickmenu_link");
    $(current).removeClass("clickmenu_link");
    current = "#menu_3"
})
