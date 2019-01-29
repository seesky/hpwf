var navgrid,
    actionUrl                       = '/Admin/FrameworkModules/PermissionSet/',
    formUrl                         = '/Admin/FrameworkModules/PermissionItemAdmin/Form/?n=' + Math.random(),
    rolePermissionFormUrl           = '/Admin/FrameworkModules/PermissionSet/RolePermissionSet/?n=' + Math.random(),
    roleUserBatchSetUrl             = '/Admin/FrameworkModules/PermissionSet/RoleUserBatchSet/?n=' + Math.random(),
    permissionScopFormUrl           = '/Admin/FrameworkModules/PermissionSet/PermissionScopForm/?n=' + Math.random(),
    roleTableFieldPermissionFormUrl = '/Admin/FrameworkModules/PermissionSet/TableFieldPermission/?n=' + Math.random(),
    firstCheckUser                  = '0',
    firstCheckRole                  = '0',
    firstCheckModule                = '0',
    firstCheckPermissionItem        = '0'; //是否为第一次加载时对相应目标资源权限的Check ，访问加载Check事件

$(function () {   
    $('#toolbar').css({
        height: '30px'
    });   

    $('#sb').splitbutton({
        iconCls: 'icon16_key',
        menu: '#mm'
    });
    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.bindGrid, height: 5 });

    $('#a_refresh').attr('onclick', 'RPAdminMethod.Refreash();'); //刷新
    $('#btnRolePermission').attr('onclick', 'RPAdminMethod.SetRolePermission();');//角色权限设置
    $('#btnRoleUser').attr('onclick', 'RPAdminMethod.SetRoleUser();');//角色角色关联
    $('#btnRoleUserBatchSet').attr('onclick', 'RPAdminMethod.SetRoleUserBatchSet();'); //角色角色集中批量设置
    $('#btnRoleBatchPermission').attr('onclick', 'RPAdminMethod.SetRoleBatchPermission();');//角色权限集中批量设置
    $('#btnRolePermissionScope').attr('onclick', 'RPAdminMethod.SetRolePermissionScope();');//角色授权范围
    $('#btnRoleTableFieldPermission').attr('onclick', 'RPAdminMethod.SetRoleTableFieldPermission();'); //角色表字段权限设置
    $('#btnRoleTableConstraintSet').attr('onclick', 'RPAdminMethod.SetRoleTableConstraintSet();'); //角色约束条件权限设置
    $('#btnSearch').attr('onclick', 'RPAdminMethod.Search();');
});

var mygrid = {
    bindGrid: function (size) {
        navgrid = $('#list').datagrid({
            url: '/Admin/FrameworkModules/RoleAdmin/GridPageListJson/',
            toolbar: '#toolbar',
            width: size.width,
            height: size.height,
            idField: 'ID',
            sortName: 'SORTCODE',
            sortOrder: 'asc',
            singleSelect: true,
            striped: true,
            pagination: true,
            rownumbers: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            pageSize: 20,
            pageList: [20, 10, 30, 50],
            frozenColumns: [[
                { field: 'ck', checkbox: true },
                { title: '编号', field: 'CODE', width: 120 },
                { title: '名称', field: 'REALNAME', width: 150 }
            ]],
            columns: [[
                { title: 'Id', field: 'ID', width: 60, hidden: true },
                { title: '分类', field: 'CATEGORY', width: 130 },
                { title: '有效', field: 'ENABLED', width: 40, align: 'center', formatter: imgcheckbox },
                { title: '允许编辑', field: 'ALLOWEDIT', width: 60, align: 'center', formatter: imgcheckbox },
                { title: '允许删除', field: 'ALLOWDELETE', width: 60, align: 'center', formatter: imgcheckbox },
                { title: '描述', field: 'DESCRIPTION', width: 300 }
            ]]
        });
    },
    reload: function () {
        //navgrid.datagrid('reload');
        navgrid.datagrid('clearSelections').datagrid('reload', { filter: '' });
    },
    selected: function () {
        return navgrid.datagrid('getSelected');
    }
};
var imgcheckbox = function(cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};

