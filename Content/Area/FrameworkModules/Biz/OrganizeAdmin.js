var formUrl = "/Admin/FrameworkModules/OrganizeAdmin/Form/",
    navgrid;

$(function () {
    autoResize({ dataGrid: '#organizeGrid', gridType: 'treegrid', callback: mygrid.bindGrid, height: 5 });
    $('#btnAdd').attr('onclick', 'OrganizeAdminMethod.AddOrganize();');//新增组织机构
    $('#btnEdit').attr('onclick', 'OrganizeAdminMethod.EditOrganize();');//修改组织机构
    $('#btnDelete').attr('onclick', 'OrganizeAdminMethod.DeleteOrganize();');//删除组织机构
    $('#btnMoveTo').attr('onclick', 'OrganizeAdminMethod.MoveTo();');//移动组织机构
    $('#btnExport').attr('onclick', 'OrganizeAdminMethod.ExportOrganize();');//导出组织机构数据
    $('#btnUserOrganizePermission').attr('onclick', 'OrganizeAdminMethod.SetUserOrganizePermission();');//设置用户组织机构权限
    $('#btnRoleOrganizePermission').attr('onclick', 'OrganizeAdminMethod.SetRoleOrganizePermission();'); //设置角色组织机构权限
    $('#a_refresh').attr('onclick', 'OrganizeAdminMethod.Refreash();');//刷新
});

