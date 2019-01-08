var navgrid,
    actionUrl                       = '/FrameworkModules/UserPermissionAdmin',
    userPermissionFormUrl           = '/FrameworkModules/PermissionSet/UserPermissionSet?n=' + Math.random(),
    userRoleBatchSetUrl             = '/FrameworkModules/PermissionSet/UserRoleBatchSet?n=' + Math.random(),
    permissionScopFormUrl           = '/FrameworkModules/PermissionSet/PermissionScopForm?n=' + Math.random(),
    userTableFieldPermissionFormUrl = '/FrameworkModules/PermissionSet/TableFieldPermission?n=' + Math.random(),
    firstCheckRole                  = '0',
    firstCheckModule                = '0',
    firstCheckPermissionItem        = '0'; //是否为第一次加载时对相应目标资源权限的Check ，访问加载Check事件。

$(function () {
    $('#toolbar').css({
        height: '30px'
    });

    $('#sb').splitbutton({
        iconCls: 'icon16_key',
        menu: '#mm'
    });

    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.bindGrid, height: 5 });
    
    $('#a_refresh').attr('onclick', 'UPAdminMethod.Refreash();');
    $('#btnUserPermission').attr('onclick', 'UPAdminMethod.SetUserPermission();'); //用户权限设置
    $('#btnUserRole').attr('onclick', 'UPAdminMethod.SetUserRole();'); //用户角色关联
    $('#btnUserRoleBatchSet').attr('onclick', 'UPAdminMethod.SetUserRoleBatchSet();');//用户角色集中批量设置
    $('#btnUserBatchPermission').attr('onclick', 'UPAdminMethod.SetUserBatchPermission();');//用户权限集中批量设置
    $('#btnUserPermissionScope').attr('onclick', 'UPAdminMethod.SetUserPermissionScope();'); //用户授权范围
    $('#btnUserTableFieldPermission').attr('onclick', 'UPAdminMethod.SetUserTableFieldPermission();'); //用户表字段权限设置
    $('#btnUserTableConstraintSet').attr('onclick', 'UPAdminMethod.SetUserTableConstraintSet();');//用户约束条件权限设置
    $('#btnSearch').attr('onclick', 'UPAdminMethod.Search();');
});

