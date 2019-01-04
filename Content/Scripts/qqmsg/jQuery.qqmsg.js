/* 
 *  Document   : hLoading
 *  Created on : 2011-12-11, 14:37:38
 *  
 *  使用方法：
 *      $.hLoading.show({type:'loading',msg:'加载中'});  //type: loading,success,hits,fail
        $('#divID').hLoading()
        $('#divID').hLoading({type:'loading',msg:'加载中'});

        $.hLoading.hide() //隐藏
        $('#divID').hLoading.hide();
 *
 *
 */
; (function ($) {
    //动态生成ID
    var createDomId = function () {
        var s4 = function() {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        };
        return "rdi-" + (s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4());
    };

    var maskClass = {
        position: 'fixed',
        left: 0,
        top: 0,
        width: '100%',
        height: '100%',
        filter: 'alpha(opacity=70)',
        opacity: '0.70',
        background: '#cccccc',
        overflow: 'hidden'
    };

    function loadingInit(target, options) {
        var $mask = $('<div class="rdi-qqmsg-mask"></div>'); //遮罩层
        var $loading = $('<div class="rdi-qqmsg-layer_wrap"/>'); //消息
        var layerId = $(target).attr('id');
        if (!layerId)
            layerId = createDomId();

        $mask.css(maskClass).appendTo($(target)).hide().attr("id", layerId + '_mask');

        var maskWidth;
        var maskHeight;

        var borderTopWidth = $(target).css('border-top-width');
        var borderLeftWidth = $(target).css('border-left-width');

        //
        // IE will return values like 'medium' as the default border, 
        // but we need a number
        //
        borderTopWidth = isNaN(parseInt(borderTopWidth)) ? 0 : borderTopWidth;
        borderLeftWidth = isNaN(parseInt(borderLeftWidth)) ? 0 : borderLeftWidth;

        var overlayLeftPos = jQuery(target).offset().left + parseInt(borderLeftWidth);
        var overlayTopPos = jQuery(target).offset().top + parseInt(borderTopWidth);

        maskWidth = parseInt(jQuery(target).width()) + parseInt(jQuery(target).css('padding-right')) + parseInt(jQuery(target).css('padding-left'));
        maskHeight = parseInt(jQuery(target).height()) + parseInt(jQuery(target).css('padding-top')) + parseInt(jQuery(target).css('padding-bottom'));
       
        if ($(target)[0].outerHTML.indexOf('<body') == -1) {
            $mask.css('width', maskWidth + 'px');
            $mask.css('height', maskHeight + 'px');
        }
        $mask.css('left', overlayLeftPos + 'px');

        $mask.css('top', overlayTopPos + 'px');
        $mask.css('z-index', options.zIndex);


        var iconCls = 'gtl_ico_loading';
        switch (options.type) {
            case 'success':
                iconCls = 'gtl_ico_succ';
                break;
            case "fail":
                iconCls = "gtl_ico_fail";
                break;
            case "hits":
                iconCls = 'gtl_ico_hits';
                break;
            
        }

        if (options.type && options.type != 'loading' ) {
            $loading.appendTo(target).attr("id", layerId + '_loading').empty()
                .append('<span class="rdi-qqmsg-layer"  id="mode_tips_v2"><span class="' + iconCls + '"></span>' +
                    options.msg + '<span class="gtl_end"></span></span>').css('z-index', options.zIndex + 1);
        } else {
            $loading.appendTo(target).attr("id", layerId + '_loading').empty()
            .append('<span class="rdi-qqmsg-layer"  id="mode_tips_v2"><span class="gtl_ico_clear"></span><span class="' + iconCls + '"></span>' +
                options.msg + '<span class="gtl_end"></span></span>').css('z-index', options.zIndex + 1);
        }
      
        var indicatorTop = overlayTopPos;

        if (options.marginTop) {
            indicatorTop += parseInt(options.marginTop);
        }

        var indicatorLeft = overlayLeftPos;

        //
        // set horizontal position
        //
        $loading.css('left', (indicatorLeft + (($mask.width() - parseInt($loading.width())) / 2)).toString() + 'px');

        //
        // set vertical position
        //
        $loading.css('top', (indicatorTop + (($mask.height() - parseInt($loading.height())) / 2)).toString() + 'px');

        setTimeout(function () {
            target.hLoading.hide(target, options.onAfterHide);
        },options.timeout);
		
        return $loading;
    }

    

    $.fn.hLoading = function(options) {
        options = $.extend({}, $.fn.hLoading.defaults, options||{});
        var hl = loadingInit(this, options);
        
        if (typeof (options.onBeforeShow) == 'function') {
            options.onBeforeShow();
        }

        hl.show();
        var id = hl.attr('id').split('_').splice(0,1);
        $('#' + id.join('_') + '_mask').show();
        
        if (typeof (options.onAfterShow) == 'function') {
            options.onAfterShow();
        }

        return this;
        
    };

    $.fn.hLoading.hide = function(jq,fn) {
        return jq.each(function() {
            var wrap = $(this);
            $("div.rdi-qqmsg-mask", wrap).fadeOut(function() {
                $(this).remove();
            });
            $("div.rdi-qqmsg-layer_wrap", wrap).fadeOut(function() {
                $(this).remove();
            });
            if (typeof(fn) == 'function') {
                fn();
            }
        });
    };

    $.hLoading = {
        hide: function () {
            var wrap = $('body');
            $("div.rdi-qqmsg-mask", wrap).fadeOut(function () {
                $(this).remove();
            });
            $("div.rdi-qqmsg-layer_wrap", wrap).fadeOut(function () {
                $(this).remove();
            });
        },
        show: function(options) {
            $('body').hLoading(options);
        }
    };


    $.fn.hLoading.defaults = {
        opacity: 0.6,
        msg: '正在加载中...',
        zIndex: 1000000,
        timeout: 3000,
        type: 'loading',
        onBeforeShow: '',
        onAfterShow: '',
        onAfterHide:'' //在隐藏后执行
    };

})(jQuery)