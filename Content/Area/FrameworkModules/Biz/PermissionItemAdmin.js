var controlPermissionItemUrl = '/FrameworkModules/PermissionItemAdmin/',
    formUrl = "/FrameworkModules/PermissionItemAdmin/Form",
    navgrid;

$(function () {
	pageSizeControl.init({gridId:'permissionitemGrid',gridType:'treegrid'});
    permissionItemTree.init();
    autoResize({ dataGrid: '#permissionitemGrid', gridType: 'treegrid', callback: mygrid.bindGrid, height: 35, width: 230 });
    
    $('#a_add').attr('onclick', 'crud.add();');
    $('#a_edit').attr('onclick', 'crud.edit();');
    $('#a_delete').attr('onclick', 'crud.del();');
    $('#a_setuserpermissionitemepermission').attr('onclick', 'crud.userPermissionItemBatchSet();');
    $('#a_setrolepermissionitemepermission').attr('onclick', 'crud.rolePermissionItemBatchSet();');
    $('#a_move').attr('onclick', 'crud.move();');
    $('#a_refresh').attr('onclick', 'crud.refreash();');
    
	$(window).resize(function () {        
		pageSizeControl.init({gridId:'permissionitemGrid',gridType:'treegrid'});
    });
});

var permissionItemTree = {
    init: function () {
        $('#permissionItemTree').tree({
            lines: true,
            url: controlPermissionItemUrl + 'GetPermissionItemTreeJson?isTree=1',
            animate: true,
            onLoadSuccess: function (node, data) {
				if(data.length && data.length>0){					
					$('body').data('permissionItemData', data);
				}
            },
            onClick: function (node) {
                $(this).tree('toggle', node.target);
            },
            onExpand: function (node) {
                var keys = permissionItemTree.getSelectedChildIds(node);
                if (keys && keys.length > 0) {
                    var addStr = '<span class="tree-title">(' + (keys.split(',').length - 1) + ')</span>';
                    if (!node.text.toIncludeString(addStr)) {
                        $(this).tree('update', {
                            target: node.target,
                            text: node.text + addStr
                        });
                    }
                }
            },
            onSelect: function (node) {
                //$(this).tree('expand', node.target);
                var keys = permissionItemTree.getSelectedChildIds(node);
                $('#permissionitemGrid').treegrid({
                    url: controlPermissionItemUrl + 'GetPermissionItemByIds',
                    queryParams: { permissionItemIds: keys }
                });
            }
        });
    },
    data: function (opr) {
        var d = JSON.stringify($('body').data('permissionItemData'));
        if (opr === '1') {
            d = '[{"id":0,"text":"请选择操作权限项"},' + d.substr(1);
        }
        return JSON.parse(d);
    },
    selected:function() {
        return $('#permissionItemTree').tree('getSelected');
    },
    getSelectedChildIds: function (node) {
        var children = $('#permissionItemTree').tree('getLeafChildren', node.target);
        var ids = '';
        if (children) {
            for (var i = 0; i < children.length; i++) {
                ids += children[i].id + ',';
            }
        }
        return ids;
    }
};

var mygrid = {
    bindGrid: function(size) {
        navgrid = $('#permissionitemGrid').treegrid({
            toolbar: '#toolbar',
            //title: '操作权限列表',
            //iconCls: 'icon icon-layout',
            width: size.width,
            height: size.height,
            nowrap: false,
            rownumbers: true,
            loadMsg: '正在努力加载中...',
            resizable: true,
            collapsible: false,
            onContextMenu: pageContextMenu.createTreeGridContextMenu,
            idField: 'Id',
            treeField: 'FullName',
			onDblClickRow:function(row){
				document.getElementById('a_edit').click();
			},
            frozenColumns: [
                [
                    { title: '操作权限名称', field: 'FullName', width: 200 },
                    { title: '编码', field: 'Code', width: 160 }
                ]
            ],
            columns: [
                [
                    { title: '分类', field: 'CategoryCode', width: 100 },
                    {
                        title: '公共',
                        field: 'IsPublic',
                        width: 50,
                        align: 'center',
                        formatter: function(v, d, i) {
                            return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                        }
                    },
                    { title: '有效', field: 'Enabled', width: 50, align: 'center', formatter: imgcheckbox },
                    { title: '排序', field: 'SortCode', width: 80, align: 'right' },
                    { title: '备注', field: 'Description', width: 500 },
                    { title: 'ParentId', field: 'ParentId', hidden: true },
                    { title: 'AllowEdit', field: 'AllowEdit', hidden: true },
                    { title: 'AllowDelete', field: 'AllowDelete', hidden: true },
                    { title: 'IsScope', field: 'IsScope', hidden: true }
                ]
            ]
        });
    },
    reload: function (treeNode) {
        if (treeNode) {
            var keys = permissionItemTree.getSelectedChildIds(treeNode);
            if (keys !== '') {
                navgrid.treegrid({
                    url: controlPermissionItemUrl + "?action=GetPermissionItemByIds",
                    queryParams: { permissionItemIds: keys }
                });
            }
        }
    },
    selected: function() {
        return navgrid.treegrid('getSelected');
    }
};