var mygrid = {
    bindGrid: function (size) {
        navgrid = $('#list').datagrid({
            url: '/FrameworkModules/UserAdmin/GetUserListByPage',
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
                { title: '登录名', field: 'USERNAME', width: 120 },
                { title: '用户名', field: 'REALNAME', width: 150 }
            ]],
            columns: [[
                { title: 'Id', field: 'ID', width: 60, hidden: true },
                { title: '部门', field: 'DEPARTMENTNAME', width: 130 },
                { title: '有效', field: 'ENABLED', width: 40, align: 'center', formatter: imgcheckbox },
                { title: '邮箱地址', field: 'EMAIL', width: 150 },
                { title: '手机号码', field: 'MOBILE', width: 100 },
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
var imgcheckbox = function (cellvalue, options, rowObject) {
    return cellvalue ? '<img src="../../Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="../../Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};
var UPAdminMethod = {
    Refreash:function() {
        mygrid.reload();
    },
    Search:function() {
        search.go('list');
    },
    SetUserPermission: function () { //用户权限设置
        var curUser = mygrid.selected();
        if (curUser) {
            var formDialog = top.$.hDialog({
                title: '用户权限设置', width: 880, height: 600, iconCls: 'icon16_key',
                href: userPermissionFormUrl,
                onLoad: function () {
                    top.$('#FormContent').layout('panel', 'center').panel({ title: '当前用户：' + curUser.REALNAME });
                    var roleGrid = top.$('#tableRole').datagrid;
                    top.$('#tableRole').datagrid({
                        url: '/FrameworkModules/RoleAdmin/GetRoleList',
                        nowrap: false, //折行                   
                        rownumbers: false, //行号
                        striped: true, //隔行变色
                        checkOnSelect: false,
                        idField: 'ID', //主键
                        singleSelect: false, //多选  
                        showHeader: false,
                        frozenColumns: [[]],
                        columns: [[
                           { title: 'Id', field: 'ID', width: 30, align: 'left', checkbox: true },
                           { title: '角色名称', field: 'REALNAME', width: 150, align: 'left' }
                        ]],
                        onLoadSuccess: function (data) {
                            //1、加载当前用户所拥有的角色
                            top.$('#tableRole').datagrid('uncheckAll'); //取消所有选中行
                            $.ajaxtext('/FrameworkModules/PermissionSet/GetUserRoleIds', 'userId=' + curUser.ID, function (returndata) {
                                if (returndata != '' && returndata.toString() != '[object XMLDocument]') {
                                    var curUserRoleIds = returndata.split(',');
                                    for (var i = 0; i < curUserRoleIds.length; i++) {
                                        var rowidx = top.$('#tableRole').datagrid('getRowIndex', curUserRoleIds[i]);
                                        if (rowidx) {
                                            top.$('#tableRole').datagrid('checkRow', rowidx);
                                        }
                                    }
                                }
                            });
                            //2、加载框架模块（菜单）列表                       
                            top.$('#tableModule').tree({
                                cascadeCheck: false, //联动选中节点
                                checkbox: true,
                                lines: true,
                                url: '/FrameworkModules/ModuleAdmin/GetModuleTreeJson?isTree=1',
                                onBeforeLoad: function (node, param) {
                                    top.$.hLoading.show();
                                },
                                onLoadSuccess: function (node, data) {
                                    top.$.hLoading.hide();
                                    //2.1、绑定当前用户已经拥有的模块（菜单）访问权限。
                                    var curUserModuleIds = [];
                                    var query = 'userId=' + curUser.ID;
                                    $.ajaxtext('/FrameworkModules/PermissionSet/GetModuleByUserId', query, function (returndata) {
                                        if (returndata != '' && returndata.toString() != '[object XMLDocument]') {
                                            curUserModuleIds = returndata.split(',');
                                        }
                                        if (curUserModuleIds && curUserModuleIds.length > 0) {
                                            firstCheckModule = '1';
                                            var moduelTree = top.$('#tableModule');
                                            moduelTree.tree('uncheckedAll');
                                            for (var i = 0; i < curUserModuleIds.length; i++) {
                                                var tmpnode = moduelTree.tree('find', curUserModuleIds[i]);
                                                if (tmpnode)
                                                    moduelTree.tree("check", tmpnode.target);
                                            }
                                            firstCheckModule = '0';
                                        }
                                    });
                                },
                                onCheck: function (node, checked) {
                                    if (firstCheckModule == '0') {
                                        if (checked) { //授予当前用户所选模块的访问权限                                           
                                            $.ajaxjson('/FrameworkModules/PermissionSet/SetUserModulePermission', 'userId=' + curUser.ID + '&grantIds=' + node.id, function (d) {
                                                if (d.Data != '1') {
                                                    msg.warning('授予用户模块访问权限失败！');
                                                }
                                            });
                                        } else { //回收当前用户所选模块的访问权限
                                            $.ajaxjson('/FrameworkModules/PermissionSet/SetUserModulePermission', 'userId=' + curUser.ID + '&revokeIds=' + node.id, function (d) {
                                                if (d.Data != '1') {
                                                    msg.warning('收回用户模块访问权限失败！');
                                                }
                                            });
                                        }
                                    }
                                }
                            });

                            //3、加载框架操作权限项列表。
                            top.$('#tablePermissionItem').tree({
                                cascadeCheck: false, //联动选中节点
                                checkbox: true,
                                lines: true,
                                url: '/FrameworkModules/PermissionItemAdmin/GetPermissionItemTreeJson?isTree=1',
                                onBeforeLoad: function (node, param) {
                                    top.$.hLoading.show();
                                },
                                onLoadSuccess: function (node, data) {
                                    top.$.hLoading.hide();
                                    //3.1、绑定当前用户已经拥有的操作权限
                                    var curUserPermissionItemIds = [];
                                    var query = 'userId=' + curUser.ID;
                                    $.ajaxtext('/FrameworkModules/PermissionSet/GetPermissionItemsByUserId', query, function (d) {
                                        if (d != '' && d.toString() != '[object XMLDocument]') {
                                            curUserPermissionItemIds = d.split(',');
                                        }
                                        if (curUserPermissionItemIds && curUserPermissionItemIds.length > 0) {
                                            firstCheckPermissionItem = '1';
                                            var permissionItemTree = top.$('#tablePermissionItem');
                                            permissionItemTree.tree('uncheckedAll');
                                            for (var i = 0; i < curUserPermissionItemIds.length; i++) {
                                                var tmpnode = permissionItemTree.tree('find', curUserPermissionItemIds[i]);
                                                if (tmpnode)
                                                    permissionItemTree.tree("check", tmpnode.target);
                                            }
                                            firstCheckPermissionItem = '0';
                                        }
                                    });
                                },
                                onCheck: function (node, checked) {
                                    if (firstCheckPermissionItem == '0') {
                                        if (checked) { //授予当前用户所选操作权限
                                            $.ajaxjson('/FrameworkModules/PermissionSet/SetUserPermissionItem', 'userId=' + curUser.ID + '&grantIds=' + node.id, function (d) {
                                                if (d.Data != '1') {
                                                    msg.warning('授予用户操作权限失败！');
                                                }
                                            });
                                        } else {  //回收当前用户所选操作权限
                                            $.ajaxjson('/FrameworkModules/PermissionSet/SetUserPermissionItem', 'userId=' + curUser.ID + '&revokeIds=' + node.id, function (d) {
                                                if (d.Data != '1') {
                                                    msg.warning('收回用户操作权限失败！');
                                                }
                                            });
                                        }
                                    }
                                }
                            });

                        }, //end of  onLoadSuccess
                        onCheck: function (rowIndex, rowData) { //当前用户角色的赋予
                            if (firstCheckRole != '1') {
                                var query = 'userId=' + curUser.ID + '&targetIds=' + rowData.ID;
                                $.ajaxjson('/FrameworkModules/PermissionSet/AddUserToRole', query, function (d) {
                                    if (d.Data != '1') {
                                        msg.warning('授予角色失败！');
                                    }
                                });
                            }
                        }, //end of onCheck
                        onUncheck: function (rowIndex, rowData) { //当前用户角色的收回
                            if (firstCheckRole != '1') {
                                var query = 'userId=' + curUser.ID + '&targetIds=' + rowData.ID;
                                $.ajaxjson('/FrameworkModules/PermissionSet/RemoveUserFromRole', query, function (d) {
                                    if (d.Data != '1') {
                                        msg.warning('回收角色失败！');
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
        }
        else {
            msg.warning('请选择用户!');
            return false;
        }
        return false;
    },
    SetUserRole: function () {  //用户角色关联
        var currentUser = mygrid.selected();
        if (currentUser) {
            var rDialog = top.$.hDialog({
                href: '/FrameworkModules/PermissionSet/UserRoleSet', width: 600, height: 500, title: '用户角色关联', iconCls: 'icon16_group_link',
                onLoad: function () {
                    top.$('#rlayout').layout();
                    top.$('#uname').text(currentUser.REALNAME);
                    top.$('#allRoles,#selectedRoles').datagrid({
                        width: 200,
                        height: 350,
                        iconCls: 'icon16_group',
                        nowrap: false, //折行
                        rownumbers: true, //行号
                        striped: true, //隔行变色
                        idField: 'ID', //主键
                        singleSelect: true, //单选
                        columns: [[
                       { title: '角色名称', field: 'REALNAME', width: 160 },
                       { title: '描述', field: 'DESCRIPTION', width: 210, hidden: true }
                   ]],
                        pagination: false,
                        pageSize: 20,
                        pageList: [20, 40, 50]
                    });

                    top.$('#allRoles').datagrid({
                        url: '/FrameworkModules/RoleAdmin/GetRoleList',
                        onDblClickRow: function (rowIndex, rowData) {
                            top.$('#aSelectRole').click();
                        }
                    });

                    top.$('#selectedRoles').datagrid({
                        url: '/FrameworkModules/RoleAdmin/GetRoleListByUserId?userId=' + currentUser.ID,
                        onDblClickRow: function (rowIndex, rowData) {
                            //top.$('#selectedRoles').datagrid('deleteRow', rowIndex);
                            top.$('#aDeleteRole').click();
                        }
                    });
                    top.$('#aSelectRole').click(function () {
                        var _row = top.$('#allRoles').datagrid('getSelected');
                        if (_row) {
                            var hasRealName = false;
                            var roles = top.$('#selectedRoles').datagrid('getRows');
                            $.each(roles, function (i, n) {
                                if (n.REALNAME == _row.REALNAME) {
                                    hasRealName = true;
                                }
                            });
                            if (!hasRealName) {
                                top.$('#selectedRoles').datagrid('appendRow', _row);
                                //添加角色
                                var query = 'userId=' + currentUser.ID + '&targetIds=' + _row.ID;
                                $.ajaxjson('/FrameworkModules/PermissionSet/AddUserToRole', query, function (d) {
                                    if (d.Data != "1") {
                                        msg.ok('添加角色失败。');
                                    }
                                });
                            }
                            else {
                                alert('角色已存在，请不要重复添加。');
                                return false;
                            }
                        } else {
                            alert('请选择角色');
                        }
                        return false;
                    });
                    top.$('#aDeleteRole').click(function () {
                        var trow = top.$('#selectedRoles').datagrid('getSelected');
                        if (trow) {
                            var rIndex = top.$('#selectedRoles').datagrid('getRowIndex', trow);
                            top.$('#selectedRoles').datagrid('deleteRow', rIndex).datagrid('unselectAll');
                            //移除角色
                            var query = 'userId=' + currentUser.ID + '&targetIds=' + trow.ID;
                            $.ajaxjson('/FrameworkModules/UserAdmin/RemoveRoleByUserId', query, function (d) {
                                if (d.Data != "1") {
                                    msg.ok('移除角色失败。');
                                }
                            });
                        } else {
                            alert('请选择角色');
                        }
                    });
                },
                submit: function () {
                    rDialog.dialog('close');
                }
            });
        } else {
            msg.warning('请选择一个用户哦！');
        }
        return false;
    },
    SetUserRoleBatchSet: function () {  //用户角色集中批量设置
        var formDialog = top.$.hDialog({
            title: '用户角色集中批量设置', width: 560, height: 600, iconCls: 'icon16_shape_square_key',
            href: userRoleBatchSetUrl,
            onLoad: function () {
                top.$('#FormContent').layout('panel', 'center').panel({ title: '' });
                navgrid = top.$('#tableUser').datagrid({
                    url: '/FrameworkModules/UserAdmin/GetUserListByPage',
                    idField: 'ID',
                    sortName: 'SORTCODE',
                    sortOrder: 'asc',
                    nowrap: false, //折行                   
                    striped: true, //隔行变色             
                    singleSelect: true, //多选  
                    showHeader: true,
                    pagination: true,
                    //pagePosition:'top',
                    rownumbers: true,
                    pageSize: 20,
                    pageList: [20, 10, 30, 50],
                    frozenColumns: [[]],
                    columns: [[
                           { title: 'Id', field: 'ID', width: 30, align: 'left', hidden: true },
                           { title: '登录名', field: 'USERNAME', width: 100, align: 'left' },
                           { title: '名称', field: 'REALNAME', width: 120, align: 'left' }
                        ]],
                    onLoadSuccess: function (data) {
                        top.$('#tableUser').datagrid('getPager').data("pagination").options.displayMsg = '';
                        //1、加载当前用户所拥有的角色
                        var roleGrid = top.$('#tableRole').datagrid;
                        top.$('#tableRole').datagrid({
                            url: '/FrameworkModules/RoleAdmin/GetRoleList',
                            nowrap: false, //折行                   
                            rownumbers: false, //行号
                            striped: true, //隔行变色
                            checkOnSelect: false,
                            idField: 'ID', //主键
                            singleSelect: false, //多选  
                            showHeader: false,
                            frozenColumns: [[]],
                            columns: [[
                               { title: 'Id', field: 'ID', width: 30, align: 'left', checkbox: true },
                               { title: '角色名称', field: 'REALNAME', width: 150, align: 'left' }
                            ]],
                            onLoadSuccess: function (data) {
                                top.$('#tableUser').datagrid('selectRow', 0);
                            }, //end of  onLoadSuccess
                            onCheck: function (rowIndex, rowData) { //当前用户角色的赋予
                                var currentUser = top.$('#tableUser').datagrid('getSelected');
                                if (firstCheckRole != '1' && currentUser) {
                                    var query = 'action=userId=' + currentUser.ID + '&targetIds=' + rowData.ID;
                                    $.ajaxjson('/FrameworkModules/PermissionSet/AddUserToRole', query, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('授予角色失败！');
                                        }
                                    });
                                }
                            }, //end of onCheck
                            onUncheck: function (rowIndex, rowData) { //当前用户角色的收回
                                var currentUser = top.$('#tableUser').datagrid('getSelected');
                                if (firstCheckRole != '1' && currentUser) {
                                    var query = 'userId=' + currentUser.ID + '&targetIds=' + rowData.ID;
                                    $.ajaxjson('/FrameworkModules/PermissionSet/RemoveUserFromRole', query, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('回收角色失败！');
                                        }
                                    });
                                }
                            } //end of onUncheck
                        });
                    },
                    onSelect: function (rowIndex, rowData) {
                        if (rowData) {
                            //1、加载当前用户所拥有的角色                            
                            $.ajaxtext('/FrameworkModules/PermissionSet/GetUserRoleIds', 'userId=' + rowData.ID, function (data) {
                                firstCheckRole = "1";
                                top.$('#tableRole').datagrid('uncheckAll'); //取消所有选中行
                                if (data != '' && data.toString() != '[object XMLDocument]') {
                                    var curUserRoleIds = data.split(',');
                                    for (var i = 0; i < curUserRoleIds.length; i++) {
                                        var rowidx = top.$('#tableRole').datagrid('getRowIndex', curUserRoleIds[i]);
                                        if (rowidx) {
                                            top.$('#tableRole').datagrid('checkRow', rowidx);
                                        }
                                    }
                                }
                                firstCheckRole = "0";
                            });
                        }
                    }
                });
            },
            submit: function () {
                formDialog.dialog('close');
                return false;
            }
        });
        return false;
    },
    SetUserBatchPermission: function () {  //用户权限集中批量设置
        var batchPermissionDialog = top.$.hDialog({
            href: '/FrameworkModules/PermissionSet/UserPermissionBatchSet', width: 1100, height: 630, title: '用户权限批量设置', iconCls: 'icon16_lightning',
            onLoad: function () {
                top.$('#FormContent').layout('panel', 'center').panel({ title: '' });
                //1、绑定界面控件
                //1.1、绑定用户列表与角色列表
                top.$('#tableUser,#tableRole').datagrid({
                    width: 180,
                    height: 390,
                    iconCls: 'icon16_group',
                    loadMsg: "数据加载中...",
                    nowrap: false, //折行                    
                    striped: true, //隔行变色
                    idField: 'ID', //主键                    
                    checkOnSelect: false,
                    showHeader: false,
                    pagination: false,
                    pageSize: 20,
                    pageList: [20, 40, 50]
                });

                top.$('#tableUser').datagrid({
                    singleSelect: true, //单选
                    rownumbers: true, //行号
                    columns: [[
                       { title: 'Id', field: 'ID', hidden: true },
                       { title: '用户名称', field: 'REALNAME', width: 130 }
                    ]],
                    url: '/FrameworkModules/UserAdmin/GetUserListJson',
                    onClickRow: function (rowIndex, rowData) { //选中某一用户后，绑定当前用户所拥有的角色、模块（菜单）访问权限、操作权限
                        //1.1.1、绑定当前用户所拥有的角色
                        $.ajaxtext('/FrameworkModules/PermissionSet/GetUserRoleIds', 'userId=' + rowData.ID, function (data) {
                            firstCheckRole = "1";
                            top.$('#tableRole').datagrid('uncheckAll'); //取消所有选中行   
                            if (data != '' && data.toString() != '[object XMLDocument]') {
                                var curUserRoleIds = data.split(',');
                                for (var i = 0; i < curUserRoleIds.length; i++) {
                                    var rowidx = top.$('#tableRole').datagrid('getRowIndex', curUserRoleIds[i]);
                                    if (rowidx) {
                                        top.$('#tableRole').datagrid('checkRow', rowidx);
                                    }
                                }
                                firstCheckRole = "0";
                            }
                        });

                        //1.1.2、绑定当前用户已经拥有的模块（菜单）访问权限。
                        var curUserModuleIds = [];
                        var query1 = 'userId=' + rowData.ID;
                        $.ajaxtext('/FrameworkModules/PermissionSet/GetModuleByUserId', query1, function (data) {
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
                                firstCheckModule = '0';
                            }
                        });

                        //1.1.3、绑定当前用户已经拥有的操作权限
                        var curUserPermissionItemIds = [];
                        var query = 'userId=' + rowData.ID;
                        $.ajaxtext('/FrameworkModules/PermissionSet/GetPermissionItemsByUserId', query, function (data) {
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
                                firstCheckPermissionItem = '0';
                            }
                        });
                    } //end of onClickRow
                });

                //1.2、绑定角色列表
                top.$('#tableRole').datagrid({
                    singleSelect: false,
                    columns: [[
                       { title: 'Id', field: 'ID', width: 25, align: 'left', checkbox: true },
                       { title: '角色名称', field: 'REALNAME', width: 125 }
                    ]],
                    url: '/FrameworkModules/RoleAdmin/GetRoleList',
                    onCheck: function (rowIndex, rowData) { //1.2.1、当前用户角色的赋予
                        var curUser = top.$('#tableUser').datagrid('getSelected');
                        if (curUser) {
                            if (firstCheckRole != '1') {
                                var query = 'userId=' + curUser.ID + '&targetIds=' + rowData.ID;
                                $.ajaxjson('/FrameworkModules/PermissionSet/AddUserToRole', query, function (d) {
                                    if (d.Data != '1') {
                                        msg.warning('授予角色失败！');
                                    }
                                });
                            }
                        }
                        else {
                            msg.warning('请选择一个用户。');
                        }
                    }, //end of onCheck
                    onUncheck: function (rowIndex, rowData) { //1.2.2、当前用户角色的收回
                        var curUser = top.$('#tableUser').datagrid('getSelected');
                        if (curUser) {
                            if (firstCheckRole != '1') {
                                var query = 'userId=' + curUser.ID + '&targetIds=' + rowData.ID;
                                $.ajaxjson('/FrameworkModules/PermissionSet/RemoveUserFromRole', query, function (d) {
                                    if (d.Data != '1') {
                                        msg.warning('回收角色失败！');
                                    }
                                });
                            }
                        } else {
                            msg.warning('请选择一个用户。');
                        }
                    }
                });

                //1.3、绑定模块（菜单）列表
                top.$('#tableModule,#tablePermissionItem').tree({
                    cascadeCheck: false, //联动选中节点
                    checkbox: true,
                    lines: true
                });

                top.$('#tableModule').tree({
                    url: '/FrameworkModules/ModuleAdmin/GetModuleTreeJson?isTree=1',
                    onCheck: function (node, checked) {
                        var curUser = top.$('#tableUser').datagrid('getSelected');
                        if (curUser) {
                            if (firstCheckModule == '0') {
                                if (checked) { //1.3.1、授予当前用户所选模块的访问权限                                           
                                    $.ajaxjson('/FrameworkModules/PermissionSet/SetUserModulePermission', 'userId=' + curUser.ID + '&grantIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('授予用户模块访问权限失败！');
                                        }
                                    });
                                } else { //1.3.2、回收当前用户所选模块的访问权限
                                    $.ajaxjson('/FrameworkModules/PermissionSet/SetUserModulePermission', 'userId=' + curUser.ID + '&revokeIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('收回用户模块访问权限失败！');
                                        }
                                    });
                                }
                            }
                        } else {
                            msg.warning('请选择一个用户。');
                        }
                    }
                });
                //1.4、绑定操作权限项列表
                top.$('#tablePermissionItem').tree({
                    url: '/FrameworkModules/PermissionItemAdmin/GetPermissionItemTreeJson?isTree=1',
                    onCheck: function (node, checked) {
                        var curUser = top.$('#tableUser').datagrid('getSelected');
                        if (curUser) {
                            if (firstCheckPermissionItem == '0') {
                                if (checked) { //1.4.1、授予当前用户所选操作权限
                                    $.ajaxjson('/FrameworkModules/PermissionSet/SetUserPermissionItem', 'userId=' + curUser.ID + '&grantIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('授予用户操作权限失败！');
                                        }
                                    });
                                } else {  //1.4.2、回收当前用户所选操作权限
                                    $.ajaxjson('/FrameworkModules/PermissionSet/SetUserPermissionItem', 'userId=' + curUser.ID + '&revokeIds=' + node.id, function (d) {
                                        if (d.Data != '1') {
                                            msg.warning('收回用户操作权限失败！');
                                        }
                                    });
                                }
                            }
                        } else {
                            msg.warning('请选择一个用户。');
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
    SetUserPermissionScope: function () { //用户授权范围  
        var currentUser = mygrid.selected();
        var up = new UserPermissionScope(currentUser, permissionScopFormUrl);
        up.show();
    },
    SetUserTableFieldPermission: function () {  //用户表字段权限设置
        //功能代码逻辑...
        var currentTableFieldPermissionUser = mygrid.selected();
        if (currentTableFieldPermissionUser) {
            var formDialog = top.$.hDialog({
                title: '表字段权限设置', width: 740, height: 588, iconCls: 'icon16_timeline_marker',
                href: userTableFieldPermissionFormUrl,
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
                        url: '/FrameworkModules/PermissionSet/GetAllTableScope?resourceCategory=PIUSER&resourceId=' + currentTableFieldPermissionUser.ID,
                        idField: 'ID',
                        sortName: 'SORTCODE',
                        sortOrder: 'asc',
                        showHeader: false,
                        singleSelect: true,
                        selectOnCheck: true,
                        checkOnSelect: true,
                        pagination: false,
                        rownumbers: true,
                        columns: [[
                           //{ field: 'ck', checkbox: true },
                            {
                                field: 'PermissionValue', title: '权限', width: 25, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionTableSet(' + "'PIUSER'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + rowData.ITEMVALUE + "'" + ',' + value + ')"  src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                                }
                            },
                            { title: '值', field: 'ITEMVALUE', width: 100, align: 'left' },
                            { title: '表名', field: 'ITEMNAME', width: 110, align: 'left', hidden: true }
                        ]],
                        onClickRow: function (rowIndex, rowData) {
                            var cc = rowData.ITEMVALUE;
                            top.$('#tableFiledList').datagrid({
                                url: '/FrameworkModules/PermissionSet/GetDTByTable',
                                queryParams: { tableName: cc, resourceCategory: 'PIUSER', resourceId: currentTableFieldPermissionUser.ID }
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
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'ISPUBLIC'" + ',' + "'PIUSER'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')" src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
//                                            var opt = '<input type="checkbox" id="idISPUBLIC" onclick="javascript:alert(this.checked)">';
//                                            if (rowData.ISPUBLIC == '1') { //这里判断是不是选 
//                                                opt = '<input type="checkbox" id="idISPUBLIC" onclick="javascript:alert(this.checked)" checked="checked">';
//                                            }
//                                            return opt;
                                }
                            },
                            {
                                field: 'COLUMNACCESS', title: '列访问权限', width: 80, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'COLUMNACCESS'" + ',' + "'PIUSER'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')" src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                                }
                            },
                            {
                                field: 'COLUMNEDIT', title: '列编辑权限', width: 80, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'COLUMNEDIT'" + ',' + "'PIUSER'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')"  src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
                                }
                            },
                            {
                                field: 'COLUMNDENEY', title: '列拒绝访问', width: 80, align: 'center',
                                formatter: function (value, rowData, rowIndex) {
                                    return '<img style="cursor:pointer" onclick="permissionSet(' + "'" + rowData.ID + "'" + ',' + value + ',' + "'COLUMNDENEY'" + ',' + "'PIUSER'" + ',' + "'" + currentTableFieldPermissionUser.ID + "'" + ',' + "'" + top.$('#tableList').datagrid('getSelected').ITEMVALUE + "'" + ',' + "'" + rowData.COLUMNCODE + "'" + ')" src="../../Content/Styles/icon/' + (value ? "checkbox_yes.png" : "checkbox_no.png") + '" />';
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
            msg.warning('请选择一个用户哦！');
        }
        return false;
    },
    SetUserTableConstraintSet: function () {  //用户表约束条件权限设置
        //功能代码逻辑...
        var currentUserTableConstraintUser = mygrid.selected();
        if (currentUserTableConstraintUser) {
            var tmpSetUserTableConstraintDialog = top.$.hDialog({
                content: '<div id="tmpGridList"></div>',
                width: 600, height: 500,
                title: '表约束条件设置-当前用户：' + currentUserTableConstraintUser.REALNAME,
                iconCls: 'icon16_script_key',
                buttons: [{
                    text: '关闭',
                    iconCls: 'icon16_cancel',
                    handler: function () {
                        tmpSetUserTableConstraintDialog.dialog("close");
                    }
                }],
                onOpen: function () {
                    top.$('#tmpGridList').datagrid({
                        url: '/FrameworkModules/PermissionSet/GetConstraintDT?resourceCategory=PIUSER&resourceId=' + currentUserTableConstraintUser.ID,
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
                                                var tmpParam = 'resourceCategory=PIUSER&resourceId=' + currentUserTableConstraintUser.ID + '&tableName=' + tmpUserTableConstraintGridRow.TABLECODE + '&tableConstraint=' + top.$('#txtContraint').val();
                                                $.ajaxjson('/FrameworkModules/PermissionSet/SetConstraint', tmpParam, function (d) {
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
                                var tmpUserTableConstraintGridRow = top.$('#tmpGridList').datagrid('getSelected');
                                if (tmpUserTableConstraintGridRow && tmpUserTableConstraintGridRow.PERMISSIONCONSTRAINT != null) {
                                    top.$.messager.confirm('询问提示', '确定要删除【' + tmpUserTableConstraintGridRow.TABLENAME + '】的约束条件吗？', function (data) {
                                        if (data) {
                                            $.ajaxjson('/FrameworkModules/PermissionSet/DeleteConstraint', 'keyId=' + tmpUserTableConstraintGridRow.ID, function (d) {
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
            msg.warning('请选择一个用户哦！');
        }
        return false;
    }
};

//公共方法
var pubMethod = {
    bindRoleList: function () {
        top.$('#tableRole').datagrid({
            url: '/FrameworkModules/RoleAdmin/GetRoleList',
            nowrap: false, //折行                   
            rownumbers: true, //行号
            striped: true, //隔行变色
            idField: 'ID', //主键
            singleSelect: true, //单选
            frozenColumns: [[]],
            columns: [[
            //{ title: '角色编码', field: 'CODE', width: 120, align: 'left' },
               {title: '角色名称', field: 'REALNAME', width: 150, align: 'left' }
            ]],
            onLoadSuccess: function (data) {
                top.$('#tableRole').datagrid('selectRow', 0);
            }
        });
    },
    bindModuleList: function () {
        top.$('#tableModule').tree({
            cascadeCheck: false, //联动选中节点
            checkbox: true,
            lines: true,
            url: '/FrameworkModules/ModuleAdmin/GetModuleTreeJson?isTree=1',
            onBeforeLoad: function (node, param) {
                firstCheckModule = '1';
                top.$.hLoading.show();
            },
            onLoadSuccess: function (node, data) {
                firstCheckModule = '0';
                top.$.hLoading.hide();
            },
            onSelect: function (node) {
                top.$('#tableModule').tree('getChildren', node.target);
            }
        });
    },
    bindPermissionItemList: function () {
        top.$('#tablePermissionItem').tree({
            cascadeCheck: false, //联动选中节点
            checkbox: true,
            lines: true,
            url: '/FrameworkModules/PermissionItemAdmin/GetPermissionItemTreeJson?isTree=1',
            onBeforeLoad: function (node, param) {
                firstCheckPermissionItem = '1';
                top.$.hLoading.show();
            },
            onLoadSuccess: function (node, data) {
                firstCheckPermissionItem = '0';
                top.$.hLoading.hide();
            },
            onSelect: function (node) {
                top.$('#tablePermissionItem').tree('getChildren', node.target);
            }
        });
    }
};
