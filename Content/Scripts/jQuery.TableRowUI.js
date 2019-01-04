; (function ($) {
    $.fn.TableRowUI = function (options) {
        var defaults = {
            evenRowClass: "tr-even",
            oddRowClass: "tr-odd",
            activeRowClass: "tr-active",
            selectRowClass:"tr-select"
        }
        var options = $.extend(defaults, options);
        this.each(function () {
            var table = $(this);
            //添加奇偶行颜色            
            $(table).find("tr:even").addClass(options.evenRowClass);
            $(table).find("tr:odd").addClass(options.oddRowClass);

            $("tr", table).hover(function () {
                $(this).addClass(options.activeRowClass);
            }, function () {
                $(this).removeClass(options.activeRowClass);
            }).click(function(){
                var _index = $("tr",table).index($(this));
                $('table').data('tr_index',_index);

                
                //$(":checkbox",table).removeAttr('checked');
                //$("td:eq(0)",$(this)).find(":checkbox").attr('checked',true).click(function(event){
                    //event.stopPropagation(); //停止事件冒泡
                //});

                $("tr",table).removeClass(options.selectRowClass);
                $(this).addClass(options.selectRowClass);
            })
        })
    }

    $.hxl = {
        text:function(options){
            var defaults= {
                clickClass:'txt-click'
            }

            options = $.extend(defaults,options);

            $(':text').live('focus',function(){
                $(this).addClass(options.clickClass);
            }).live('blur',function(){
                $(this).removeClass(options.clickClass);
            })
        }
    }

    $(function(){
        $.hxl.text();
        $('.grid2').TableRowUI();
    });
})(jQuery);