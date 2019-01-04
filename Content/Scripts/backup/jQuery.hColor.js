/*
作者：EricHU

页面中加入的CSS
.colorpicker{position: absolute;top:0px; background:#fafafa;padding:2px;border:1px solid #666;z-index:9999999;}
.colorpicker table td{border: 1px solid #3E3E3E;cursor: pointer;}
.colorpicker table {border-collapse:collapse}

调用方法：
$('input').hColor();

*/


$.fn.hColor = function (options) {

    var loc = "", td = "";
    loc += "<tr>";
    var hexarr = ["ff0000", "ffff00", "00ff00", "00ffff", "0000ff", "ff00ff", "ffffff", "ebebeb", "e1e1e1", "d7d7d7", "cccccc", "c2c2c2", "b7b7b7", "acacac", "a0a0a0", "959595", "ee1d24", "fff100", "00a650", "00aeef", "2f3192", "ed008c", "898989", "7d7d7d", "707070", "626262", "555555", "464646", "363636", "262626", "111111", "000000", "f7977a", "fbad82", "fdc68c", "fff799", "c6df9c", "a4d49d", "81ca9d", "7bcdc9", "6ccff7", "7ca6d8", "8293ca", "8881be", "a286bd", "bc8cbf", "f49bc1", "f5999d", "f16c4d", "f68e54", "fbaf5a", "fff467", "acd372", "7dc473", "39b778", "16bcb4", "00bff3", "438ccb", "5573b7", "5e5ca7", "855fa8", "a763a9", "ef6ea8", "f16d7e", "ee1d24", "f16522", "f7941d", "fff100", "8fc63d", "37b44a", "00a650", "00a99e", "00aeef", "0072bc", "0054a5", "2f3192", "652c91", "91278f", "ed008c", "ee105a", "9d0a0f", "a1410d", "a36209", "aba000", "588528", "197b30", "007236", "00736a", "0076a4", "004a80", "003370", "1d1363", "450e61", "62055f", "9e005c", "9d0039", "790000", "7b3000", "7c4900", "827a00", "3e6617", "045f20", "005824", "005951", "005b7e", "003562", "002056", "0c004b", "30004a", "4b0048", "7a0045", "7a0026"];
    $.each(hexarr, function (i, n) {
        td = '<td rel="' + n + '" style="background:#' + n + '" ></td>';
        loc += td;
        if (i == hexarr.length - 1)
            loc += "</tr>";
        else if ((i + 1) / 16 > 0 && ((i + 1) % 16) == 0)
            loc += "</tr><tr>";
    });

    var winHeight = $(window).height() / 2;
    var currinput, offsettop;
    return this.each(function (e) {

        $(this).click(function () {
            currinput = $(this);
            $('#colortable').remove();
            var colorbox = $('<div id="colortable" class="colorpicker"></div>').appendTo($('body'));
            var offset = currinput.offset();

            if (offset.top > winHeight)
                offsettop = offset.top - 140;
            else
                offsettop = offset.top + currinput.outerHeight(true);

            var tdwidth = 18;
            $('#colortable').width(tdwidth * 16);
            colorbox.html('<table cellpadding=0>' + loc + '<table>')
			.css({ left: offset.left, top: offsettop })
			.mouseleave(function () { $(this).remove(); })
			.find('table td').click(function () {
			    var c = $(this).attr('rel');
			    currinput.val(c);
			    $('#colortable').remove();
			}).hover(function () {
			    $(this).css({ 'border': '1px solid #fff' });
			}, function () {
			    $(this).css({ 'border': '1px solid #000' });
			});

            $('#colortable table td').width(tdwidth).height(tdwidth);
        });
    });
}