var mygrid = {
    bindGrid: function (winsize) {
        navgrid = $('#organizeGrid').treegrid({
            toolbar: '#toolbar',           
            width: winsize.width,
            height: winsize.height,
            nowrap: true,
            rownumbers: true,
            animate: true,
            resizable: true,
            collapsible: false,
            onContextMenu: pageContextMenu.createTreeGridContextMenu,
            url: '/Admin/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/',
            idField: 'id',
            treeField: 'fullname',
			onDblClickRow:function(row){
				document.getElementById('btnEdit').click();
			},
            frozenColumns: [[
                { title: '组织机构名称', field: 'fullname', width: 200 },
                { title: '编码', field: 'code', width: 100 }
            ]],
            columns: [[
                { title: '简称', field: 'shortname', width: 120 },
                { title: '主负责人', field: 'manager', width: 70, align: 'center' },
                { title: '电话', field: 'outerphone', width: 100, align: 'center' },
                { title: '传真', field: 'fax', width: 100, align: 'center' },
                { title: '有效', field: 'enabled', width: 50, align: 'center', formatter: imgcheckbox },
                { title: '排序', field: 'sortcode', width: 80, align: 'center' },
                { title: '备注', field: 'description', width: 300 },
                { title: 'ParentId', field: 'parentid', hidden: true },
                { title: 'Category', field: 'category', hidden: true },
                { title: 'InnerPhone', field: 'innerphone', hidden: true },
                { title: 'Postalcode', field: 'postalcode', hidden: true },
                { title: 'Address', field: 'address', hidden: true },
                { title: 'Web', field: 'web', hidden: true },
                { title: 'AssistantManager', field: 'assistantmanager', hidden: true },
                { title: 'IsInnerOrganize', field: 'isinnerorganize', hidden: true }
            ]]
        });
    },
    reload: function () {
        navgrid.treegrid('reload');
    },
    selected: function () {
        return navgrid.treegrid('getSelected');
    }
};
var imgcheckbox = function (cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};
var OrganizeAdminMethod = {
    Refreash: function () {
        mygrid.reload();
    },
    AddOrganize: function () { //增加组织机构
        var addDialog = top.$.hDialog({
            href: formUrl,
            title: '添加组织机构',
            iconCls: 'icon16_add',
            width: 750,
            height: 450,
            onLoad: function () {
                pubMethod.bindCtrl();
                top.$('#enabled,#isinnerorganize').attr("checked", true);
                pageMethod.bindCategory('category', 'OrganizeCategory');
                pubMethod.bindComboGrid();
                var row = mygrid.selected();
                if (row) {
                    top.$('#parentid').combotree('setValue', row.parentid);
                }
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var Manager = top.$('#managerid').combogrid('getText');
                    var AssistantManager = top.$('#assistantmanagerid').combogrid('getText');
                    var postData = pageMethod.serializeJson(top.$('#uiform'));
                    var parOther = 'Manager=' + Manager + '&AssistantManager=' + AssistantManager;
                    $.ajaxjson("/Admin/FrameworkModules/OrganizeAdmin/SubmitForm/?" + parOther, postData, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            addDialog.dialog('close');
                            mygrid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            }
        });
        return false;
    },
    EditOrganize: function () { //修改组织机构
        var row = mygrid.selected();
        if (row) {
            var editDailog = top.$.hDialog({
                href: formUrl,
                title: '修改组织机构',
                iconCls: 'icon16_edit_button',
                width: 750,
                height: 450,
                onLoad: function () {
                    pubMethod.bindCtrl(row.id);
                    pageMethod.bindCategory('category', 'OrganizeCategory');
                    pubMethod.bindComboGrid();
                    var parm = 'key=' + row.id;
                    setTimeout(
                        $.ajaxjson('/Admin/FrameworkModules/OrganizeAdmin/GetEntity/', parm, function (data) {
                            if (data) {
                                SetWebControls(data, true);
                            }
                        }), 400);
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {

                        //保存时判断当前节点所选的父节点，不能为当前节点的子节点，这样就乱套了....
                        var treeParentId = top.$('#parentid').combotree('tree'); // 得到树对象
                        var node = treeParentId.tree('getSelected');
                        if (node) {
                            var nodeParentId = treeParentId.tree('find', row.id);
                            var children = treeParentId.tree('getChildren', nodeParentId.target);
                            var nodeIds = '';
                            var isFind = 'false';
                            for (var index = 0; index < children.length; index++) {
                                if (children[index].id == node.id) {
                                    isFind = 'true';
                                    break;
                                }
                            }

                            if (isFind == 'true') {
                                top.$.messager.alert('温馨提示', '请选择父节点元素！', 'warning');
                                return;
                            }
                        }
                        var Manager = top.$('#managerid').combogrid('getText');
                        var AssistantManager = top.$('#assistantmanagerid').combogrid('getText');
                        var postData = pageMethod.serializeJson(top.$('#uiform'));
                        var parOther = 'key=' + row.id + '&Manager=' + Manager + '&AssistantManager=' + AssistantManager;
                        $.ajaxjson("/Admin/FrameworkModules/OrganizeAdmin/SubmitForm/?" + parOther, postData, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                editDailog.dialog('close');
                                mygrid.reload();
                            } else {
                                MessageOrRedirect(d);
                            }
                        });
                        
                        
                    }
                }
            });
        } else {
            msg.warning('请选择要修改的组织机构!');
            return false;
        }
        return false;
    },
    DeleteOrganize: function () { //删除组织机构
        var row = mygrid.selected();
        if (row != null) {
            var childs = $('#organizeGrid').treegrid('getChildren', row.id);
            if (childs.length > 0) {
                $.messager.alert('警告提示', '当前所选有子节点数据，不能删除。', 'warning');
                return false;
            }
            $.messager.confirm('询问提示', '确认要删除选中的组织机构吗？', function (data) {
                if (data) {
                    var parm = 'key=' + row.id;
                    $.ajaxjson("/Admin/FrameworkModules/OrganizeAdmin/Delete/", parm, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            mygrid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                } else {
                    return false;
                }
            });
        } else {
            msg.warning('请选择要删除的组织机构!');
            return false;
        }
        return false;
    },
    MoveTo: function () { //移动组织机构
        var row = mygrid.selected();
        if (row != null) {
            var ad = top.$.hDialog({
                max: false,
                width: 300,
                height: 500,
                title: '移动组织机构 ━ ' + row.fullname,
                iconCls: 'icon16_arrow_switch',
                content: '<ul id="orgTree"></ul>',
                submit: function () {
                    var node = top.$('#orgTree').tree('getSelected');
                    if (node) {
                        var parm = 'organizeId=' + row.id + '&parentId=' + node.id;
                        $.ajaxjson("/Admin/FrameworkModules/OrganizeAdmin/MoveTo/", parm, function (d) {
                            if (d.Success) {
                                msg.ok('移动成功！');
                                mygrid.reload();
                            } else {
                                msg.warning('移动失败！');
                                MessageOrRedirect(d);
                            }
                        });
                    } else {
                        msg.warning('请选择要移动的节点！');
                    }
                }
            });

            top.$(ad).hLoading();
            top.$('#orgTree').tree({
                url: '/Admin/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/?isTree=1',
                valuefield: 'id',
                textField: 'text',
                animate: true,
                lines: true,
                onLoadSuccess: function (node, data) {
                    top.$.hLoading.hide(); //加载完毕后隐藏loading
                },
                onClick: function (node) {
                    var selectedId = node.id;
                }
            });

        } else {
            msg.warning('请选择要移动的组织机构!');
            return false;
        }
        return false;
    },
    ExportOrganize: function () { //导出组织机构
        var exportData = new ExportExcel('organizeGrid');
        exportData.go('PIORGANIZE', 'SORTCODE');
    },
    SetUserOrganizePermission: function () { //设置用户组织机构权限
        //功能代码逻辑...
        var userGrid;
        var curResourceTargetResourceIds = [];
        var setDialog = top.$.hDialog({
            title: '（用户-组织机构）权限设置',
            width: 670,
            height: 600,
            iconCls: 'icon16_key', //cache: false,
            href: "/Admin/FrameworkModules/PermissionSet/PermissionBacthSet/",
            onLoad: function () {
                using('panel', function () {
                    top.$('#panelTarget').panel({ title: '组织机构列表', iconCls: 'icon-org', height: $(window).height() - 3 });
                });

                userGrid = top.$('#leftnav').datagrid({
                    title: '用户列表',
                    url: '/Admin/FrameworkModules/UserAdmin/GetUserListJson/',
                    nowrap: false, //折行
                    //fit: true,
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'id', //主键
                    singleSelect: true, //单选
                    frozenColumns: [[]],
                    columns: [
                        [
                            { title: '登录名', field: 'username', width: 120, align: 'left' },
                            { title: '用户名', field: 'realname', width: 150, align: 'left' }
                        ]
                    ],
                    onLoadSuccess: function (data) {
                        top.$('#rightnav').tree({
                            cascadeCheck: false, //联动选中节点
                            checkbox: true,
                            lines: true,
                            url: '/Admin/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/?isTree=1',
                            onSelect: function (node) {
                                top.$('#rightnav').tree('getChildren', node.target);
                            }
                        });
                        top.$('#leftnav').datagrid('selectRow', 0);
                    },
                    onSelect: function (rowIndex, rowData) {
                        curResourceTargetResourceIds = [];
                        var query = 'resourceCategory=PIUSER&resourceId=' + rowData.id + '&targetCategory=PIORGANIZE';
                        $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetPermissionScopeTargetIds/', query, function (data) {
                            var targetResourceTree = top.$('#rightnav');
                            targetResourceTree.tree('uncheckedAll');
                            if (data == '' || data.toString() == '[object XMLDocument]') {
                                return;
                            }
                            curResourceTargetResourceIds = data.split(',');
                            for (var i = 0; i < curResourceTargetResourceIds.length; i++) {
                                var node = targetResourceTree.tree('find', curResourceTargetResourceIds[i]);
                                if (node)
                                    targetResourceTree.tree("check", node.target);
                            }
                        });
                    }
                });
            },
            submit: function () {
                var allSelectTargetResourceIds = permissionMgr.getSelectedResource().split(',');
                var grantResourceIds = '';
                var revokeResourceIds = '';
                var flagRevoke = 0;
                var flagGrant = 0;
                while (flagRevoke < curResourceTargetResourceIds.length) {
                    if ($.inArray(curResourceTargetResourceIds[flagRevoke], allSelectTargetResourceIds) == -1) {
                        revokeResourceIds += curResourceTargetResourceIds[flagRevoke] + ','; //得到收回的权限列表
                    }
                    ++flagRevoke;
                }

                while (flagGrant < allSelectTargetResourceIds.length) {
                    if ($.inArray(allSelectTargetResourceIds[flagGrant], curResourceTargetResourceIds) == -1) {
                        grantResourceIds += allSelectTargetResourceIds[flagGrant] + ','; //得到授予的权限列表
                    }
                    ++flagGrant;
                }

                var query = 'resourceId=' + top.$('#leftnav').datagrid('getSelected').id
                    + '&resourceCategory=PIUSER&targetCategory=PIORGANIZE'
                    + '&grantTargetIds=' + grantResourceIds + "&revokeTargetIds=" + revokeResourceIds;
                $.ajaxjson('/Admin/FrameworkModules/PermissionSet/GrantRevokePermissionScopeTargets/', query, function (d) {
                    if (d.Data > 0) {
                        msg.ok('设置成功！');
                    } else {
                        alert(d.Message);
                    }
                });
            }
        });
        return false;
    },
    SetRoleOrganizePermission: function () { //设置角色组织机构权限
        var userGrid;
        var curResourceTargetResourceIds = [];
        var setDialog = top.$.hDialog({
            title: '（角色-组织机构）权限设置',
            width: 670,
            height: 600,
            iconCls: 'icon16_lightning', //cache: false,
            href: "/Admin/FrameworkModules/PermissionSet/PermissionBacthSet/",
            onLoad: function () {
                using('panel', function () {
                    top.$('#panelTarget').panel({ title: '组织机构列表', iconCls: 'icon-org', height: $(window).height() - 3 });
                });

                userGrid = top.$('#leftnav').datagrid({
                    title: '角色列表',
                    url: '/Admin/FrameworkModules/RoleAdmin/GetRoleList/',
                    nowrap: false, //折行
                    //fit: true,
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'ID', //主键
                    singleSelect: true, //单选
                    frozenColumns: [[]],
                    columns: [
                        [
                            { title: '角色编码', field: 'CODE', width: 120, align: 'left' },
                            { title: '角色名称', field: 'REALNAME', width: 150, align: 'left' }
                        ]
                    ],
                    onLoadSuccess: function (data) {
                        top.$('#rightnav').tree({
                            cascadeCheck: false, //联动选中节点
                            checkbox: true,
                            lines: true,
                            url: '/Admin/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/?isTree=1',
                            onSelect: function (node) {
                                top.$('#rightnav').tree('getChildren', node.target);
                            }
                        });
                        top.$('#leftnav').datagrid('selectRow', 0);
                    },
                    onSelect: function (rowIndex, rowData) {
                        curResourceTargetResourceIds = [];
                        var query = 'resourceCategory=PiRole&resourceId=' + rowData.ID + '&targetCategory=PiOrganize';
                        $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetPermissionScopeTargetIds/', query, function (data) {
                            var targetResourceTree = top.$('#rightnav');
                            targetResourceTree.tree('uncheckedAll');
                            if (data == '' || data.toString() == '[object XMLDocument]') {
                                return;
                            }
                            curResourceTargetResourceIds = data.split(',');
                            for (var i = 0; i < curResourceTargetResourceIds.length; i++) {
                                var node = targetResourceTree.tree('find', curResourceTargetResourceIds[i]);
                                if (node)
                                    targetResourceTree.tree("check", node.target);
                            }
                        });
                    }
                });
            },
            submit: function () {
                var allSelectTargetResourceIds = permissionMgr.getSelectedResource().split(',');
                var grantResourceIds = '';
                var revokeResourceIds = '';
                var flagRevoke = 0;
                var flagGrant = 0;
                while (flagRevoke < curResourceTargetResourceIds.length) {
                    if ($.inArray(curResourceTargetResourceIds[flagRevoke], allSelectTargetResourceIds) == -1) {
                        revokeResourceIds += curResourceTargetResourceIds[flagRevoke] + ','; //得到收回的权限列表
                    }
                    ++flagRevoke;
                }

                while (flagGrant < allSelectTargetResourceIds.length) {
                    if ($.inArray(allSelectTargetResourceIds[flagGrant], curResourceTargetResourceIds) == -1) {
                        grantResourceIds += allSelectTargetResourceIds[flagGrant] + ','; //得到授予的权限列表
                    }
                    ++flagGrant;
                }

                var query = 'resourceId=' + top.$('#leftnav').datagrid('getSelected').ID
                    + '&resourceCategory=PiRole&targetCategory=PiOrganize'
                    + '&grantTargetIds=' + grantResourceIds + "&revokeTargetIds=" + revokeResourceIds;
                $.ajaxjson('/Admin/FrameworkModules/PermissionSet/GrantRevokePermissionScopeTargets/', query, function (d) {
                    if (d.Data > 0) {
                        msg.ok('设置成功！');
                    } else {
                        alert(d.Message);
                    }
                });
            }
        });
        return false;
    }
};