var RPAdminMethod = {
    Refreash:function() {
        mygrid.reload();
    },
    Search: function () {
        search.go('list');
    },
    SetRolePermission: function () { //角色权限设置
        var curRole = mygrid.selected();
        if (curRole) {
            var formDialog = top.$.hDialog({
                title: '角色权限设置', width: 660, height: 600, iconCls: 'icon16_molecule',
                href: rolePermissionFormUrl,
                onLoad: function () {
                    top.$('#FormContent').layout('panel', 'center').panel({ title: '当前角色：' + curRole.REALNAME });
                    //1、加载模块（菜单）列表
                    top.$('#tableModule').tree({
                        cascadeCheck: false, //联动选中节点
                        checkbox: true,
                        lines: true,
                        url: '/Admin/FrameworkModules/ModuleAdmin/GetModuleTreeJson/?isTree=1',
                        onBeforeLoad: function (node, param) {
                            top.$.hLoading.show();
                        },
                        onLoadSuccess: function (node, data) {
                            top.$.hLoading.hide();
                            var curRoleModuleIds = [];
                            var query = 'roleId=' + curRole.ID;
                            //1.1、得到当前角色可以访问的模块菜单主键列表
                            $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetModuleByRoleId/', query, function (d) {
                                if (d != '' && d.toString() != '[object XMLDocument]') {
                                    curRoleModuleIds = d.split(',');
                                }
                                if (curRoleModuleIds && curRoleModuleIds.length > 0) {
                                    firstCheckModule = '1';
                                    var moduelTree = top.$('#tableModule');
                                    moduelTree.tree('uncheckedAll');
                                    for (var i = 0; i < curRoleModuleIds.length; i++) {
                                        var tmpnode = moduelTree.tree('find', curRoleModuleIds[i]);
                                        if (tmpnode)
                                            moduelTree.tree("check", tmpnode.target);
                                    }
                                    firstCheckModule = '0';
                                }
                            });
                        },
                        onCheck: function (node, checked) {
                            if (firstCheckModule == '0') {
                                if (checked) { //授予当前角色所选模块的访问权限                                           
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRoleModulePermission/', 'roleId=' + curRole.ID + '&grantIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('授予角色模块访问权限失败！');
                                        }
                                    });
                                } else { //回收当前角色所选模块的访问权限
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRoleModulePermission/', 'roleId=' + curRole.ID + '&revokeIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('收回角色模块访问权限失败！');
                                        }
                                    });
                                }
                            }
                        }
                    });

                    //2、加载框架操作权限项列表。
                    top.$('#tablePermissionItem').tree({
                        cascadeCheck: false, //联动选中节点
                        checkbox: true,
                        lines: true,
                        url: '/Admin/FrameworkModules/PermissionItemAdmin/GetPermissionItemTreeJson/?isTree=1',
                        onBeforeLoad: function (node, param) {
                            top.$.hLoading.show();
                        },
                        onLoadSuccess: function (node, data) {
                            top.$.hLoading.hide();
                            var curRolePermissionItemIds = [];
                            var query = 'roleId=' + curRole.ID;
                            //2.1、得到当前角色可以访问的操作权限主键列表
                            $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetPermissionItemsByRoleId/', query, function (d) {
                                if (d != '' && d.toString() != '[object XMLDocument]') {
                                    curRolePermissionItemIds = d.split(',');
                                }
                                if (curRolePermissionItemIds && curRolePermissionItemIds.length > 0) {
                                    firstCheckPermissionItem = '1';
                                    var permissionItemTree = top.$('#tablePermissionItem');
                                    permissionItemTree.tree('uncheckedAll');
                                    for (var i = 0; i < curRolePermissionItemIds.length; i++) {
                                        var tmpnode = permissionItemTree.tree('find', curRolePermissionItemIds[i]);
                                        if (tmpnode)
                                            permissionItemTree.tree("check", tmpnode.target);
                                    }
                                    firstCheckPermissionItem = '0';
                                }
                            });
                        },
                        onCheck: function (node, checked) {
                            if (firstCheckPermissionItem == '0') {
                                if (checked) { //授予当前角色所选操作权限
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRolePermissionItem/', 'roleId=' + curRole.ID + '&grantIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('授予角色操作权限失败！');
                                        }
                                    });
                                } else {  //回收当前角色所选操作权限
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRolePermissionItem/', 'roleId=' + curRole.ID + '&revokeIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('收回角色操作权限失败！');
                                        }
                                    });
                                }
                            }
                        }
                    });
                },
                submit: function () {
                    formDialog.dialog('close');
                    return false;
                }
            });
        }
        else {
            msg.warning('请选择角色!');
            return false;
        }
        return false;
    },
    SetRoleUser: function () {  //角色用户关联
        var currentRole = mygrid.selected();
        if (currentRole) {
            var rDialog = top.$.hDialog({
                href: '/Admin/FrameworkModules/PermissionSet/RoleUserSet/', width: 600, height: 500, title: '角色用户关联', iconCls: 'icon16_group_link',
                onLoad: function () {
                    top.$('#rlayout').layout();
                    top.$('#roleName').text(currentRole.REALNAME);
                    top.$('#allUsers,#selectedUser').datagrid({
                        width: 255,
                        height: 350,
                        iconCls: 'icon-users',
                        nowrap: false, //折行
                        rownumbers: true, //行号
                        striped: true, //隔行变色
                        idField: 'id', //主键
                        singleSelect: true, //单选
                        columns: [[
                       { title: '登录名', field: 'username', width: 100 },
                       { title: '用户名', field: 'realname', width: 120 }
                   ]],
                        pagination: false,
                        pageSize: 20,
                        pageList: [20, 40, 50]
                    });

                    top.$('#allUsers').datagrid({
                        url: '/Admin/FrameworkModules/UserAdmin/GetUserListJson/',
                        onDblClickRow: function (rowIndex, rowData) {
                            top.$('#aSelectUser').click();
                        }
                    });

                    top.$('#selectedUser').datagrid({
                        url: '/Admin/FrameworkModules/UserAdmin/GetDTByRole/?roleId=' + currentRole.ID,
                        onDblClickRow: function (rowIndex, rowData) {
                            top.$('#aDeleteUser').click();
                        }
                    });
                    top.$('#aSelectUser').click(function () {
                        var _row = top.$('#allUsers').datagrid('getSelected');
                        if (_row) {
                            var hasUserName = false;
                            var users = top.$('#selectedUser').datagrid('getRows');
                            $.each(users, function (i, n) {
                                if (n.username == _row.username) {
                                    hasUserName = true;
                                }
                            });
                            if (!hasUserName) {
                                top.$('#selectedUser').datagrid('appendRow', _row);
                                //添加用户
                                var query = 'targetIds=' + currentRole.ID + '&userId=' + _row.id;
                                $.ajaxjson('/Admin/FrameworkModules/PermissionSet/AddUserToRole/', query, function (d) {
                                    if (d.Data != '1') {
                                        msg.ok('添加用户失败。');
                                    }
                                });
                            }
                            else {
                                top.$.messager.alert("操作提示", "用户已存在，请不要重复添加。", "warning");
                                return false;
                            }
                        } else {
                            top.$.messager.alert("操作提示", "请选择用户!", "warning");
                        }
                        return false;
                    });
                    top.$('#aDeleteUser').click(function () {
                        var trow = top.$('#selectedUser').datagrid('getSelected');
                        if (trow) {
                            var rIndex = top.$('#selectedUser').datagrid('getRowIndex', trow);
                            top.$('#selectedUser').datagrid('deleteRow', rIndex).datagrid('unselectAll');
                            //移除角色
                            var query = 'targetIds=' + currentRole.ID + '&userId=' + trow.id;
                            $.ajaxjson('/Admin/FrameworkModules/PermissionSet/RemoveUserFromRole/', query, function (d) {
                                if (d != '1') {
                                    msg.ok('移除用户失败。');
                                }
                            });
                        } else {
                            top.$.messager.alert("操作提示", "请选择用户!", "warning");
                        }
                    });
                },
                submit: function () {
                    rDialog.dialog('close');
                }
            });
        } else {
            msg.warning('请选择一个角色哦！');
        }
        return false;
    },
    SetRoleUserBatchSet: function () {  //角色用户集中批量设置
        var formDialog = top.$.hDialog({
            title: '角色用户集中批量设置', width: 560, height: 600, iconCls: 'icon16_folder_user',
            href: roleUserBatchSetUrl,
            onLoad: function () {
                top.$('#FormContent').layout('panel', 'center').panel({ title: '' });
                top.$('#tableRole,#tableUser').datagrid({
                    idField: 'id',
                    sortName: 'sortcode',
                    sortOrder: 'asc',
                    nowrap: false, //折行                   
                    rownumbers: false, //行号
                    striped: true, //隔行变色         
                    pagination: false,
                    showHeader: false,
                    pageSize: 20,
                    pageList: [20, 40, 50]
                });

                top.$('#tableRole').datagrid({
                    url: '/Admin/FrameworkModules/RoleAdmin/GetRoleList/',
                    singleSelect: true, //单选 
                    columns: [[
                    //{ title: '编码', field: 'CODE', width: 100 },
			           {title: '角色名称', field: 'realname', width: 190 }
		            ]],
                    onSelect: function (rowIndex, rowData) {
                        if (rowData) {
                            //1、加载当前角色所拥有的用户                            
                            $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetRoleUserIds/', 'roleId=' + (rowData.ID || rowData.id), function (data) {
                                firstCheckUser = "1";
                                top.$('#tableUser').datagrid('uncheckAll'); //取消所有选中行
                                if (data != '' && data.toString() != '[object XMLDocument]') {
                                    var curRoleUserIds = data.split(',');
                                    for (var i = 0; i < curRoleUserIds.length; i++) {
                                        var rowidx = top.$('#tableUser').datagrid('getRowIndex', curRoleUserIds[i]);
                                        if (rowidx >= 0) {
                                            top.$('#tableUser').datagrid('checkRow', rowidx);
                                        }
                                    }
                                }
                                firstCheckUser = "0";
                            });
                        }
                    }
                });

                top.$('#tableUser').datagrid({
                    url: '/Admin/FrameworkModules/UserAdmin/GetUserListJson/',
                    columns: [[
                       { title: 'id', field: 'id', width: 30, align: 'left', checkbox: true },
			           { title: '登录名', field: 'username', width: 100, align: 'left' },
                       { title: '名称', field: 'realname', width: 120, align: 'left' }
		            ]],
                    onCheck: function (rowIndex, rowData) { //当前角色的用户赋予
                        var currentRole = top.$('#tableRole').datagrid('getSelected');
                        if (firstCheckUser != '1' && currentRole) {
                            var query = 'roleId=' + currentRole.id + '&targetIds=' + (rowData.ID || rowData.id);
                            $.ajaxjson('/Admin/FrameworkModules/PermissionSet/AddRoleUser/', query, function (d) {
                                if (d.Data != '1') {
                                    msg.warning('授予用户失败！');
                                }
                            });
                        }
                    }, //end of onCheck
                    onUncheck: function (rowIndex, rowData) { //当前角色的用户收回
                        var currentRole = top.$('#tableRole').datagrid('getSelected');
                        if (firstCheckUser != '1' && currentRole) {
                            var query = 'roleId=' + currentRole.id + '&targetIds=' + (rowData.ID || rowData.id);
                            $.ajaxjson('/Admin/FrameworkModules/PermissionSet/RemoveRoleUser/', query, function (d) {
                                if (d.Data != '1') {
                                    msg.warning('回收用户失败！');
                                }
                            });
                        }
                    } //end of onUncheck
                });
            },
            submit: function () {
                formDialog.dialog('close');
                return false;
            }
        });
        return false;
    },
    SetRoleBatchPermission: function () {  //角色权限批量设置
        var batchPermissionDialog = top.$.hDialog({
            href: '/Admin/FrameworkModules/PermissionSet/RolePermissionBatchSet/', width: 1100, height: 630, title: '角色权限批量设置', iconCls: 'icon16_shape_square_key',
            onLoad: function () {
                top.$('#FormContent').layout('panel', 'center').panel({ title: '' });
                //1、绑定界面控件
                //1.1、绑定角色列表与用户列表
                top.$('#tableRole,#tableUser').datagrid({
                    width: 180,
                    height: 390,
                    iconCls: 'icon16_group',
                    loadMsg: "数据加载中...",
                    idField: 'id',
                    sortName: 'sortcode',
                    sortOrder: 'asc',
                    nowrap: false, //折行                   
                    rownumbers: false, //行号
                    striped: true, //隔行变色         
                    pagination: false,
                    showHeader: false,
                    pageSize: 20,
                    pageList: [20, 40, 50]
                });

                top.$('#tableRole').datagrid({
                    url: '/Admin/FrameworkModules/RoleAdmin/GetRoleList/',
                    singleSelect: true, //单选 
                    columns: [[
                    //{ title: '编码', field: 'CODE', width: 100 },
			           {title: '角色名称', field: 'realname', width: 155 }
		            ]],
                    onSelect: function (rowIndex, rowData) {
                        if (rowData) {
                            //1.2、加载当前角色所拥有的目标资源权限  
                            //1.2.1、加载当前角色所拥有的用户                        
                            $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetRoleUserIds/', 'roleId=' + (rowData.ID || rowData.id), function (data) {
                                firstCheckUser = "1";
                                top.$('#tableUser').datagrid('uncheckAll'); //取消所有选中行
                                if (data != '' && data.toString() != '[object XMLDocument]') {
                                    var curRoleUserIds = data.split(',');
                                    for (var i = 0; i < curRoleUserIds.length; i++) {
                                        var rowidx = top.$('#tableUser').datagrid('getRowIndex', curRoleUserIds[i]);
                                        if (rowidx >= 0) {
                                            top.$('#tableUser').datagrid('checkRow', rowidx);
                                        }
                                    }
                                }
                                firstCheckUser = "0";
                            });

                            //1.2.2、绑定当前角色已经拥有的模块（菜单）访问权限。
                            var curUserModuleIds = [];
                            var tmpquery = 'roleId=' + (rowData.ID || rowData.id);
                            $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetModuleByRoleId/', tmpquery, function (data) {
                                firstCheckModule = '1';
                                var moduelTree = top.$('#tableModule');
                                moduelTree.tree('uncheckedAll');
                                if (data != '' && data.toString() != '[object XMLDocument]') {
                                    curUserModuleIds = data.split(',');
                                }
                                if (curUserModuleIds && curUserModuleIds.length > 0) {
                                    for (var i = 0; i < curUserModuleIds.length; i++) {
                                        var node = moduelTree.tree('find', curUserModuleIds[i]);
                                        if (node)
                                            moduelTree.tree("check", node.target);
                                    }                                    
                                }

                                firstCheckModule = '0';
                            });

                            //1.2.3、绑定当前角色已经拥有的操作权限
                            var curUserPermissionItemIds = [];
                            var query = 'roleId=' + (rowData.ID || rowData.id);
                            $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetPermissionItemsByRoleId/', query, function (data) {
                                firstCheckPermissionItem = '1';
                                var permissionItemTree = top.$('#tablePermissionItem');
                                permissionItemTree.tree('uncheckedAll');
                                if (data != '' && data.toString() != '[object XMLDocument]') {
                                    curUserPermissionItemIds = data.split(',');
                                }
                                if (curUserPermissionItemIds && curUserPermissionItemIds.length > 0) {

                                    for (var i = 0; i < curUserPermissionItemIds.length; i++) {
                                        var node = permissionItemTree.tree('find', curUserPermissionItemIds[i]);
                                        if (node)
                                            permissionItemTree.tree("check", node.target);
                                    }

                                }
                                firstCheckPermissionItem = '0';
                            });
                        }
                    }
                });

                //绑定用户
                top.$('#tableUser').datagrid({
                    url: '/Admin/FrameworkModules/UserAdmin/GetUserListJson/',
                    columns: [[
                       { title: 'Id', field: 'id', width: 30, align: 'left', checkbox: true },
                       { title: '名称', field: 'realname', width: 125, align: 'left' }
		            ]],
                    onCheck: function (rowIndex, rowData) { //当前角色的用户赋予
                        var currentRole = top.$('#tableRole').datagrid('getSelected');
                        if (firstCheckUser != '1' && currentRole) {
                            var query = 'roleId=' + (currentRole.ID || currentRole.id) + '&targetIds=' + (rowData.ID || rowData.id);
                            $.ajaxjson('/Admin/FrameworkModules/PermissionSet/AddRoleUser/', query, function (d) {
                                if (d.Data != '1') {
                                    msg.warning('授予用户失败！');
                                }
                            });
                        }
                    }, //end of onCheck
                    onUncheck: function (rowIndex, rowData) { //当前角色的用户收回
                        var currentRole = top.$('#tableRole').datagrid('getSelected');
                        if (firstCheckUser != '1' && currentRole) {
                            var query = 'roleId=' + (currentRole.ID || currentRole.id) + '&targetIds=' + (rowData.ID || rowData.id);
                            $.ajaxjson('/Admin/FrameworkModules/PermissionSet/RemoveRoleUser/', query, function (d) {
                                if (d.Data != '1') {
                                    msg.warning('回收用户失败！');
                                }
                            });
                        }
                    } //end of onUncheck
                });

                //1.3、绑定模块（菜单）列表
                top.$('#tableModule,#tablePermissionItem').tree({
                    cascadeCheck: false, //联动选中节点
                    checkbox: true,
                    lines: true
                });

                top.$('#tableModule').tree({
                    url: '/Admin/FrameworkModules/ModuleAdmin/GetModuleTreeJson/?isTree=1',
                    onCheck: function (node, checked) {
                        var curRole = top.$('#tableRole').datagrid('getSelected');
                        if (curRole) {
                            if (firstCheckModule == '0') {
                                if (checked) { //1.3.1、授予当前角色所选模块的访问权限                                           
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRoleModulePermission/', 'roleId=' + (curRole.ID || curRole.id) + '&grantIds=' + (node.id || node.ID), function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('授予角色模块访问权限失败！');
                                        }
                                    });
                                } else { //1.3.2、回收当前角色所选模块的访问权限
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRoleModulePermission/', 'roleId=' + (curRole.ID || curRole.id) + '&revokeIds=' + (node.id || node.ID), function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('收回角色模块访问权限失败！');
                                        }
                                    });
                                }
                            }
                        } else {
                            msg.warning('请选择一个角色。');
                        }
                    }
                });
                //1.4、绑定操作权限项列表
                top.$('#tablePermissionItem').tree({
                    url: '/Admin/FrameworkModules/PermissionItemAdmin/GetPermissionItemTreeJson/?isTree=1',
                    onCheck: function (node, checked) {
                        var curRole = top.$('#tableRole').datagrid('getSelected');
                        if (curRole) {
                            if (firstCheckPermissionItem == '0') {
                                if (checked) { //1.4.1、授予当前角色所选操作权限
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRolePermissionItem/', 'roleId=' + (curRole.ID || curRole.id) + '&grantIds=' + (node.id || node.ID), function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('授予角色操作权限失败！');
                                        }
                                    });
                                } else {  //1.4.2、回收当前角色所选操作权限
                                    $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRolePermissionItem/', 'roleId=' + (curRole.ID || curRole.id) + '&revokeIds=' + (node.id || node.ID), function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('收回角色操作权限失败！');
                                        }
                                    });
                                }
                            }
                        } else {
                            msg.warning('请选择一个角色。');
                        }
                    }
                });
            },
            submit: function () {
                batchPermissionDialog.dialog('close');
                return false;
            }
        });
        return false;
    },
    SetRolePermissionScope: function () {  //角色授权范围
        var currentRole = mygrid.selected(),
        rp = new RolePermissionScope(currentRole, permissionScopFormUrl);
        rp.show();
        return false;
    },
    SetRoleTableFieldPermission: function () {  //角色表字段权限设置
        var currentTableFieldPermissionUser = mygrid.selected();
        if (currentTableFieldPermissionUser) {
            var formDialog = top.$.hDialog({
                title: '表字段权限设置', width: 740, height: 588, iconCls: 'icon16_timeline_marker',
                href: roleTableFieldPermissionFormUrl,
                buttons: [{
                    text: '关闭',
                    iconCls: 'icon16_cancel',
                    handler: function () {
                        formDialog.dialog("close");
                    }
                }],
                onLoad: function () {
                    top.$('#FormContent').layout('panel', 'center').panel({ title: '当前资源：' + currentTableFieldPermissionUser.REALNAME });
                    top.$('#tableList').datagrid({
                        url: '/Admin/FrameworkModules/PermissionSet/GetAllTableScope/?resourceCategory=PIROLE&resourceId=' + currentTableFieldPermissionUser.ID,
                        idField: 'ID',
                        sortName: 'SORTCODE',
                        sortOrder: 'asc',
                        showHeader: false,
                        singleSelect: true,
                        selectOnCheck: false,
                        checkOnSelect: false,
                        pagination: false,
                        rownumbers: true,
                        columns: [[
                           //{ field: 'ck', checkbox: true },
                           {
                           field: 'PermissionValue', title: '权限', width: 25, align: 'center',
                           formatter: function (value, rowData, rowIndex) {
                               return '<img style="cursor:pointer" onclick="permissionTableSet(' + "'PIROLE'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + rowData.ITEMVALUE + "'" + ',' + value + ')"  src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                           }
                           },
                            { title: '值', field: 'ITEMVALUE', width: 100, align: 'left' },
                            { title: '表名', field: 'ITEMNAME', width: 110, align: 'left', hidden: true }
                        ]],
                        onClickRow: function (rowIndex, rowData) {
                            var cc = rowData.ITEMVALUE;
                            top.$('#tableFiledList').datagrid({
                                url: '/Admin/FrameworkModules/PermissionSet/GetDTByTable/',
                                queryParams: { tableName: cc, resourceCategory: 'PIROLE', resourceId: currentTableFieldPermissionUser.ID }
                            });
                        }
                    });

                    top.$('#tableFiledList').datagrid({
                        loadMsg: "正在加载表明细，请稍等...",
                        nowrap: false, rownumbers: true, striped: true, selectOnCheck: false, checkOnSelect: false,
                        singleSelect: true,
                        showHeader: true,
                        idField: 'ID',
                        frozenColumns: [[]],
                        columns: [[
                            { title: 'ID', field: 'ID', width: 10, align: 'left', hidden: true },
                            { title: '字段名称', field: 'COLUMNCODE', width: 140, align: 'left' },
                            {
                                field: 'ISPUBLIC', title: '公共', width: 30, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'ISPUBLIC'" + ',' + "'PIROLE'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')"  src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                                }
                            },
                            {
                                field: 'COLUMNACCESS', title: '列访问权限', width: 80, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'COLUMNACCESS'" + ',' + "'PIROLE'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')" src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                                }
                            },
                            {
                                field: 'COLUMNEDIT', title: '列编辑权限', width: 80, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'COLUMNEDIT'" + ',' + "'PIROLE'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')" src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                                }
                            },
                            {
                                field: 'COLUMNDENEY', title: '列拒绝访问', width: 80, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'COLUMNDENEY'" + ',' + "'PIROLE'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')" src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                                }
                            }
                        ]],
                        onLoadSuccess: function (data) {
                            top.$('#tableFiledList').datagrid('selectRow', 0);
                        }
                    });
                }
            });
        } else {
            msg.warning('请选择一个角色哦！');
        }
        return false;
    },
    SetRoleTableConstraintSet: function () {  //角色约束条件权限设置
        //功能代码逻辑...
        var currentRoleTableConstraint = mygrid.selected();
        if (currentRoleTableConstraint) {
            var tmpSetRoleTableConstraintDialog = top.$.hDialog({
                content: '<div id="tmpGridList"></div>',
                width: 600, height: 500,
                title: '表约束条件设置-当前角色：' + currentRoleTableConstraint.REALNAME,
                iconCls: 'icon16_script_key',
                buttons: [{
                    text: '关闭',
                    iconCls: 'icon16_cancel',
                    handler: function () {
                        tmpSetRoleTableConstraintDialog.dialog("close");
                    }
                }],
                onOpen: function () {
                    top.$('#tmpGridList').datagrid({
                        url: '/Admin/FrameworkModules/PermissionSet/GetConstraintDT/?resourceCategory=PIROLE&resourceId=' + currentRoleTableConstraint.ID,
                        singleSelect: true,
                        selectOnCheck: true,
                        checkOnSelect: true,
                        width: 560,
                        height: 400,
                        idField: 'ID',
                        sortName: 'TABLECODE',
                        sortOrder: 'asc',
                        pagination: false,
                        rownumbers: true,
                        toolbar: [{
                            id: 'btnSetContraint',
                            text: '设置条件表达式',
                            iconCls: 'icon-script_add',
                            handler: function () {
                                var tmpUserTableConstraintGridRow = top.$('#tmpGridList').datagrid('getSelected');
                                if (tmpUserTableConstraintGridRow) {
                                    var tmpSetContraintDialog = top.$.hDialog({//设置约束条件式
                                        content: '<textarea  id="txtContraint" name="Contraint" rows="5" style="width:430px;height:80px;" class="txt03">',
                                        width: 470,
                                        height: 180,
                                        title: '设置约束条件',
                                        iconCls: 'icon-script_add',
                                        submit: function () {
                                            if (top.$('#txtContraint').val()) {
                                                var tmpParam = 'resourceCategory=PIROLE&resourceId=' + currentRoleTableConstraint.ID + '&tableName=' + tmpUserTableConstraintGridRow.TABLECODE + '&tableConstraint=' + top.$('#txtContraint').val();
                                                $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetConstraint/', tmpParam, function (d) {
                                                    if (d.Data > 0) {
                                                        msg.ok('设置成功！');
                                                        top.$('#tmpGridList').datagrid('reload');
                                                    } else {
                                                        MessageOrRedirect(d);
                                                    }
                                                });
                                                tmpSetContraintDialog.dialog('close');
                                            } else {
                                                msg.warning('条件表达式不能为空！');
                                            }
                                            return false;
                                        }
                                    });
                                } else {
                                    msg.warning('无选择的数据！');
                                }
                            }
                        }, "-", {
                            id: 'btnDelContraint',
                            text: '删除条件表达式',
                            iconCls: 'icon-script_delete',
                            handler: function () {
                                var tmpRoleTableConstraintGridRow = top.$('#tmpGridList').datagrid('getSelected');
                                if (tmpRoleTableConstraintGridRow && tmpRoleTableConstraintGridRow.PERMISSIONCONSTRAINT != null) {
                                    top.$.messager.confirm('询问提示', '确定要删除【' + tmpRoleTableConstraintGridRow.TABLENAME + '】的约束条件吗？', function (data) {
                                        if (data) {
                                            $.ajaxjson('/Admin/FrameworkModules/PermissionSet/DeleteConstraint/', 'keyId=' + tmpRoleTableConstraintGridRow.ID, function (d) {
                                                if (d.Data > 0) {
                                                    msg.ok('删除成功！');
                                                    top.$('#tmpGridList').datagrid('reload');
                                                } else {
                                                    MessageOrRedirect(d);
                                                }
                                            });
                                        }
                                    });
                                } else {
                                    msg.warning('无选择的数据，或所选数据没有设置条件表达式！');
                                }
                            }
                        }],
                        columns: [[
                                { field: 'ck', checkbox: true },
                                { title: '表', field: 'TABLECODE', width: 150, sortable: true },
                                { title: '名称', field: 'TABLENAME', width: 150 },
                                { title: '约束条件', field: 'PERMISSIONCONSTRAINT', width: 200 }
                            ]]
                    });
                }
            });
        } else {
            msg.warning('请选择一个角色哦！');
        }
        return false;
    }
};