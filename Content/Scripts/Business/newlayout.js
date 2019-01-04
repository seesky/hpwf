
var onlyOpenTitle = "我的桌面";
var openTabs = 7; //允许打开的窗口数量
var errorUrl = 'Error/Error404.html';
$(function () {
    if (_menus) {
        initNav();
        tabClose();
        //addTab("欢迎使用", "welcome.html", "icon-house_star");
        addTab("我的桌面", "desktop.html", "icon16_home_page");
    } else {
        $.messager.alert("系统提示", "<font color=red><b>您没有任何权限，请联系管理员!</b></font>", "warning", function () {
            location.href = 'login.htm';
        });
    }

    $('#editpass').click(function () {        
        editMyPass();
    });

    $('body').layout({
        onExpand: function () {
            $('body').layout('resize');
        }
    });

    //Tab右键菜单
    $('#closeMenu').menu({
        onClick: function (item) {
            closeTab(item.id);
        }
    });
});

function initNav() {
    if (sys_config.navType) {
        switch (sys_config.navType) {
        case "Accordion":
            Accordion.InitLeftMenu(); //手风琴形式
            break;
        case "Tree":
            treeNav.init(); //树形结构
            break;
        case "AccordionTree": //手风琴+树形目录(2级+)
            AccordionTree.init();
            break;
        default:
            Accordion.InitLeftMenu();
            break;
        }
    } else {
        Accordion.InitLeftMenu();
    }
   
    $('#tabs').tabs({
        tools: [{
            title:"首页",
            iconCls: "icon16_home_page",
            handler: function () {
                addTab("我的桌面", "desktop.html", "icon16_home_page");
                return false;
            }
        },
        {
            iconCls: 'icon16_arrow_refresh',
            handler: function () {
                var tab = $('#tabs').tabs('getSelected');
                if (tab.panel('options').title != onlyOpenTitle)
                    closeTab('refresh');
                else
                    return false;
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

//手风琴效果导航
var Accordion = {
    addNav: function(data) {
        $.each(data, function(i, sm) {
            var menulist = "";
            menulist += '<ul>';
            $.each(sm.children, function(j, o) {
                var cssIcon = 'icon16_page'; //没有设置图标，则取一个默认图标
                if (o.IconCss) {
                    cssIcon = o.IconCss;
                }

                menulist += '<li><div><a ref="' + o.Id + '" href="#" rel="'
                    + o.NavigateUrl + '" ><span  iconCls="' + cssIcon + '" class="icon ' + cssIcon
                    + '" >&nbsp;</span><span class="nav">' + o.FullName
                    + '</span></a></div></li> ';
            });
            menulist += '</ul>';

            $('#wnav').accordion('add', {
                title: sm.FullName,
                content: menulist,
                iconCls: 'icon ' + sm.IconCss,
                border: false
            });
        });

        var pp = $('#wnav').accordion('panels');
        var t = pp[0].panel('options').title;
        $('#wnav').accordion('select', t);
    },
    InitLeftMenu: function() {
        $("#wnav").accordion({ animate: false, fit: true, border: false });
        Accordion.addNav(_menus);

        $('.accordion li').click(function() {
            var a = $(this).children('div').children('a');
            var tabTitle = $(a).children('.nav').text();

            var url = $(a).attr("rel");
            var menuid = $(a).attr("ref");
            var icon = $(a).children('.icon').attr('class');

            addTab(tabTitle, url, icon);
            $('.accordion li div').removeClass("selected");
            $(this).children('div').addClass("selected");
        }).hover(function() {
            $(this).children('div').addClass("hover");
        }, function() {
            $(this).children('div').removeClass("hover");
        });
    }
};

//手风琴 +tree
var AccordionTree = {
    init: function () {
        $.each(_menus, function (i, n) {
            var cssIcon = 'icon16_page'; //没有设置图标，则取一个默认图标
            if (n.iconCls) {
                cssIcon = n.iconCls;
            }

            $('#wnav').append('<div style="padding:0px;" title="' + n.text
                                 + '" data-options="border:false,iconCls:\''
                                 + cssIcon
                                 + '\'"><ul id="nt'
                                 + i
                                 + '"></ul></div>');
        });

        $("#wnav").accordion({
            fit: true,
            border: false,
            onSelect: function (t, i) {
                $('#nt' + i).tree({
                    lines: false,
                    animate: true,
                    data: _menus[i].children,
                    onClick: function (node) {
                        if (node.attributes.url != "" && node.attributes.url != '#') {
                            addTab(node.text, node.attributes.url + '?navid=' + node.id, node.iconCls);
                        } else {
                            if (node.attributes.url != '#') {
                                addTab(node.text, errorUrl, node.iconCls);
                            }
                        }
                    }
                });
            }
        });
    }
};


//横向导航
var MenuButton = {
    initMenuItem: function(n, str) {
        $.each(n.children, function(j, o) {
            //递归
            if (o.children.length > 0) {
                str += '<div>';
                str += '<span iconCls="' + o.iconCls + '">' + o.title + '</span><div style="width:120px;">';
                str = MenuButton.initMenuItem(o, str);
                str += '</div></div>';
            } else
                str += '<div iconCls="' + o.iconCls + '" id="' + o.url + '">' + o.title + '</div>';
        });
        return str;
    },
    addNav: function(data) {
        var menulist = "";
        var childMenu = '';
        $.each(data, function(i, n) {
            menulist += String.format('<a href="javascript:void(0)" id="mb{0}" class="easyui-menubutton" menu="#mm{0}" iconCls="{1}">{2}</a>',
            (i + 1), n.iconCls, n.title);

            if (n.children.length > 0) {
                childMenu += '<div id="mm' + (i + 1) + '" style="width:120px;">';
                childMenu = MenuButton.initMenuItem(n, childMenu);

                childMenu += '</div>';
            }
        });

        $('#wnav').append(menulist).append(childMenu);

    },
    init: function() {
        MenuButton.addNav(_menus);
        $('#wnav').css({ 'float': 'left', 'width': '100%', 'height': '30px', 'padding': '3px 0px 0px 20px', 'background': '#6ABEFA url(/images/datagrid_title_bg.png)' });

        if (theme == "gray") {
            $('#wnav').css('background', 'url(Scripts/easyui/themes/gray/images/tabs_enabled.gif)');
        }

        var northPanel = $('body').layout('panel', 'north');
        northPanel.panel('resize', { height: 103 });

        $('body').layout('resize');

        var mb = $('#wnav .easyui-menubutton').menubutton();
        $.each(mb, function(i, n) {
            $($(n).menubutton('options').menu).menu({
                onClick: function(item) {
                    var tabTitle = item.text;
                    var url = item.id;
                    var icon = item.iconCls;
                    addTab(tabTitle, url, icon);
                    return false;
                }
            });
        });
    }
};

//左侧树形菜单
var treeNav = {
    init: function () {
        $("#wnav").tree({
            animate: true,
            lines: true,
            data: _menus,
            onClick: function (node) {
                if (node.attributes.url != '#' && node.attributes.url != '') {
                    addTab(node.text, node.attributes.url + '?navid=' + node.id, node.iconCls);
                } else {
                    if (node.attributes.url != '#') {
                        addTab(node.text, errorUrl, node.iconCls);
                    }
                }
            }
        });
    }
};

function addTab(subtitle, url, icon) {
    //if (!url && url === "#") {
    if (!url) {
        url = errorUrl;
        //return false;
    }
    var tabCount = $('#tabs').tabs('tabs').length;
    var hasTab = $('#tabs').tabs('exists', subtitle);
    var add = function() {
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
        $.messager.confirm("系统提示", msg, function(b) {
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
                $.ajaxtext('ajax/editpass.ashx', "newPassword=" + $('#txtNewPassword').val() + '&oldPassword=' + $('#txtOldPassword').val(), function (msg) {
                    if (msg == '1') {
                        layer.msg('成功修改登录密码，请重新登录！!', { icon: 9 }); 
                        location.href = 'ajax/loginout.ashx';
                    } else {
                        $.messager.alert('温馨提示', msg, 'warning');                      
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