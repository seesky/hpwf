var moduleGrid,
    controlModuleUrl = '/Admin/FrameworkModules/ModuleAdmin/',
    formUrl = "/Admin/FrameworkModules/ModuleAdmin/Form/";

$(function () {	
	pageSizeControl.init({gridId:'moduleGrid',gridType:'treegrid'});
    moduleTree.init();	
    autoResize({ dataGrid: '#moduleGrid', gridType: 'treegrid', callback: grid.databind, height: 35, width: 230 });
    $('#a_add').attr('onclick', 'crud.add();');
    $('#a_edit').attr('onclick', 'crud.edit();');
    $('#a_delete').attr('onclick', 'crud.del();');
    $('#a_refresh').attr('onclick', 'crud.refreash();');
    $('#a_setusermodulepermission').attr('onclick', 'crud.userModulePermissionBatchSet();');
    $('#a_setrolemodulepermission').attr('onclick', 'crud.roleModulePermissionBatchSet();');
    $('#a_moduleconfig').attr('onclick', 'crud.moduleconfig();');
    
	$(window).resize(function () {        
		pageSizeControl.init({gridId:'moduleGrid',gridType:'treegrid'});
    });	
});

var moduleTree = {
    init: function () {
        $('#moduleTree').tree({
            lines: true,
            url: controlModuleUrl + 'GetModuleTreeJson/?isTree=1',
            animate: true,
            onLoadSuccess: function (node, data) {
				if(data.length && data.length>0){					
					$('body').data('moduleData', data);
				}
            },
            onClick: function (node) {
                $(this).tree('toggle', node.target);
            },
            onExpand:function(node) {
                var keys = moduleTree.getSelectedChildIds(node);
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
                var keys = moduleTree.getSelectedChildIds(node);
                $('#moduleGrid').treegrid({
                    url: controlModuleUrl + 'GetModuleByIds/',
                    queryParams: { moduleIds: keys }
                }); 
            }
        });
    },
    data: function (opr) {
        var d = JSON.stringify($('body').data('moduleData'));
        if (opr === '1') {
            d = '[{"id":0,"text":"请选择父级模块（菜单）"},' + d.substr(1);
        }
        return JSON.parse(d);
    },
    selected: function () {        
        return $('#moduleTree').tree('getSelected');
    },
    getSelectedChildIds:function(node) {
        var children = $('#moduleTree').tree('getLeafChildren', node.target);
        var ids = '';
        if (children) {
            for (var i = 0; i < children.length; i++) {
                ids += children[i].id + ',';
            }
        }
        return ids;
    }, 
    reLoad: function () {
        return $('#moduleTree').tree('reload');
    }
};

