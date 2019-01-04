/**
* rdiframework-index.js
* Copyright © RDIFramework.NET V3.0

* RDIFramework.NET，基于.NET的快速信息化系统开发、整合框架，给用户和开发者最佳的.Net框架部署方案。
* 框架官网：http://www.rdiframework.net/
* 框架博客：http://blog.rdiframework.net/
* 交流QQ：406590790 
* 邮件交流：406590790@qq.com
* 其他博客：
* http://www.cnblogs.com/huyong 
* http://blog.csdn.net/chinahuyong
*/

var onlyOpenTitle = "我的桌面";
var openTabs = 7; //允许打开的窗口数量

$(function () {
    initNav();
    $('#editPass').click(function () {
        editMyPass();
    });
    tabClose();

    //Tab右键菜单
    $('#closeMenu').menu({
        onClick: function (item) {
            closeTab(item.id);
        }
    });
});

function initNav() {
    $('#tabs').tabs({
        tools: [{
            title: "首页",
            iconCls: "icon16_home_page",
            handler: function () {
                addTab("我的桌面", '@Url.Content("~/Home/StartPage")', "icon16_home_page");
                return false;
            }
        },
        {
            iconCls: 'icon16_arrow_refresh',
            handler: function () {
                var tab = $('#tabs').tabs('getSelected');
                if (tab.panel('options').title != onlyOpenTitle) {
                    closeTab('refresh');
                }
                else {
                    return false;
                }
            }
        },
        {
            iconCls: 'icon16_DeleteRed',
            handler: function () {
                layer.confirm('确认关闭所有打开的窗口吗?', { icon: 4, title: '关闭提示' }, function (index) {
                    closeTab("closeall");
                    layer.close(index);
                });
            }
        }],
        onContextMenu: function (e, title) {
            if (title !== onlyOpenTitle) { //起始页不创建快捷菜单
                e.preventDefault();
                $('#closeMenu').menu('show', {
                    left: e.pageX,
                    top: e.pageY
                });
                $('#tabs').tabs('select', title);
            } else {
                return false;
            }
        }
    });
}

function addTab(subtitle, url, icon) {
    //if (!url && url === "#") {
    if (!url) {
        url = errorUrl;
        //return false;
    }
    var tabCount = $('#tabs').tabs('tabs').length;
    var hasTab = $('#tabs').tabs('exists', subtitle);
    var add = function () {
        if (!hasTab) {
            $('#tabs').tabs('add', {
                title: subtitle,
                content: createFrame(url),
                closable: (subtitle != onlyOpenTitle),
                icon: icon
            });
        } else {
            $('#tabs').tabs('select', subtitle);
            //closeTab('refresh'); //选择TAB时刷新页面
        }
    };

    if (tabCount > openTabs && !hasTab) {
        var msg = '<b>打开页面过多，可能会影响程序程序的展现效率，继续打开？</b>';
        $.messager.confirm("系统提示", msg, function (b) {
            if (b) {
                add();
            } else {
                return false;
            }
        });
    } else {
        add();
    }
    return false;
}

function createFrame(url) {
    var s = '<iframe scrolling="auto" frameborder="0"  style="width:100%;height:100%;" src="' + url + '" ></iframe>';
    return s;
}

function tabClose() {
    //双击关闭TAB选项卡
    $(".tabs-inner").live('dblclick', function () {
        var subtitle = $(this).children(".tabs-closable").text();
        if (subtitle != onlyOpenTitle && subtitle != "")
            $('#tabs').tabs('close', subtitle);
    });
}

function closeTab(action) {
    var alltabs = $('#tabs').tabs('tabs');
    var currentTab = $('#tabs').tabs('getSelected');
    var allTabtitle = [];
    $.each(alltabs, function (i, n) {
        allTabtitle.push($(n).panel('options').title);
    });
    var currtabTitle;
    var tabIndex;
    switch (action) {
        case "refresh":
            var iframe = $(currentTab.panel('options').content);
            var src = iframe.attr('src');
            $('#tabs').tabs('update', {
                tab: currentTab,
                options: {
                    content: createFrame(src)
                }
            });
            break;
        case "close":
            currtabTitle = currentTab.panel('options').title;
            $('#tabs').tabs('close', currtabTitle);
            break;
        case "closeall":
            $.each(allTabtitle, function (i, n) {
                if (n != onlyOpenTitle) {
                    $('#tabs').tabs('close', n);
                }
            });
            break;
        case "closeother":
            currtabTitle = currentTab.panel('options').title;
            $.each(allTabtitle, function (i, n) {
                if (n != currtabTitle && n != onlyOpenTitle) {
                    $('#tabs').tabs('close', n);
                }
            });
            break;
        case "closeright":
            tabIndex = $('#tabs').tabs('getTabIndex', currentTab);
            if (tabIndex == alltabs.length - 1) {
                layer.msg('右侧无待关闭的窗口!', { icon: 9 });
                return false;
            }
            $.each(allTabtitle, function (i, n) {
                if (i > tabIndex) {
                    if (n != onlyOpenTitle) {
                        $('#tabs').tabs('close', n);
                    }
                }
            });
            break;
        case "closeleft":
            tabIndex = $('#tabs').tabs('getTabIndex', currentTab);
            if (tabIndex == 1) {
                layer.msg('起始页不能关闭!', { icon: 9 });
                return false;
            }
            $.each(allTabtitle, function (i, n) {
                if (i < tabIndex) {
                    if (n != onlyOpenTitle) {
                        $('#tabs').tabs('close', n);
                    }
                }
            });
            break;
        case "exit":
            $('#closeMenu').menu('hide');
            break;
    }
}


var htmlEditPassowrd = '<table class="grid" id="ePForm">';
htmlEditPassowrd += '<tr><td>登录名：</td><td><span id="loginName"></span></td></tr>';
htmlEditPassowrd += '<tr><td>原密码：</td><td><input  validType="safepass"  required="true" id="txtOldPassword" name="oldPassword" type="password" class="txt03" /></td></tr>';
htmlEditPassowrd += '<tr><td>新密码：</td><td><input  validType="safepass"  required="true" id="txtNewPassword" name="newPassword" type="password" class="txt03" /></td></tr>';
htmlEditPassowrd += '</table>';


var editMyPass = function () {
    top.$('#w').hWindow({
        width: 300, height: 210, title: '修改密码', iconCls: 'icon16_key', html: htmlEditPassowrd, submit: function () {
            if ($('#txtNewPassword').validatebox('isValid')) {
                $.ajaxtext('/Login/ChangePassword', "newPassword=" + $('#txtNewPassword').val() + '&oldPassword=' + $('#txtOldPassword').val(), function (msg) {
                    if (msg.Data > 0) {
                        layer.msg('成功修改登录密码，请重新登录！', { icon: 9 });
                        window.setTimeout(function () {
                            getAjax("/Login/OutLogin", "", function (data) {
                                top.location.href = '../Login/Index';
                            });
                        }, 200);
                    } else {
                        $.messager.alert('温馨提示', msg.Message, 'warning');
                    }
                });
            }
        }
    });

    $('#loginName').text($('#curname').text());
    $('#txtNewPassword').validatebox();
    $('#txtOldPassword').validatebox();
    $('#txtOldPassword').focus();
};