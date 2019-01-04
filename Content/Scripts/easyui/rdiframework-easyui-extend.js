(function ($) {
    function guidDialogId() {
        var s4 = function () {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        };
        return "RDIFramework-" + (s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4());
    }
    ///////////////////////////////////////////////////////////////////////////////////////////////
    //新的弹出窗口方法
    $.hDialog = function (options) {
        options = $.extend({}, $.hDialog.defaults, options || {});

        var dialogId = guidDialogId();
        if (options.id)
            dialogId = options.id;

        //if (!options.href && !options.content) {
        //    alert('缺少必要的参数 href or content');
        //    return false;
        //}

        var defaultBtn = [{
            text: '确定',
            iconCls: 'icon16_ok',
            handler: options.submit
        }, {
            text: '关闭',
            iconCls: 'icon16_cancel',
            handler: function () {
                $("#" + dialogId).dialog("close");
            }
        }];

        if (!options.showBtns)
            defaultBtn = [];

        if (options.buttons.length == 0)
            options.buttons = defaultBtn;

        if (options.max) {
            //dialog.dialog('maximize');
            var winWidth = $(window).width();
            var winHeight = $(window).height();
            options.width = winWidth - 20;
            options.height = winHeight - 20;
        }


        var $dialog = $('<div/>').css('padding', options.boxPadding).appendTo($('body'));

        var dialog = $dialog.dialog($.extend(options, {
            onClose: function () {
                dialog.dialog('destroy');
            }
        })).attr('id', dialogId);
        //.dialog('refresh').dialog('open')

        $dialog.find('.dialog-button').css('text-align', options.align);

        return dialog;
    };

    $.hDialog.defaults = $.extend({}, $.fn.dialog.defaults, {
        boxPadding: '3px',
        align: 'right', //按钮对齐方式
        href: '',
        id: '',
        content: '',
        height: 200,
        width: 400,
        collapsible: false,
        minimizable: false,
        maximizable: false,
        closable: true,
        modal: true,
        shadow: false,
        mask: true,
        cache: false,
        closed: false, //默认是否关闭窗口 如果为true,需调用open方法打开
        showBtns: true,
        buttons: [],
        submit: function () {
            alert('写入可执行代码');
            return false;
        },
        onBeforeClose: function () {
            $(this).find(".combo-f").each(function () {
                var panel = $(this).data().combo.panel;
                panel.panel("destroy");
            });
            $(this).empty();
        },
        onMove: function (left, right) {
            $('.validatebox-tip').remove();
        }

    });

    ///////////////////////////////////////////////////////////////////////////////////////////////

    $.hWindow = function (options) {
        var windowId = guidDialogId();

        options = $.extend({}, $.hDialog.defaults, options || {});
        if (!options.href && !options.content) {
            alert('缺少必要的参数 href or content');
            return false;
        }

        var $dialog = $('<div/>').attr('id', windowId).appendTo($('body'));

        if (options.max) {
            //dialog.dialog('maximize');
            var winWidth = $(window).width();
            var winHeight = $(window).height();
            options.width = winWidth - 20;
            options.height = winHeight - 20;
        }

        var win = $dialog.window($.extend(options, {
            onClose: function () {
                win.window('destroy');
            }
        })).window('refresh').attr('id', windowId);


        return win;
    };

    $.hWindow.defaults = $.extend({}, $.fn.window.defaults, {
        href: '',
        content: '',
        height: 300,
        width: 400,
        collapsible: false, 	//折叠
        closable: true,         //显示右上角关闭按钮
        minimizable: false, 	//最小化
        maximizable: false, 	//最大化
        resizable: true, 	    //是否允许改变窗口大小
        title: '窗口标题', 	    //窗口标题
        modal: true, 		    //模态	
        draggable: true,        //允许拖动
        fit: false, //当该项设置为true时设置panel的大小自适应父容器, 下面的示例展示,他将自动适应父容器内部最大尺寸 
        max: false,
        onBeforeClose: function () {
            $(this).find(".combo-f").each(function () {
                var panel = $(this).data().combo.panel;
                alert(panel.html());
                panel.panel("destroy");
            });
            $(this).empty();
        }
    });

    /////////////////////////////////////////////////////////////////////////////////////////////////
    //以前的1.0版前的打开弹窗的方法
    $.fn.hWindow = function (options) {
        var self = this;
        var defaults = {
            width: 500, 			//宽度
            height: 400, 		//高度
            iconCls: '', 		//图标class
            collapsible: false, 	//折叠
            closable: true, //显示右上角关闭按钮
            minimizable: false, 	//最小化
            maximizable: false, 	//最大化
            resizable: false, 	//改变窗口大小
            title: '窗口标题', 	//窗口标题
            modal: true, 		//模态	
            draggable: true, //允许拖动
            submit: function () {
                alert('写入执行的代码。');
            },
            html: '',
            center: true,         //每次弹出窗口居中
            url: '',          //要加载文件的地址
            showclosebtn: true, //显示关闭按钮
            closeText: '取消', // 默认关闭按钮显示文本
            okText: '确定', //默认提交按钮显示文本
            onload: function () {
                //加载文件完成后，执行的函数
            },
            max: false //是否最大化窗口
        };
        var options = $.extend(defaults, options);
        var win_width = $(window).width();
        var win_height = $(window).height();

        if (options.max) {
            options.width = win_width - 20;
            options.height = win_height - 20;
        }

        var _top = (win_height - options.height) / 2;
        var _left = (win_width - options.width) / 2;



        var html = options.html;
        $.extend(options, {
            top: _top, left: _left, content: buildWindowContent(html, options.submit, options.url), onBeforeClose: function () {
                $(this).find(".combo-f").each(function () {
                    var panel = $(this).data().combo.panel;
                    panel.panel("destroy");
                });
                $(this).empty();

                $('body .validatebox-tip').remove();
            }
        });
        $(self).window(options).window('open');

        //$(self).keyup(function (e) {
        //    if (e.keyCode == 27) {
        //        $(self).window('close'); return false;
        //    }
        //}).focus();

        function buildWindowContent(contentHTML, fn, url) {
            var centerDIV = $('<div region="center" border="false" style="padding:5px;"></div>').html(contentHTML);
            if (url && url != '')
                centerDIV.empty().load(url, options.onload);
            $('<div class="easyui-layout" fit="true"></div>')
			.append(centerDIV)
			//.append('<div region="south" border="false" style="padding-top:5px;height:40px; overflow:hidden; text-align:center;background:#fafafa;border-top:#eee 1px solid;"> <button id="AB" class="sexybutton"><span><span><span class="ok">' + options.okText + '</span></span></span></button> ' +
			.append('<div region="south" border="false" style="padding-top:5px;height:40px; overflow:hidden; text-align:center;border-top:#eee 1px solid;"> <button id="AB" class="sexybutton"><span><span><span class="ok">' + options.okText + '</span></span></span></button> ' +
            (options.showclosebtn ? '&nbsp; <button title="ESC 关闭" id="AC" class="sexybutton"><span><span><span class="cancel">' + options.closeText + '</span></span></span></button>' : '')
            + '</div>')
			.appendTo($(self).empty())
			.layout();

            $('button[id="AC"]').click(function () {
                $(self).window('close'); return false;
            });

            $('#AB', self).unbind('click').click(fn);
        }
    };
    $.hxlMessage = {
        alertInfo: function (title, msg) {
            $.messager.alert(title, msg, 'info');
        },
        alertError: function (title, msg) {
            $.messager.alert(title, msg, 'error');
        },
        alerWarning: function (title, msg) {
            $.messager.alert(title, msg, 'warning');
        }
    }; //Dialog
    $.fn.hDialog = function (options) {
        var defaults = {
            width: 300,
            height: 200,
            title: '此处标题',
            html: '',
            iconCls: '',
            modal: true,
            showbtn: true,
            btns: [{
                text: '确定',
                iconCls: 'icon-ok',
                handler: options.submit
            }, {
                text: '取消',
                iconCls: 'icon16_cancel',
                handler: function () {
                    $('#' + id).dialog('close'); return false;
                }
            }],
            submit: function () { alert('可执行代码.'); }
        };
        var id = $(this).attr('id');

        var self = this;

        options = $.extend(defaults, options);
        $(self).dialog({
            href: options.href,
            title: options.title,
            height: options.height,
            width: options.width,
            iconCls: options.iconCls,
            onLoad: options.onload,
            modal: options.modal,
            buttons: (function () {
                if (options.showbtn)
                    return options.btns;
                else
                    return null;
            })()
        });

        function createContent() {
            $('.dialog-content', $(self)).empty().append('<div id="' + id + '_content" style="padding:5px;"></div>');
            if (options.html != '')
                $('#' + id + "_content").html(options.html);
        }
        createContent();
    };

    function createtip(el) {
        var box = $(el);
        var msg = box.attr('tip');
        var tip = $("<div class=\"validatebox-tip\">" + "<span class=\"validatebox-tip-content\">" + "</span>" + "<span class=\"validatebox-tip-pointer\">" + "</span>" + "</div>").appendTo("body");
        tip.find(".validatebox-tip-content").html(msg);
        el.data("tip", tip);
        tip.css({ display: "block", left: box.offset().left + box.outerWidth(), top: box.offset().top });
    }

    function removetip(el) {
        var tip = el.data("tip");
        if (tip) {
            tip.remove();
            $(el).removeData("tip");
        }
    }

    $.fn.tip = function (options) {
        return this.each(function () {
            var msg = $(this).attr('tip');
            if (msg) {
                switch (options.trigger) {
                    case "hover":
                        $(this).hover(function () { createtip($(this)); }, function () { removetip($(this)); });
                        break;
                    default:
                        $(this).focus(function () {
                            createtip($(this));
                        }).blur(function () {
                            removetip($(this));
                        });
                        break;
                }
            }
        });
    }; ///////////////////////////////////////////////////////////////////////////////////////////////
    //扩展datagrid 方法 getSelectedIndex
    $.extend($.fn.datagrid.methods, {
        getSelectedIndex: function (jq) {
            var row = $(jq).datagrid('getSelected');
            if (row)
                return $(jq).datagrid('getRowIndex', row);
            else
                return -1;
        }
        ,
        checkRows: function (jq, idValues) {
            if (idValues && idValues.length > 0) {
                var rows = $(jq).datagrid('getRows');
                var keyFild = $(jq).datagrid('options').idField;
                $.each(rows, function (i, n) {
                    if ($.inArray(n[keyFild], idValues)) {
                        $(jq).datagrid('checkRow', row);
                    }
                });
            }
            return jq;
        }
    });
    //扩展 combobox 方法 selectedIndex
    $.extend($.fn.combobox.methods, {
        selectedIndex: function (jq, index) {
            if (!index)
                index = 0;
            var data = $(jq).combobox('options').data;
            var vf = $(jq).combobox('options').valueField;
            $(jq).combobox('setValue', eval('data[index].' + vf));
        }
    });
    //Easyui tree扩展tree方法获取目标节点的一级子节点，具体的用法和getChildren方法是一样的，只是这个只返回目标节点的第一级子节点。
    $.extend($.fn.tree.methods, {
        getLeafChildren: function (jq, params) {
            var nodes = [];
            $(params).next().children().children("div.tree-node").each(function () {
                nodes.push($(jq[0]).tree('getNode', this));
            });
            return nodes;
        }
    });

    //在tree的实现了有选中getSelected方法和带单选的getChecked和uncheck，却少了一个unSelect方法。
    //使用方法：
    //  var node = $("#tt1").tree("getSelected");
    //  $("#tt1").tree("unSelect", node.target);    
    $.extend($.fn.tree.methods, {
        unSelect: function (jq, target) {
            return jq.each(function () {
                $(target).removeClass("tree-node-selected");
            });
        }
    });

    //释放IFRAME内存
    $.fn.panel.defaults = $.extend({}, $.fn.panel.defaults, {
        onBeforeDestroy: function () {
            var frame = $('iframe', this);
            if (frame.length > 0) {
                try {
                    frame[0].contentWindow.document.write('');
                    frame[0].contentWindow.close();
                } catch (err) {
                }
                frame.remove();
                if ($.browser.msie) {
                    CollectGarbage();
                }
            }
        }
    });

    //tree 方法扩展 全选、取消全选
    $.extend($.fn.tree.methods, {
        checkedAll: function (jq, target) {
            var data = $(jq).tree('getChildren');
            if (target)
                data = $(jq).tree('getChildren', target);

            $.each(data, function (i, n) {
                $(jq).tree('check', n.target);
            });
        }
    });

    $.extend($.fn.tree.methods, {
        uncheckedAll: function (jq) {
            var data = $(jq).tree('getChildren');
            $.each(data, function (i, n) {
                $(jq).tree('uncheck', n.target);
            });
        }
    });

    //2013-12-11 日扩展
    function autoResize(c) {
        var a = {
            width: 6,
            height: 119,
            gridType: "jqgrid"
        };
        c = $.extend(a, c);
        var d = b();
        if ($.isFunction(c.callback)) {
            c.callback(d);
        }
        $(window).resize(function () {
            var e = b(true);
            switch (c.gridType) {
                case "datagrid":
                    $(c.dataGrid).datagrid("resize", {
                        width: e.width,
                        height: e.height
                    });
                    break;
                case "treegrid":
                    $(c.dataGrid).treegrid("resize", {
                        width: e.width,
                        height: e.height
                    });
                    break;
                case "jqgrid":
                    $(c.dataGrid).jqGrid("setGridHeight", e.height).jqGrid("setGridWidth", d.width);
                    break;
            }
        });
        function b(e) {
            var g = 0;
            var f = 0;
            if (typeof (window.innerHeight) == "number") {
                g = window.innerHeight;
                f = window.innerWidth;
            } else {
                if (document.documentElement && document.documentElement.clientHeight) {
                    g = document.documentElement.clientHeight;
                    f = document.documentElement.clientWidth;
                } else {
                    if (document.body && document.body.clientHeight) {
                        g = document.body.clientHeight;
                        f = document.body.clientWidth;
                    }
                }
            }
            f -= c.width;
            g -= c.height;
            return {
                width: f,
                height: g
            };
        }
    };
    
    //$.fn.datagrid.defaults.onRowContextMenu = pageContextMenu.createDataGridContextMenu;
    //$.fn.treegrid.defaults.onContextMenu = pageContextMenu.createTreeGridContextMenu;

    var createGridHeaderContextMenu = function (e, field) {
        e.preventDefault();
        var grid = $(this); /* grid本身 */
        var headerContextMenu = this.headerContextMenu; /* grid上的列头菜单对象 */
        var okCls = 'tree-checkbox1'; // 选中
        var emptyCls = 'tree-checkbox0'; // 取消
        if (!headerContextMenu) {
            var tmenu = $('<div style="width:100px;"></div>').appendTo('body');
            var fields = grid.datagrid('getColumnFields');
            for (var i = 0; i < fields.length; i++) {
                var fildOption = grid.datagrid('getColumnOption', fields[i]);
                if (!fildOption.hidden) {
                    $('<div iconCls="' + okCls + '" field="' + fields[i] + '"/>')
						.html(fildOption.title).appendTo(tmenu);
                } else {
                    $('<div iconCls="' + emptyCls + '" field="' + fields[i] + '"/>')
						.html(fildOption.title).appendTo(tmenu);
                }
            }
            headerContextMenu = this.headerContextMenu = tmenu.menu({
                onClick: function (item) {
                    var field = $(item.target).attr('field');
                    if (item.iconCls == okCls) {
                        grid.datagrid('hideColumn', field);
                        $(this).menu('setIcon', {
                            target: item.target,
                            iconCls: emptyCls
                        });
                    } else {
                        grid.datagrid('showColumn', field);
                        $(this).menu('setIcon', {
                            target: item.target,
                            iconCls: okCls
                        });
                    }
                }
            });
        }
        headerContextMenu.menu('show', {
            left: e.pageX,
            top: e.pageY
        });
    };

    $.fn.datagrid.defaults.onHeaderContextMenu = createGridHeaderContextMenu;
    $.fn.treegrid.defaults.onHeaderContextMenu = createGridHeaderContextMenu;    
})(jQuery)