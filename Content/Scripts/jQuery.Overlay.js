/****************************************************
*  创建者：老黄牛
*  时间：2009-9-17
*****************************************************/
$(function() { overlay_init(); });
function overlay_init() { 
    rightOverlay_write() 
    $("#r_overlay").hide();
}

//在右上角显示加载动画
function rightOverlay_write() {
    $('body').append('<div id="r_overlay" style="z-index:999999;padding:2px 10px;position:fixed !important; position:absolute;border:0px solid black; background-color:red;color:yellow;top:0px;right:0px;"/>');
    $('#r_overlay').append("正在处理中，请稍候...");
}

jQuery.RightOverlay = {

    hide: function () { $("#r_overlay").hide(); },
    show: function() { $("#r_overlay").show(); }
}