var imgcheckbox = function(cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/../../Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/../../Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};

var setTreeValue = function (id) {
	top.$('#ParentId').combotree('setValue', id);
};

var crud = {
    refreash: function () {
        mygrid.reload(permissionItemTree.selected());
    },
    add: function () {
        var gridSelected = mygrid.selected(),
			treeSelected = permissionItemTree.selected();
        var row = mygrid.selected();
        if (!row) {
            row = treeSelected;
        }
        var addDialog = top.$.hDialog({
            href: formUrl, title: '添加操作权限项', iconCls: 'icon16_layout_add', width: 530, height: 310,
            onLoad: function () {
                pubMethod.bindCtrl();
                if (treeSelected) {
                    setTimeout(function () { setTreeValue(treeSelected.id) }, 300);
                    //top.$('#ParentId').combotree('setValue', treeSelected.id);
                }
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var treeParentId = top.$('#ParentId').combotree('tree'); // 得到树对象
                    var node = treeParentId.tree('getSelected');
                    if (node && node.id != 0) {

                        /*
                        var vparentid = top.$('#ParentId').combobox('getValue');
                        var param = 'action=Add&vparentid=' + vparentid + '&' + top.$('#uiform').serialize();
                        $.ajaxjson(controlPermissionItemUrl, param, function (d) {
                        */
                        var queryString = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson(controlPermissionItemUrl + 'SubmitForm', queryString, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                var tmpTree = $('#permissionItemTree');
                                var treeText = top.$('#FullName').val();
                                if (treeSelected) {
                                    tmpTree.tree('append', {
                                        parent: treeSelected.target,
                                        data: [{
                                            id: d.Data,
                                            text: treeText
                                        }]
                                    });
                                }
                                mygrid.reload(treeSelected);
                                addDialog.dialog('close');
                            } else {
                                MessageOrRedirect(d);
                            }
                        });
                    } else {
                        top.$.messager.alert('温馨提示', '请至少选择一个父节点元素！', 'warning');
                        return;
                    }
                }
            }
        });
        return false;
    },
    edit: function () {
        var originalParentId = '', //修改前父节点
			gridSelected = mygrid.selected(),
			treeSelected = permissionItemTree.selected();
        var row = mygrid.selected();
        if (!row) {
            row = treeSelected;
        }
        if (row) {
            var editDailog = top.$.hDialog({
                href: formUrl, title: '修改操作权限项', iconCls: 'icon16_layout_edit', width: 530, height: 310,
                onLoad: function () {
                    pubMethod.bindCtrl();
                    var parm = 'key=' + (row.Id || row.id);
                    $.ajaxjson('/FrameworkModules/PermissionItemAdmin/GetEntity', parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                        setTimeout(function () {
                            setTreeValue(data.ParentId);
                         }, 300);
                    });
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        //保存时判断当前节点所选的父节点，不能为当前节点的子节点，这样就乱套了....
                        var treeParentId = top.$('#ParentId').combotree('tree'); // 得到树对象
                        var node = treeParentId.tree('getSelected');
                        if (node && node.id != 0) {
                            var nodeParentId = treeParentId.tree('find', (row.Id || row.id));
                            if (nodeParentId === null) {
                                return;
                            }
                            var children = treeParentId.tree('getChildren', nodeParentId.target);
                            var isFind = 'false';
                            for (var index = 0; index < children.length; index++) {
                                if (children[index].id == node.id) {
                                    isFind = 'true';
                                    break;
                                }
                            }

                            if (isFind == 'true') {
                                top.$.messager.alert('温馨提示', '请正确选择父节点元素，不能为当前节点的子节点!', 'warning');
                                return;
                            }
                        } else {
                            top.$.messager.alert('温馨提示', '请至少选择一个父节点元素！', 'warning');
                            return;
                        }
                        var vparentid = top.$('#ParentId').combobox('getValue');
                        var queryString = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson(controlPermissionItemUrl + 'SubmitForm?key=' + (row.Id || row.id), queryString, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                var tmpTree = $('#permissionItemTree');
                                var treeText = top.$('#FullName').val();

                                //TODO:这儿还要判断下改变父节点的情况。

                                if (gridSelected) { //A、单击的是dataGrid进行修改
                                    var curnode = tmpTree.tree('find', row.Id);
                                    tmpTree.tree('update', {
                                        target: curnode.target,
                                        text: treeText
                                    });

                                    //1、改变父节点的情况：
                                    //1.1、判断左侧树的选择节点（即父节点）与当前保存的父节点不一样，则要做相应的移动处理。
                                    if (vparentid != '0' && treeSelected.id !== vparentid) {
                                        //移除当前父节点下移动的子节点
                                        tmpTree.tree('remove', tmpTree.tree('find', row.Id).target);
                                        //修改的父节点树下增加节点
                                        tmpTree.tree('append', {
                                            parent: tmpTree.tree('find', vparentid).target,
                                            data: [{
                                                id: row.Id,
                                                text: treeText
                                            }]
                                        });
                                    }
                                } else { //B、单击的是Tree进行修改
                                    tmpTree.tree('update', {
                                        target: treeSelected.target,
                                        text: treeText
                                    });

                                    //2、改变父节点的情况：
                                    if (vparentid != '0' && originalParentId !== vparentid) {
                                        //2.1、判断左侧树的选择节点（即父节点）与当前保存的父节点不一样，则要做相应的移动处理。
                                        if (treeSelected.id !== vparentid) {
                                            //移除当前父节点下移动的子节点
                                            tmpTree.tree('remove', treeSelected.target);

                                            //修改的父节点树下增加节点
                                            tmpTree.tree('append', {
                                                parent: tmpTree.tree('find', vparentid).target,
                                                data: [{
                                                    id: row.Id,
                                                    text: treeText
                                                }]
                                            });
                                        }
                                    }
                                }
                                mygrid.reload(treeSelected);
                                editDailog.dialog('close');
                            } else {
                                MessageOrRedirect(d);
                            }
                        });
                    }
                }
            });
        } else {
            msg.warning('请选择要修改菜单!');
            return false;
        }
        return false;
    },
    del: function () {
        var row = mygrid.selected();
        var treeSelected = permissionItemTree.selected();
        if (row != null) {
            //var childs = $('#permissionitemGrid').treegrid('getChildren', row.Id);
            var childs = permissionItemTree.getSelectedChildIds($('#permissionItemTree').tree('find', row.Id));
            if (childs && childs.length > 0) {
                $.messager.alert('警告提示', '当前所选有子操作权限项数据，不能删除。<br> 请先删除子操作权限项数据!', 'warning');
                return false;
            }
            var query = 'key=' + row.Id;
            $.messager.confirm('询问提示', '确认要删除选中的操作权限项吗？', function (data) {
                if (data) {
                    $.ajaxjson(controlPermissionItemUrl + 'Delete', query, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            //重新加载
                            var tmpTree = $('#permissionItemTree');
                            var curnode = tmpTree.tree('find', row.Id);
                            if (curnode) {
                                tmpTree.tree('remove', curnode.target);
                            }
                            mygrid.reload(treeSelected);
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
                else {
                    return false;
                }
            });
        }
        else {
            msg.warning('请选择要删除的操作权限项!');
            return false;
        }
        return false;
    },
    move: function () {
        var row = mygrid.selected(),
			treeSelected = permissionItemTree.selected();

        if (row != null) {
            //保存时判断当前节点所选的父节点，不能为当前节点的子节点，这样就乱套了....
            var tmpTree = $('#permissionItemTree');
            var curNode = tmpTree.tree('find', row.Id);
            if (curNode) {
                var children = tmpTree.tree('getChildren', curNode.target);
                if (children && children.length > 0) {
                    top.$.messager.alert('温馨提示', '当前节点有子节点，不能移动!', 'warning');
                    return;
                }
            }

            var ad = top.$.hDialog({
                max: false,
                width: 350,
                height: 500,
                title: '移动操作权限项 ━ ' + row.FullName,
                iconCls: 'icon16_arrow_switch',
                content: '<ul id="tempTree"></ul>',
                submit: function () {
                    var node = top.$('#tempTree').tree('getSelected');
                    if (node) {
                        $.ajaxtext(controlPermissionItemUrl + 'MoveTo', 'key=' + row.Id + '&parentId=' + node.id, function (d) {
                            if (d > 0) {
                                msg.ok('移动成功！');
                                //tree与datagrid同步处理：判断左侧树的选择节点（即父节点）与当前保存的父节点不一样，则要做相应的移动处理。
                                if (treeSelected.id !== node.id) {
                                    //移除当前父节点下移动的子节点									
                                    tmpTree.tree('remove', curNode.target);
                                    //修改的父节点树下增加节点
                                    tmpTree.tree('append', {
                                        parent: tmpTree.tree('find', node.id).target,
                                        data: [{
                                            id: row.Id,
                                            text: curNode.text
                                        }]
                                    });
                                }

                                mygrid.reload(treeSelected);
                                ad.dialog('close');
                            } else if (d == 0) {
                                msg.warning('移动失败！');
                            } else {
                                msg.error('移动出错！');
                            }
                        });
                    } else {
                        msg.warning('请选择要移动的节点！');
                    }
                }
            });

            top.$(ad).hLoading();
            //初始化tree
            top.$('#tempTree').tree({
                url: controlPermissionItemUrl + 'GetPermissionItemTreeJson?isTree=1',
                valuefield: 'id',
                textField: 'text',
                animate: true,
                lines: true,
                onLoadSuccess: function (node, data) {
                    top.$(ad).hLoading.hide(); //加载完毕后隐藏loading
                },
                onSelect: function (node) {
                    if (node.id == row.Id) {
                        top.$.messager.alert('警告提示', '上级操作权限不能与当前所选相同!', 'warning');
                        return;
                    }
                }
            });
        } else {
            msg.warning('请选择要移动的操作权限项!');
            return false;
        }
        return false;
    },
    userPermissionItemBatchSet: function () {
        var userGrid;
        var curUserPermissionItemIds = []; //当前所选用户所拥有的操作权限项ID        
        var setDialog = top.$.hDialog({
            title: '用户操作权限批量设置',
            width: 670, height: 600, iconCls: 'icon16_view_bandwidth_usage', //cache: false,
            href: "/FrameworkModules/PermissionSet/PermissionBacthSet",
            onLoad: function () {
                using('panel', function () {
                    top.$('#panelTarget').panel({ title: '操作权限项', iconCls: 'icon-org', height: $(window).height() - 3 });
                });
                userGrid = top.$('#leftnav').datagrid({
                    title: '所有用户',
                    url: '/FrameworkModules/UserAdmin/GetUserListJson',
                    nowrap: false, //折行
                    //fit: true,
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'ID', //主键
                    singleSelect: true, //单选
                    frozenColumns: [[]],
                    columns: [[
                        { title: '登录名', field: 'USERNAME', width: 120, align: 'left' },
                        { title: '用户名', field: 'REALNAME', width: 150, align: 'left' }
                    ]],
                    onLoadSuccess: function (data) {
                        top.$('#rightnav').tree({
                            cascadeCheck: false, //联动选中节点
                            checkbox: true,
                            lines: true,
                            url: controlPermissionItemUrl + 'GetPermissionItemTreeJson?isTree=1',
                            onSelect: function (node) {
                                top.$('#rightnav').tree('getChildren', node.target);
                            }
                        });
                        top.$('#leftnav').datagrid('selectRow', 0);
                    },
                    onSelect: function (rowIndex, rowData) {
                        curUserPermissionItemIds = [];
                        var query = 'userId=' + rowData.ID;
                        $.ajaxtext('/FrameworkModules/PermissionSet/GetPermissionItemsByUserId', query, function (data) {
                            var permissionItemTree = top.$('#rightnav');
                            permissionItemTree.tree('uncheckedAll');
                            if (data == '' || data.toString() == '[object XMLDocument]') {
                                return;
                            }
                            curUserPermissionItemIds = data.split(',');
                            for (var i = 0; i < curUserPermissionItemIds.length; i++) {
                                var node = permissionItemTree.tree('find', curUserPermissionItemIds[i]);
                                if (node)
                                    permissionItemTree.tree("check", node.target);
                            }
                        });
                    }
                });
            },
            submit: function () {
                var allSelectPemissionItemIds = pubMethod.getUserSelectedPermissionItems().split(',');
                var grantPemissionItemIds = '';
                var revokePemissionItemIds = '';
                var flagRevoke = 0;
                var flagGrant = 0;

                while (flagRevoke < curUserPermissionItemIds.length) {
                    if ($.inArray(curUserPermissionItemIds[flagRevoke], allSelectPemissionItemIds) == -1) {
                        revokePemissionItemIds += curUserPermissionItemIds[flagRevoke] + ','; //得到收回的权限列表
                    }
                    ++flagRevoke;
                }

                while (flagGrant < allSelectPemissionItemIds.length) {
                    if ($.inArray(allSelectPemissionItemIds[flagGrant], curUserPermissionItemIds) == -1) {
                        grantPemissionItemIds += allSelectPemissionItemIds[flagGrant] + ','; //得到授予的权限列表
                    }
                    ++flagGrant;
                }

                var query = 'userId=' + top.$('#leftnav').datagrid('getSelected').ID + '&grantIds=' + grantPemissionItemIds + "&revokeIds=" + revokePemissionItemIds;
                $.ajaxjson('/FrameworkModules/PermissionSet/SetUserPermissionItem', query, function (d) {
                    if (d.Data > 0) {
                        msg.ok('设置成功！');
                    }
                    else {
                        alert(d.Message);
                    }
                });
            }
        });
        return false;
    },
    rolePermissionItemBatchSet: function () {
        var roleGrid;
        var curRolePermissionItemIds = []; //当前所选角色所拥有的操作权限项ID
        var setDialog = top.$.hDialog({
            title: '角色操作权限批量设置',
            width: 670, height: 600, iconCls: 'icon16_key', //cache: false,
            href: "/FrameworkModules/PermissionSet/PermissionBacthSet",
            onLoad: function () {
                using('panel', function () {
                    top.$('#panelTarget').panel({ title: '操作权限项', iconCls: 'icon-org', height: $(window).height() - 3 });
                });
                roleGrid = top.$('#leftnav').datagrid({
                    title: '所有角色',
                    url: '/FrameworkModules/RoleAdmin/GetRoleList',
                    nowrap: false, //折行
                    //fit: true,
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'ID', //主键
                    singleSelect: true, //单选
                    frozenColumns: [[]],
                    columns: [[
                        { title: '角色编码', field: 'CODE', width: 120, align: 'left' },
                        { title: '角色名称', field: 'REALNAME', width: 150, align: 'left' }
                    ]],
                    onLoadSuccess: function (data) {
                        top.$('#rightnav').tree({
                            cascadeCheck: false, //联动选中节点
                            checkbox: true,
                            lines: true,
                            url: controlPermissionItemUrl + 'GetPermissionItemTreeJson?isTree=1',
                            onSelect: function (node) {
                                top.$('#rightnav').tree('getChildren', node.target);
                            }
                        });
                        top.$('#leftnav').datagrid('selectRow', 0);
                    },
                    onSelect: function (rowIndex, rowData) {
                        curRolePermissionItemIds = '';
                        var query = 'roleId=' + rowData.ID;
                        $.ajaxtext('/FrameworkModules/PermissionSet/GetPermissionItemsByRoleId', query, function (data) {
                            var permissionItemTree = top.$('#rightnav');
                            permissionItemTree.tree('uncheckedAll');
                            if (data == '' || data.toString() == '[object XMLDocument]') {
                                return;
                            }
                            curRolePermissionItemIds = data.split(',');
                            for (var i = 0; i < curRolePermissionItemIds.length; i++) {
                                var node = permissionItemTree.tree('find', curRolePermissionItemIds[i]);
                                if (node)
                                    permissionItemTree.tree("check", node.target);
                            }
                        });
                    }
                });
            },
            submit: function () {
                var allSelectPermissionItemIds = pubMethod.getUserSelectedPermissionItems().split(',');
                var grantIds = '';
                var revokeIds = '';
                var flagRevoke = 0;
                var flagGrant = 0;

                while (flagRevoke < curRolePermissionItemIds.length) {
                    if ($.inArray(curRolePermissionItemIds[flagRevoke], allSelectPermissionItemIds) == -1) {
                        revokeIds += curRolePermissionItemIds[flagRevoke] + ','; //得到收回的权限列表
                    }
                    ++flagRevoke;
                }

                while (flagGrant < allSelectPermissionItemIds.length) {
                    if ($.inArray(allSelectPermissionItemIds[flagGrant], curRolePermissionItemIds) == -1) {
                        grantIds += allSelectPermissionItemIds[flagGrant] + ','; //得到授予的权限列表
                    }
                    ++flagGrant;
                }

                var query = 'roleId=' + top.$('#leftnav').datagrid('getSelected').ID + '&grantIds=' + grantIds + "&revokeIds=" + revokeIds;
                $.ajaxjson('/FrameworkModules/PermissionSet/SetRolePermissionItem', query, function (d) {
                    if (d.Data > 0) {
                        msg.ok('设置成功！');
                    }
                    else {
                        alert(d.Message);
                    }
                });
            }
        });
        top.$(setDialog).hLoading();
        return false;
    }
};
var pubMethod = {
    bindCtrl: function (navId) {
		var treeData = '';
		var parm = 'isTree=1';
		$.ajaxtext(controlPermissionItemUrl + 'GetPermissionItemTreeJson', parm, function (data) {
			if (data) {
				treeData = data.replace(/Id/g, 'id').replace(/FullName/g, 'text');
				treeData = '[{"id":0,"selected":true,"text":"请选择父级操作权限项"},' + treeData.substr(1, treeData.length - 1);
				top.$('#ParentId').combotree({
					data: JSON.parse(treeData),
					valueField: 'id',
					textField: 'text',
					panelWidth: '280',
					editable: false,
					lines: true,
					onSelect: function (item) {
						var nodeId = top.$('#ParentId').combotree('getValue');
						if (item.id == navId) {
							top.$('#ParentId').combotree('setValue', nodeId);
							top.$.messager.alert('警告提示', '上级操作权限不能与当前所选相同！', 'warning');
						}
					}
				}).combotree('setValue', 0);				
			}
		});	
		
		/*
        var treeData = $('body').data('permissionItemData');
        treeData = JSON.stringify(treeData).replace(/Id/g, 'id').replace(/FullName/g, 'text');
        treeData = '[{"id":0,"selected":true,"text":"请选择父级操作权限项"},' + treeData.substr(1, treeData.length - 1);

        top.$('#ParentId').combotree({
            data: JSON.parse(treeData),
            valueField: 'id',
            textField: 'text',
            panelWidth: '280',
            editable: false,
            lines: true,
            onSelect: function (item) {
                var nodeId = top.$('#ParentId').combotree('getValue');
                if (item.id == navId) {
                    top.$('#ParentId').combotree('setValue', nodeId);
                    top.$.messager.alert('警告提示', '上级操作权限不能与当前所选相同！', 'warning');
                }
            }
        }).combotree('setValue', 0);
		*/
        top.$('#Code').focus();
        top.$('#Enabled').attr("checked", true);
        top.$('#AllowEdit').attr("checked", true);
        top.$('#AllowDelete').attr("checked", true);
        top.$('#uiform').validate({
            //此处加入验证
        });
    },
    getUserSelectedPermissionItems: function () { //得到用户选择的模块       
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