var grid = {
    databind: function (winsize) {
        moduleGrid = $('#moduleGrid').treegrid({
            toolbar: '#toolbar',
            width: winsize.width,
            height: winsize.height,
            nowrap: false,
            rownumbers: true,
            loadMsg:'正在努力加载中....',
            //animate: true,
            resizable: true,
            collapsible: false,
            onContextMenu: pageContextMenu.createTreeGridContextMenu,
            //url: controlModuleUrl,
            idField: 'id',
            treeField: 'fullname',
			onDblClickRow:function(row){
				document.getElementById('a_edit').click();
			},
            frozenColumns: [[
                { title: '模块（菜单）名称', field: 'fullname', width: 200 },
                { title: '编码', field: 'code', width: 130 }
            ]],
            columns: [[
                { title: 'Id', field: 'id', hidden: true },
                { title: 'ParentId', field: 'parentid', hidden: true },
                { title: '模块分类', field: 'category', width: 100 },
                { title: '图标', field: 'iconcss', width: 130, hidden: true },
                { title: 'Web链接地址', field: 'navigateurl', width: 200 },
                { title: 'WinForm程序集', field: 'assemblyname', width: 150 },
                { title: 'WinForm窗体', field: 'formname', width: 200 },
                {
                    title: '模块类型', field: 'moduletype', width: 60, align: 'center', formatter: function (v, d, i) {
                        if (v == 1) {
                            return '<img src="/Content/images/' + "winform.png" + '" />';
                        }
                        else if (v == 2) {
                            return '<img src="/Content/images/' + "webform.png" + '" />';
                        }
                        else if (v == 3) {
                            return '<img src="/Content/images/' + "winwebform.png" + '" />';
                        }
                        else {
                            return '<img src="/Content/images/' + "otherform.png" + '" />';
                        }
                    }
                },
                {
                    title: '公共', field: 'ispublic', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    }
                },
				{
                    title: '可删', field: 'allowdelete', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    }
                },
                { 
                    title: '有效', field: 'enabled', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    } 
                },
                { title: '菜单', field: 'ismenu', width: 50, align: 'center', formatter: imgcheckbox },
                { title: '排序', field: 'sortcode', width: 80, align: 'right' },
                { title: '备注', field: 'description', width: 500 },
            //{ title: 'AllowEdit', field: 'AllowEdit', hidden: true },
                {title: 'AllowDelete', field: 'allowdelete', hidden: true }
            //{ title: 'ModuleType', field: 'ModuleType', hidden: true }
            ]]
        });
    },
    reload: function (treeNode) {
        if (treeNode) {
            var keys = moduleTree.getSelectedChildIds(treeNode);
            if (keys !== '') {
                moduleGrid.treegrid({
                    url: controlModuleUrl + "GetModuleByIds/",
                    queryParams: { moduleIds: keys }
                });
            }
        }
    },
    selected: function () {
        return moduleGrid.treegrid('getSelected');
    }
};

var imgcheckbox = function(cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};

var showIcon = function () {
    top.$('#selecticon').click(function () {
        var iconDialog = top.$.hDialog({
            iconCls: 'icon16_application',
            href: '/Content/Styles/iconModuleList.htm?v=' + Math.random(),
            title: '选取图标', width: 800, height: 600, showBtns: false,
            onLoad: function () {
                top.$('#iconlist li').attr('style', 'float:left;border:1px solid #fff;margin:2px;width:16px;cursor:pointer').click(function () {
                    //var iconCls = top.$(this).find('span').attr('class').replace('icon ', '');
                    var iconCls = top.$(this).find('span').attr('class');
                    top.$('#iconcss').val(iconCls);
                    top.$('#iconurl').val(top.$(this).attr('title'));
                    //top.$('#smallIcon').attr('class', "icon " + iconCls);
                    top.$('#smallicon').attr('class', iconCls);

                    iconDialog.dialog('close');
                }).hover(function () {
                    top.$(this).css({ 'border': '1px solid red' });
                }, function () {
                    top.$(this).css({ 'border': '1px solid #fff' });
                });
                //top.$('#btnicon').click(function() {
                //    $.get(controlModuleUrl, 'action=buildIcon', function(d) {
                //        top.$.hDialog({
                //            content: '<textarea style="width:100%;height:100%;">' + d + '</textarea>',
                //            max: true
                //        });
                //    });

                //});
            }
        });
    });
};

function createParam(action, keyid, ids) {
    var o = {};
    var query = top.$('#uiform').serializeArray();
    query = convertArray(query);
    o.jsonEntity = JSON.stringify(query);
    o.action = action;
    o.keyid = keyid;
    if (ids)
        o.keyids = ids;
    else {
        o.keyids = '';
    }
    return "json=" + JSON.stringify(o);
}

function getChildNodes(treeNodeId, result) {
    var childrenNodes = moduleGrid.treegrid('getChildren', treeNodeId);
    if (childrenNodes) {
        for (var i = 0; i < childrenNodes.length; i++) {
            result.push(childrenNodes[i].KeyId);
            result = getChildNodes(childrenNodes[i].KeyId, result);
        }
    }
    return result;
};

var setTreeValue = function (id) {
	top.$('#parentid').combotree('setValue', id);
};