//公共方法
var pubMethod = {
    bindCtrl: function (navId) {
        var treeData = navgrid.treegrid('getData');
        treeData = JSON.stringify(treeData).replace(/id/g, 'id').replace(/fullname/g, 'text');
        treeData = '[{"id":0,"selected":true,"text":"请选择上级节点"},' + treeData.substr(1, treeData.length - 1);

        top.$('#parentid').combotree({
            data: JSON.parse(treeData),
            valueField: 'id',
            textField: 'text',
            panelWidth: '280',
            editable: false,
            lines: true,
            onSelect: function (node) {
                var nodeId = top.$('#parentid').combotree('getValue');
                if (node.id == navId) {
                    top.$('#parentid').combotree('setValue', nodeId);
                    top.$.messager.alert('警告提示', '上级节点不能与当前所选相同！', 'warning');
                }
            }
        }).combotree('setValue', 0);

        top.$('#code').focus();
        top.$('#uiform').validate({
            //此处加入验证
        });
    },
    bindComboGrid: function () {
        top.$('#managerid,#assistantmanagerid').combogrid({
            panelWidth: 320,
            idField: 'ID',
            textField: 'REALNAME',
            url: '/Admin/FrameworkModules/UserAdmin/GetUserListByPage/',
            sortName: 'SORTCODE',
            sortOrder: 'asc',
            showPageList: false,
            striped: true,
            pagination: true,
            rownumbers: true,
            fitColumns: true,
            pageSize: 50,
            pageList: [10, 20, 30, 50],
            method: 'post',
            columns: [[
                { title: '登录名', field: 'USERNAME', width: 60, sortable: true },
                { title: '用户名', field: 'REALNAME', width: 70 }
            ]]
        });
    }
};

var permissionMgr = {
    getSelectedResource: function () {
        var nodes = top.$('#rightnav').tree('getChecked');

        if (nodes.length > 0) {
            var dwg = [];
            for (var i = 0; i < nodes.length; i++) {
                dwg.push(nodes[i].id);
            }
            //alert(dwg.join(','));
            return dwg.join(',');

        } else {
            return "";
        }
    }
};

