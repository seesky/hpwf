/**
* 用户授权范围
**/

function UserPermissionScope(model, url) {
    this.obj = model;
    this.actionLink = url;
}

UserPermissionScope.prototype = {
    show: function() {
        if (this.obj) {
            var _this = this;
            var ad = top.$.hDialog({
                title: '用户授权范围（资源管理权限）',
                width: 560,
                height: 600,
                iconCls: 'icon16_report_user',
                href: _this.actionLink,
                onLoad: function () {
                    _this.initData();
                },
                submit: function() {
                    ad.dialog('close');
                }
            });
            //top.$(ad).hLoading();
        } else {
            msg.warning("请选择权限设置对象。");
        }
    },
    initData: function() {
        var _this = this;
        top.$('#FormContent').layout('panel', 'center').panel({ title: '当前用户：' + _this.obj.REALNAME });
        top.$('#txt_ResourceId').val(_this.obj.ID);
        top.$('#tableRole,#tableUser').datagrid({
            idField: 'id',
            sortName: 'sortcode',
            sortOrder: 'asc',
            nowrap: false, //折行                   
            rownumbers: false, //行号
            striped: true, //隔行变色
            checkOnSelect: false,
            pagination: false,
            showHeader: false,
            pageSize: 20,
            pageList: [20, 40, 50]
        });

        top.$('#tableUser').datagrid({
            toolbar: [
                   { text: '全选', iconCls: 'icon16_check_box', handler: function () { top.$('#tableUser').datagrid('checkAll'); } },
                   { text: '取消全选', iconCls: 'icon16_check_box_uncheck', handler: function () { top.$('#tableUser').datagrid('uncheckAll'); } },
                   '-',
                   { text: '恢复', iconCls: 'icon16_undo', handler: function () { top.$('#tableUser').datagrid('uncheckAll'); _this.bindUser(); } },
                    '-',
                   { text: '保存', iconCls: 'icon16_save_data', handler: function () { _this.saveUserScope(); } }
            ],
        });

        top.$('#tableRole').datagrid({
            toolbar: [
                    { text: '全选', iconCls: 'icon16_check_box', handler: function () { top.$('#tableRole').datagrid('checkAll'); } },
                    { text: '取消全选', iconCls: 'icon16_check_box_uncheck', handler: function () { top.$('#tableRole').datagrid('uncheckAll'); } },
                    '-',
                    { text: '恢复', iconCls: 'icon16_undo', handler: function () { top.$('#tableRole').datagrid('uncheckAll'); _this.bindRole(); } },
                     '-',
                    { text: '保存', iconCls: 'icon16_save_data', handler: function () { _this.saveRoleScope(); } }
            ]
        });

        //业务逻辑处理
        //1、加载用户列表
       
        top.$('#tableUser').datagrid({
            url: '/Admin/FrameworkModules/UserAdmin/GetUserListJson/',
            columns: [[
               { title: 'Id', field: 'id', width: 30, align: 'left', checkbox: true },
               { title: '登录名', field: 'username', width: 130, align: 'left' },
               { title: '名称', field: 'realname', width: 150, align: 'left' }
            ]],
            onLoadSuccess: function (data) {
                _this.bindUser();
            }
        });

        //2、加载角色列表
        top.$('#tableRole').datagrid({
            url: '/Admin/FrameworkModules/RoleAdmin/GetRoleList/',
            columns: [[
                { title: 'Id', field: 'id', width: 30, align: 'left', checkbox: true },
                { title: '角色编码', field: 'code', width: 150 },
                { title: '角色名称', field: 'realname', width: 190 }
            ]],
            onLoadSuccess: function (data) {
                _this.bindRole();
            }
        });

        top.$('#tableOrganize,#tableModule,#tablePermissionItem').tree({
            cascadeCheck: false, //联动选中节点
            checkbox: true,
            lines: true,
            onContextMenu: function(e, row) {
                _this.popCMenu(e, row);
            }
        });

        //3、加载组织机构列表
        top.$('#tableOrganize').tree({
            url: '/Admin/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/?isTree=1',
            onLoadSuccess: function (data) {
                _this.bindOrganize();
            }
        });
        //4、加载模块（菜单）列表
        top.$('#tableModule').tree({
            url: '/Admin/FrameworkModules/ModuleAdmin/GetModuleTreeJson/?isTree=1',
            onLoadSuccess: function (data) {
                _this.bindModule();
            }
        });

        //5、加载操作（功能）权限列表
        top.$('#tablePermissionItem').tree({
            url: '/Admin/FrameworkModules/PermissionItemAdmin/GetPermissionItemTreeJson/?isTree=1',
            onLoadSuccess: function (data) {
                _this.bindPermissionItem();
            }
        });
    },
    popCMenu: function (e, row) { //弹出菜单
        var _this = this;
        var createRowMenu = function () {
            var rmenu = top.$('<div id="rmenu" style="width:100px;"></div>').appendTo('body');
            var menus = [{ title: '全选', iconCls: 'icon16_check_box' },
                         { title: '取消全选', iconCls: 'icon16_check_box_uncheck' }, '-',
                         { title: '恢复', iconCls: 'icon16_undo' }, '-',
                         { title: '保存', iconCls: 'icon16_save_data' }];
            for (var i = 0; i < menus.length; i++) {
                if (menus[i].title)
                    top.$('<div iconCls="' + menus[i].iconCls + '"/>').html(menus[i].title).appendTo(rmenu);
                else {
                    top.$('<div class="menu-sep"></div>').appendTo(rmenu);
                }
            }
        };
        e.preventDefault();
        if (top.$('#rmenu').length == 0) { createRowMenu(); }
        top.$('#rmenu').menu({
            onClick: function (item) {
                switch (item.text) {
                    case '全选': _this.treeCheckOppr('checkedAll'); break;
                    case '取消全选': _this.treeCheckOppr('uncheckedAll'); break;
                    case '恢复': _this.treeRestoreOppr(); break;
                    case '保存': _this.treeApply(); break;
                    default:
                        break;
                }
            }
        }).menu('show', { left: e.pageX, top: e.pageY });
    },
    bindUser: function () {
        var query = 'userId=' + (this.obj.ID || this.obj.id);
        $.ajaxjson('/Admin/FrameworkModules/ResourcePermission/GetScopeUserIdsByUserId/', query, function (arr) {
            if (arr.length > 0) {
                var tmpGrd = top.$('#tableUser');
                $.each(arr, function (i, val) {
                    tmpGrd.datagrid('checkRow', tmpGrd.datagrid('getRowIndex', val));
                });
            }
        });
    },
    bindRole: function () {
        var query = 'userId=' + (this.obj.ID || this.obj.id);
        $.ajaxjson('/Admin/FrameworkModules/ResourcePermission/GetScopeRoleIdsByUserId/', query, function (arr) {
            if (arr.length > 0) {
                var tmpGrd = top.$('#tableRole');
                $.each(arr, function (i, val) {
                    tmpGrd.datagrid('checkRow', tmpGrd.datagrid('getRowIndex', val));
                });
            }
        });
    },
    bindOrganize:function() {
        var query = 'userId=' + (this.obj.ID || this.obj.id);
        $.ajaxjson('/Admin/FrameworkModules/ResourcePermission/GetScopeOrganizeIdsByUserId/', query, function (arr) {
            if (arr.length > 0) {
                var tmpTree = top.$('#tableOrganize');
                tmpTree.tree('uncheckedAll');
                $.each(arr, function (i, val) {
                    var node = tmpTree.tree('find', val);
                    if (node) tmpTree.tree('check', node.target);
                });
            }
        });
    },
    bindModule: function () {
        var query = 'userId=' + (this.obj.ID || this.obj.id);
        $.ajaxjson('/Admin/FrameworkModules/ResourcePermission/GetScopeModuleIdsByUserId/', query, function (arr) {
            if (arr.length > 0) {
                var tmpTree = top.$('#tableModule');
                tmpTree.tree('uncheckedAll');
                $.each(arr, function (i, val) {
                    var node = tmpTree.tree('find', val);
                    if (node) tmpTree.tree('check', node.target);
                });
            }
        });
    },
    bindPermissionItem: function () {
        var query = 'userId=' + (this.obj.ID || this.obj.id);
        $.ajaxjson('/Admin/FrameworkModules/ResourcePermission/GetScopePermissionItemIdsByUserId/', query, function (arr) {
            if (arr.length > 0) {
                var tmpTree = top.$('#tablePermissionItem');
                tmpTree.tree('uncheckedAll');
                $.each(arr, function (i, val) {
                    var node = tmpTree.tree('find', val);
                    if (node) tmpTree.tree('check', node.target);
                });
            }
        });
    },
    getDgChecks:function(dgName) { //得到指定datagrid选中的主键数组
        var checkedItems = top.$('#' + dgName).datagrid('getChecked');
        var ids = [];
        $.each(checkedItems, function(index, item) {
            ids.push(item.id);
        });
        return ids.join(',');
    },
    getTvChecks: function (tvName) {//得到指定tree选中的主键数组
        var nodes = top.$('#' + tvName).tree('getChecked');
        if (nodes.length > 0) {
            var tmpIds = [];
            for (var idx = 0; idx < nodes.length; idx++) {
                tmpIds.push(nodes[idx].id);
            }
            return tmpIds.join(',');
        } else {
            return '';
        }
    },
    treeCheckOppr: function(methodName) {
        var tmpTabs = top.$('#staffTab');
        var index = tmpTabs.tabs('getTabIndex', tmpTabs.tabs('getSelected'));
        if (index && methodName) {
            switch (index) {
                case 2:
                    top.$('#tableOrganize').tree(methodName);
                    break;
                case 3:
                    top.$('#tableModule').tree(methodName);
                    break;
                case 4:
                    top.$('#tablePermissionItem').tree(methodName);
                    break;
                default: 
                    break;
            }
        }
    },
    treeRestoreOppr: function () {
        var _this = this;
        var tmpTabs = top.$('#staffTab');
        var index = tmpTabs.tabs('getTabIndex', tmpTabs.tabs('getSelected'));
        if (index) {
            switch (index) {
                case 2:
                    _this.bindOrganize();
                    break;
                case 3:
                    _this.bindModule();
                    break;
                case 4:
                    _this.bindPermissionItem();
                    break;
                default:
                    break;
            }
        }
    },
    treeApply: function () {
        var tmpTabs = top.$('#staffTab');
        var _this = this;
        var index = tmpTabs.tabs('getTabIndex', tmpTabs.tabs('getSelected'));
        if (index) {
            switch (index) {
                case 2:
                    _this.saveOrganizeScope();
                    break;
                case 3:
                    _this.saveModuleScope();
                    break;
                case 4:
                    _this.savePermissionItem();
                    break;
                default:
                    break;
            }
        }
    },
    saveUserScope: function () {
        var _this = this;
        var uIds = _this.getDgChecks('tableUser');
        var query = 'targetUserId=' + (this.obj.ID || this.obj.id) + "&userIds=" + uIds;
        $.ajaxjson('/Admin/FrameworkModules/ResourcePermission/SaveUserUserScope/', query, function (d) {
            if (d.Data > 0) {
                msg.ok(d.Message);
            } else {
                alert(d.Message);
            }
        });
    },
    saveRoleScope: function () {
        var _this = this;
        var rIds = _this.getDgChecks('tableRole');
        var query = 'targetUserId=' + (this.obj.ID || this.obj.id) + "&roleIds=" + rIds;
        $.ajaxjson('sss/Admin/FrameworkModules/ResourcePermission/SaveUserRoleScope/', query, function (d) {
            if (d.Data > 0) {
                msg.ok(d.Message);
            } else {
                alert(d.Message);
            }
        });
    },
    saveOrganizeScope: function () {
        var _this = this;
        var orgIds = _this.getTvChecks('tableOrganize');
        var query = 'targetUserId=' + (this.obj.ID || this.obj.id)+ "&organizeIds=" + orgIds;
        $.ajaxjson('sss/Admin/FrameworkModules/ResourcePermission/SaveOrganizeScope/', query, function (d) {
            if (d.Data > 0) {
                msg.ok(d.Message);
            } else {
                alert(d.Message);
            }
        });
    },
    saveModuleScope: function () {
        var _this = this;
        var mIds = _this.getTvChecks('tableModule');
        var query = 'targetUserId=' + (this.obj.ID || this.obj.id) + "&moduleIds=" + mIds;
        $.ajaxjson('sss/Admin/FrameworkModules/ResourcePermission/SaveModuleScope/', query, function (d) {
            if (d.Data > 0) {
                msg.ok(d.Message);
            } else {
                alert(d.Message);
            }
        });
    },
    savePermissionItem: function () {
        var _this = this;
        var pIds = _this.getTvChecks('tablePermissionItem');
        var query = 'targetUserId=' + (this.obj.ID || this.obj.id) + "&permissionItemIds=" + pIds;
        $.ajaxjson('sss/Admin/FrameworkModules/ResourcePermission/SavePermissionItemScope/', query, function (d) {
            if (d.Data > 0) {
                msg.ok(d.Message);
            } else {
                alert(d.Message);
            }
        });
    }
}