var crud = {
    refreash: function () {
        grid.reload(moduleTree.selected());
    },
    bindCtrl: function (navId) {
        var treeData = '';
        $.ajaxtext(controlModuleUrl + 'GetModuleTreeJson/', '', function (data) {
            if (data) {
                treeData = data.replace(/id/g, 'id').replace(/fullname/g, 'text');
                treeData = '[{"id":0,"selected":true,"text":"请选择父级模块（菜单）"},' + treeData.substr(1, treeData.length - 1);
                top.$('#parentid').combotree({
                    data: JSON.parse(treeData),
                    valueField: 'id',
                    textField: 'text',
                    panelWidth: '280',
                    editable: false,
                    lines: true,
                    onSelect: function (item) {
                        var nodeId = top.$('#parentid').combotree('getValue');
                        if (item.id == navId) {
                            top.$('#parentid').combotree('setValue', nodeId);
                            top.$.messager.alert('警告提示', '上级模块不能与当前模块相同！', 'warning');
                        }
                    }
                }).combotree('setValue', 0);
            }
        });
        /*
        var treeData = $('body').data('moduleData'); //moduleGrid.treegrid('getData');
        treeData = JSON.stringify(treeData).replace(/Id/g, 'id').replace(/FullName/g, 'text');
        treeData = '[{"id":0,"selected":true,"text":"请选择父级模块（菜单）"},' + treeData.substr(1, treeData.length - 1);
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
        top.$.messager.alert('警告提示', '上级模块不能与当前模块相同！', 'warning');
        }
        }
        }).combotree('setValue', 0);
        */

        showIcon(); //选取图标
        //top.$('#SortCode').numberspinner();
        top.$('#code').focus();
        top.$('#enabled,#allowedit,#allowdelete').attr("checked", true);
        top.$('#uiform').validate({
            //此处加入验证
        });
    },
    add: function () {
        var gridSelected = grid.selected(),
			treeSelected = moduleTree.selected();
        var row = grid.selected();
        if (!row) {
            row = treeSelected;
        }

        var addDialog = top.$.hDialog({
            href: formUrl, title: '添加模块（菜单）', iconCls: 'icon16_tab_add', width: 500, height: 540,
            onLoad: function () {
                crud.bindCtrl();
                pageMethod.bindCategory('category', 'ModuleCategory');
                pageMethod.bindCategory('moduletype', 'ModuleType');
                top.$('#moduletype').combobox('setValue', '2');
                if (treeSelected) {
                    setTimeout(function () { setTreeValue(treeSelected.id); }, 300);
                    //top.$('#ParentId').combotree('setValue', treeSelected.id);
                }
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var queryString = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson(controlModuleUrl + 'SubmitForm/', queryString, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            var tmpTree = $('#moduleTree');
                            var iconCss = top.$('#iconcss').val();
                            var treeText = top.$('#fullname').val();
                            if (iconCss) {
                                iconCss = iconCss.replace('icon ', '');
                            } else {
                                iconCss = 'icon-note';
                            }

                            if (treeSelected) {
                                tmpTree.tree('append', {
                                    parent: treeSelected.target,
                                    data: [{
                                        id: d.Data,
                                        text: treeText,
                                        iconCls: iconCss
                                    }]
                                });
                            }
                            grid.reload(treeSelected);
                            addDialog.dialog('close');
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            }
        });
        return false;
    },
    edit: function () {
        var originalParentId = '', //修改前父节点
			gridSelected = grid.selected(),
			treeSelected = moduleTree.selected();
        var row = grid.selected();
        if (!row) {
            row = treeSelected;
        }

        if (row) {
            var editDailog = top.$.hDialog({
                href: formUrl, title: '修改模块（菜单）', iconCls: 'icon16_tab_edit', width: 500, height: 540,
                onLoad: function () {
                    crud.bindCtrl(row.Id);
                    pageMethod.bindCategory('category', 'ModuleCategory');
                    pageMethod.bindCategory('moduletype', 'ModuleType');
                    var parm = 'key=' + (row.Id || row.id); //(row.Id || row.id) 注意此处的用法很经典，其中一个为空就取另一个值。                   
                    $.ajaxjson('/Admin/FrameworkModules/ModuleAdmin/GetEntity/', parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                        originalParentId = data.parentid; //缓存修改前父节点
                        setTimeout(function () { setTreeValue(data.parentid); }, 300);
                    });
                    
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        //保存时判断当前节点所选的父节点，不能为当前节点的子节点，这样就乱套了....
                        var treeParentId = top.$('#parentid').combotree('tree'); // 得到树对象
                        var node = treeParentId.tree('getSelected');
                        if (node) {
                            var nodeParentId = treeParentId.tree('find', (row.Id || row.id));
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
                                top.$.messager.alert('温馨提示', '请正确选择父节点元素，不能为当前节点的子节点!', 'warning');
                                return;
                            }
                        }

                        var vcategory = top.$('#category').combobox('getValue');
                        var vparentid = top.$('#parentid').combobox('getValue');
                        var vmoduletype = top.$('#moduletype').combobox('getValue');
                        if (!vmoduletype || vmoduletype == 'undefined') {
                            top.$.messager.alert('温馨提示', '请选择模块类型！', 'warning');
                            return;
                        }

                        var queryString = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson(controlModuleUrl + 'SubmitForm/?key=' + (row.Id || row.id), queryString, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                var tmpTree = $('#moduleTree');
                                var iconCss = top.$('#iconcss').val();
                                var treeText = top.$('#fullname').val();
                                if (iconCss) {
                                    iconCss = iconCss.replace('icon ', '');
                                } else {
                                    iconCss = 'icon-note';
                                }
                                if (gridSelected) { //A、单击的是dataGrid进行修改
                                    var curnode = tmpTree.tree('find', row.id);
                                    tmpTree.tree('update', {
                                        target: curnode.target,
                                        text: treeText,
                                        iconCls: iconCss
                                    });
                                    //1、改变父节点的情况：
                                    //1.1、判断左侧树的选择节点（即父节点）与当前保存的父节点不一样，则要做相应的移动处理。
                                    if (vparentid != '0' && treeSelected.id !== vparentid) {
                                        //移除当前父节点下移动的子节点
                                        tmpTree.tree('remove', tmpTree.tree('find', row.id).target);
                                        //修改的父节点树下增加节点
                                        tmpTree.tree('append', {
                                            parent: tmpTree.tree('find', vparentid).target,
                                            data: [{
                                                id: row.id,
                                                text: treeText,
                                                iconCls: iconCss
                                            }]
                                        });
                                    }
                                } else { //B、单击的是Tree进行修改
                                    tmpTree.tree('update', {
                                        target: treeSelected.target,
                                        text: treeText,
                                        iconCls: iconCss
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
                                                    id: row.id,
                                                    text: treeText,
                                                    iconCls: iconCss
                                                }]
                                            });
                                        }
                                    }
                                }
                                grid.reload(treeSelected);
                                editDailog.dialog('close');
                            } else {
                                MessageOrRedirect(d);
                            }
                        });
                    }
                }
            });
        } else {
            msg.warning('请选择待修改模块（菜单）!');
            return false;
        }
        return false;
    },
    del: function () {
        var row = grid.selected();
        var treeSelected = moduleTree.selected();
        if (row != null) {
            if (row.AllowDelete == '0') {
                msg.warning('该模块不允许被删除～！');
                return false;
            }
            var childs = moduleTree.getSelectedChildIds($('#moduleTree').tree('find', row.id));
            if (childs && childs.length > 0) {
                $.messager.alert('警告提示', '当前模块有子模块数据，不能删除。<br> 请先删除子模块数据!', 'warning');
                return false;
            }
            var query = 'key=' + row.id;
            $.messager.confirm('询问提示', '确认要删除选中的模块（菜单）吗？', function (data) {
                if (data) {
                    $.ajaxjson(controlModuleUrl + 'Delete/', query, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            //重新加载
                            var tmpTree = $('#moduleTree');
                            var curnode = tmpTree.tree('find', row.Id);
                            if (curnode) {
                                tmpTree.tree('remove', curnode.target);
                            }
                            grid.reload(treeSelected);
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
            msg.warning('请选择要删除的模块!');
            return false;
        }
        return false;
    },
    userModulePermissionBatchSet: function () { //用户模块（菜单）权限批量设置
        var userGrid;
        var curUserModuleIds = []; //当前所选用户所拥有的模块ID
        var setDialog = top.$.hDialog({
            title: '用户模块（菜单）权限批量设置',
            width: 670, height: 600, iconCls: 'icon16_user_gladiator', //cache: false,
            href: "/Admin/FrameworkModules/PermissionSet/PermissionBacthSet/",
            onLoad: function () {
                using('panel', function () {
                    top.$('#panelTarget').panel({ title: '模块（菜单）', iconCls: 'icon-org', height: $(window).height() - 3 });
                });
                userGrid = top.$('#leftnav').datagrid({
                    title: '所有用户',
                    url: '/Admin/FrameworkModules/UserAdmin/GetUserListJson/',
                    nowrap: false, //折行
                    //fit: true,
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'id', //主键
                    singleSelect: true, //单选
                    frozenColumns: [[]],
                    columns: [[
                        { title: '登录名', field: 'username', width: 120, align: 'left' },
                        { title: '用户名', field: 'realname', width: 150, align: 'left' }
                    ]],
                    onLoadSuccess: function (data) {
                        top.$('#rightnav').hLoading();
                        top.$('#rightnav').tree({
                            cascadeCheck: false, //联动选中节点
                            checkbox: true,
                            lines: true,
                            url: '/Admin/FrameworkModules/ModuleAdmin/GetModuleTreeJson/?isTree=1',
                            onSelect: function (node) {
                                top.$('#rightnav').tree('getChildren', node.target);
                            }, onLoadSuccess: function (node, data) {
                                top.$('#rightnav').hLoading.hide();
                            }
                        });
                        top.$('#leftnav').datagrid('selectRow', 0);
                    },
                    onSelect: function (rowIndex, rowData) {
                        curUserModuleIds = [];
                        var query = 'userId=' + rowData.id;
                        $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetModuleByUserId/', query, function (data) {
                            var moduelTree = top.$('#rightnav');
                            moduelTree.tree('uncheckedAll');
                            if (data == '' || data.toString() == '[object XMLDocument]') {
                                return;
                            }
                            curUserModuleIds = data.split(',');
                            for (var i = 0; i < curUserModuleIds.length; i++) {
                                var node = moduelTree.tree('find', curUserModuleIds[i]);
                                if (node)
                                    moduelTree.tree("check", node.target);
                            }
                        });
                    }
                });
            },
            submit: function () {
                var allSelectModuledIds = permissionMgr.getUserSelectedModule().split(',');
                var grantModuleIds = '';
                var revokeModuleIds = '';
                var flagRevoke = 0;
                var flagGrant = 0;
                while (flagRevoke < curUserModuleIds.length) {
                    if ($.inArray(curUserModuleIds[flagRevoke], allSelectModuledIds) == -1) {
                        revokeModuleIds += curUserModuleIds[flagRevoke] + ','; //得到收回的权限列表
                    }
                    ++flagRevoke;
                }

                while (flagGrant < allSelectModuledIds.length) {
                    if ($.inArray(allSelectModuledIds[flagGrant], curUserModuleIds) == -1) {
                        grantModuleIds += allSelectModuledIds[flagGrant] + ','; //得到授予的权限列表
                    }
                    ++flagGrant;
                }

                var query = 'userId=' + top.$('#leftnav').datagrid('getSelected').id + '&grantIds=' + grantModuleIds + "&revokeIds=" + revokeModuleIds;
                $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetUserModulePermission/', query, function (d) {
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
    roleModulePermissionBatchSet: function () { //角色模块（菜单）权限批量设置
        var roleGrid;
        var curRoleModuleIds = []; //当前所选角色所拥有的模块ID
        var setDialog = top.$.hDialog({
            title: '角色模块（菜单）权限批量设置',
            width: 670, height: 600, iconCls: 'icon16_group_key', //cache: false,
            href: "/Admin/FrameworkModules/PermissionSet/PermissionBacthSet/",
            onLoad: function () {
                using('panel', function () {
                    top.$('#panelTarget').panel({ title: '模块（菜单）', iconCls: 'icon-org', height: $(window).height() - 3 });
                });
                roleGrid = top.$('#leftnav').datagrid({
                    title: '所有角色',
                    url: '/Admin/FrameworkModules/RoleAdmin/GetRoleList/',
                    nowrap: false, //折行
                    //fit: true,
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'id', //主键
                    singleSelect: true, //单选
                    frozenColumns: [[]],
                    columns: [[
                        { title: '角色编码', field: 'code', width: 120, align: 'left' },
                        { title: '角色名称', field: 'realname', width: 150, align: 'left' }
                    ]],
                    onLoadSuccess: function (data) {
                        top.$('#rightnav').hLoading();
                        top.$('#rightnav').tree({
                            cascadeCheck: false, //联动选中节点
                            checkbox: true,
                            lines: true,
                            url: '/Admin/FrameworkModules/ModuleAdmin/GetModuleTreeJson/?isTree=1',
                            onSelect: function (node) {
                                top.$('#rightnav').tree('getChildren', node.target);
                            }, onLoadSuccess: function (node, data) {
                                top.$('#rightnav').hLoading.hide();
                            }
                        });
                        top.$('#leftnav').datagrid('selectRow', 0);
                    },
                    onSelect: function (rowIndex, rowData) {
                        curRoleModuleIds = [];
                        var query = 'roleId=' + rowData.id;
                        $.ajaxtext('/Admin/FrameworkModules/PermissionSet/GetModuleByRoleId/', query, function (data) {
                            var moduelTree = top.$('#rightnav');
                            moduelTree.tree('uncheckedAll');
                            if (data == '' || data.toString() == '[object XMLDocument]') {
                                return;
                            }
                            curRoleModuleIds = data.split(',');
                            for (var i = 0; i < curRoleModuleIds.length; i++) {
                                var node = moduelTree.tree('find', curRoleModuleIds[i]);
                                if (node)
                                    moduelTree.tree("check", node.target);
                            }
                        });
                    }
                });
            },
            submit: function () {
                var allSelectModuledIds = permissionMgr.getUserSelectedModule().split(',');
                var grantModuleIds = '';
                var revokeModuleIds = '';
                var flagRevoke = 0;
                var flagGrant = 0;
                while (flagRevoke < curRoleModuleIds.length) {
                    if ($.inArray(curRoleModuleIds[flagRevoke], allSelectModuledIds) == -1) {
                        revokeModuleIds += curRoleModuleIds[flagRevoke] + ','; //得到收回的权限列表
                    }
                    ++flagRevoke;
                }

                while (flagGrant < allSelectModuledIds.length) {
                    if ($.inArray(allSelectModuledIds[flagGrant], curRoleModuleIds) == -1) {
                        grantModuleIds += allSelectModuledIds[flagGrant] + ','; //得到授予的权限列表
                    }
                    ++flagGrant;
                }
                var query = 'roleId=' + top.$('#leftnav').datagrid('getSelected').id + '&grantIds=' + grantModuleIds + "&revokeIds=" + revokeModuleIds;
                $.ajaxjson('/Admin/FrameworkModules/PermissionSet/SetRoleModulePermission/', query, function (d) {
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
    moduleconfig: function () {  //模块配置
        var setDialog = top.$.hDialog({
            title: '模块（菜单）配置',
            width: 380, height: 500, iconCls: 'icon16_tab_content_vertical',
            content: htmlModuleConfig(),
            submit: function () {

            }
        });
        top.$(setDialog).hLoading();
        var treemodule = top.$('#contentArea').tree({
            cascadeCheck: false, //联动选中节点
            checkbox: true,
            lines: true,
            url: '/Admin/FrameworkModules/ModuleAdmin/GetModuleTreeJson/?isTree=1',
            onLoadSuccess: function (node, data) {
                top.$.hLoading.hide(); //加载完毕后隐藏loading
                //alert('模块加载成功，改功能模块尚示完成！');
            },
            onSelect: function (node) {
                top.$('#contentArea').tree('getChildren', node.target);
            },
            onDblClick: function (node) { //双击节点选中节点及期子节点
                var t = top.$('#contentArea');
                t.tree('check', node.target);
                function checkNodes(n) {
                    var childNodes = t.tree('getChildren', n.target);
                    $.each(childNodes, function () {
                        t.tree('check', this.target);
                        t.tree('checkedAll', this.target);
                        checkNodes(this);
                    });
                }

                checkNodes(node);
            }
        });
        return false;
    }
};

function htmlModuleConfig() {
    var html = '<div class="hint-info">';
    html += '<div class="hint-tip icon16_tip"></div>';
    html += '<div>温馨提示：设置后请点“确定”按钮保存当前的设置。</div>';
    html += '</div>';
    html += '<div style="margin:10px 0;"></div>';
    html += '<div class="easyui-panel" style="width:330px;padding:5px;">';
    //html += '<div class="easyui-layout" fit=true>';
    //html += '<div region="center" style="width:290px;padding:10px">';
    html += '<table id="contentArea"  style="width:310px;padding-top:2px;"></table></div>';
    //html += '</div> </div>';
    return html;
}

var permissionMgr = {
    getUserSelectedModule: function () { //得到用户选择的模块       
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

var moveGridRow = {
    Up: function (jq) {
        var rowindex = jq.datagrid('getSelectedIndex');
        if (rowindex > -1) {
            var rows = jq.datagrid('getRows');
            var newRowIndex = rowindex - 1;
            if (newRowIndex < 0)
                newRowIndex = 0;

            var targetRow = rows[newRowIndex];
            var currentRow = rows[rowindex];

            rows[newRowIndex] = currentRow;
            rows[rowindex] = targetRow;

            jq.datagrid('loadData', rows);
            jq.datagrid('selectRow', newRowIndex);

        } else
            alert('亲，都到顶啦，在点就可以见到天宫1号啦！');
    },
    Down: function (jq) {
        var rowindex = jq.datagrid('getSelectedIndex');
        var rows = jq.datagrid('getRows');
        if (rowindex < rows.length - 1) {
            var newRowIndex = rowindex + 1;

            var targetRow = rows[newRowIndex];
            var currentRow = rows[rowindex];

            rows[newRowIndex] = currentRow;
            rows[rowindex] = targetRow;

            jq.datagrid('loadData', rows);
            jq.datagrid('selectRow', newRowIndex);

        } else
            alert('亲，到底啦，在点就罢工啦！');
    },
    Insert: function (ljq, rjq) {
        var rows = ljq.datagrid('getSelected');
        if (rows) {
            var currRows = rjq.datagrid('getRows');
            var hasBtns = Enumerable.from(currRows).where("x=>x.KeyId==" + rows.KeyId).select("$").toArray();
            if (hasBtns.length > 0)
                return false;
            else {
                rjq.datagrid('appendRow', rows);
            }
        } else {
            alert('请选择按钮。');
            return false;
        }
        return false;
    },
    Remove: function (jq) {
        var rowindex = jq.datagrid('getSelectedIndex');
        if (rowindex > -1)
            jq.datagrid('deleteRow', rowindex);
        return false;
    }
};