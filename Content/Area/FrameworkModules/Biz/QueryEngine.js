var queryEngineGrid,
    controlQueryEngineUrl = '/FrameworkModules/QueryEngineAdmin/',
    formUrl = "/FrameworkModules/QueryEngineAdmin/";

$(function () {
    pageSizeControl.init({ gridId: 'queryEngineGrid', gridType: 'treegrid' });
    queryEngineTree.init();
    autoResize({ dataGrid: '#queryEngineGrid', gridType: 'treegrid', callback: grid.databind, height: 35, width: 230 });
    $('#a_add').attr('onclick', 'crud.add();');
    $('#a_edit').attr('onclick', 'crud.edit();');
    $('#a_delete').attr('onclick', 'crud.del();');
    $('#a_refresh').attr('onclick', 'crud.refreash();');
    $(window).resize(function () {
        pageSizeControl.init({ gridId: 'queryEngineGrid', gridType: 'treegrid' });
    });
});

var queryEngineTree = {
    init: function () {
        $('#queryEngineTree').tree({
            lines: true,
            url: controlQueryEngineUrl + 'GetQueryEngineTreeJson?isTree=1',
            animate: true,
            onLoadSuccess: function (node, data) {
                if (data.length && data.length > 0) {
                    $('body').data('queryEngineData', data);
                }
            },
            onClick: function (node) {
                $(this).tree('toggle', node.target);
            },
            onSelect: function (node) {
                var keys = queryEngineTree.getSelectedChildIds(node);
                $('#queryEngineGrid').treegrid({
                    url: controlQueryEngineUrl + 'GetQueryEngineByIds',
                    queryParams: { queryEngineIds: keys }
                });
            }
        });
    },
    data: function (opr) {
        var d = JSON.stringify($('body').data('queryEngineData'));
        if (opr === '1') {
            d = '[{"id":0,"text":"请选择父级"},' + d.substr(1);
        }
        return JSON.parse(d);
    },
    selected: function () {
        return $('#queryEngineTree').tree('getSelected');
    },
    getSelectedChildIds: function (node) {
        var children = $('#queryEngineTree').tree('getLeafChildren', node.target);
        var ids = '';
        if (children) {
            for (var i = 0; i < children.length; i++) {
                ids += children[i].id + ',';
            }
            ids = ids.substring(0, ids.length - 1);
        }
        return ids;
    },
    reLoad: function () {
        return $('#queryEngineTree').tree('reload');
    }
};

var grid = {
    databind: function (winsize) {
        queryEngineGrid = $('#queryEngineGrid').treegrid({
            toolbar: '#toolbar',
            width: winsize.width,
            height: winsize.height,
            nowrap: false,
            rownumbers: true,
            loadMsg: '正在努力加载中....',
            resizable: true,
            collapsible: false,
            onContextMenu: pageContextMenu.createTreeGridContextMenu,
            idField: 'Id',
            treeField: 'FullName',
            onDblClickRow: function (row) {
                document.getElementById('a_edit').click();
            },
            frozenColumns: [[
                { title: '名称', field: 'FullName', width: 200 },
                { title: '编码', field: 'Code', width: 130 }
            ]],
            columns: [[
                { title: 'Id', field: 'Id', hidden: true },
                { title: 'ParentId', field: 'ParentId', hidden: true },
                {
                    title: '可编辑', field: 'AllowEdit', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    }
                },          
				{
				    title: '可删除', field: 'AllowDelete', width: 50, align: 'center', formatter: function (v, d, i) {
				        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
				    }
				},
                {
                    title: '有效', field: 'Enabled', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    }
                },
                { title: '排序', field: 'SortCode', width: 80, align: 'right' },
                { title: '备注', field: 'Description', width: 500 }
            ]]
        });
    },
    reload: function (treeNode) {
        if (treeNode) {
            var keys = queryEngineTree.getSelectedChildIds(treeNode);
            if (keys !== '') {
                queryEngineGrid.treegrid({
                    url: controlQueryEngineUrl + "GetQueryEngineByIds",
                    queryParams: { queryEngineIds: keys }
                });
            }
        }
    },
    selected: function () {
        return queryEngineGrid.treegrid('getSelected');
    }
};

var crud = {
    refreash: function () {
        grid.reload(queryEngineTree.selected());
    },
    bindCtrl: function (navId) {
        var treeData = '';
        $.ajaxtext(controlQueryEngineUrl + 'GetqueryEngineTreeJson', '', function (data) {
            if (data) {
                treeData = data.replace(/Id/g, 'id').replace(/FullName/g, 'text');
                if (treeData === '[]' || !treeData) {
                    treeData = '[{"id":0,"selected":true,"text":"请选择父级"}]';
                } else {
                    treeData = '[{"id":0,"selected":true,"text":"请选择父级"},' + treeData.substr(1, treeData.length - 1);
                }

                top.$('#ParentId').combotree({
                    data: JSON.parse(treeData),
                    valueField: 'id',
                    textField: 'text',
                    panelWidth: '320',
                    editable: false,
                    lines: true,
                    onSelect: function (item) {
                        var nodeId = top.$('#ParentId').combotree('getValue');
                        if (item.id == navId) {
                            top.$('#ParentId').combotree('setValue', nodeId);
                            msg.warning('上级不能与当前相同!');
                        }
                    }
                }).combotree('setValue', 0);
            }
        });
        top.$('#Code').focus();
        top.$('#Enabled,#AllowEdit,#AllowDelete').attr("checked", true);
    },
    add: function () {
        var gridSelected = grid.selected(),
			treeSelected = queryEngineTree.selected();
        var row = grid.selected();
        if (!row) {
            row = treeSelected;
        }

        var addDialog = top.$.hDialog({
            href: formUrl + 'QueryEngineForm?n=' + Math.random(), title: '添加查询引擎', iconCls: 'icon16_table_add', width: 430, height: 300,
            onLoad: function () {
                crud.bindCtrl();
                if (treeSelected) {
                    setTimeout(function () { top.$('#ParentId').combotree('setValue', treeSelected.id); }, 300);
                }
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var queryString = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson(controlQueryEngineUrl + 'SubmitForm', queryString, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            var tmpTree = $('#queryEngineTree');
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
			treeSelected = queryEngineTree.selected();
        var row = grid.selected();
        if (!row) {
            row = treeSelected;
        }
        if (row) {
            if (row.AllowEdit == '0') {
                msg.warning('该数据不允许修改～！');
                return false;
            }
            var editDailog = top.$.hDialog({
                href: formUrl + 'QueryEngineForm?n=' + Math.random(), title: '修改查询引擎', iconCls: 'icon16_table_edit', width: 430, height: 300,
                onLoad: function () {
                    crud.bindCtrl(row.Id);
                    var parm = 'key=' + (row.Id || row.id); //(row.Id || row.id) 注意此处的用法很经典，其中一个为空就取另一个值。
                    $.ajaxjson('/FrameworkModules/QueryEngineAdmin/GetEntity', parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                        originalParentId = data.ParentId; //缓存修改前父节点
                        setTimeout(function () { top.$('#ParentId').combotree('setValue', data.ParentId); }, 300);
                    });

                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        //保存时判断当前节点所选的父节点，不能为当前节点的子节点，这样就乱套了....
                        var treeParentId = top.$('#ParentId').combotree('tree'); // 得到树对象
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
                                msg.warning('请正确选择父节点元素，不能为当前节点的子节点!');
                                return;
                            }
                        }

                        var vparentid = top.$('#ParentId').combobox('getValue');
                        var queryString = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson(controlQueryEngineUrl + 'SubmitForm?key=' + (row.Id || row.id), queryString, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                var tmpTree = $('#queryEngineTree');
                                var treeText = top.$('#FullName').val();
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
            msg.warning('请选择待修改的数据!');
            return false;
        }
        return false;
    },
    del: function () {
        var row = grid.selected();
        var treeSelected = queryEngineTree.selected();
        if (row != null) {
            if (row.AllowDelete == '0') {
                msg.warning('该数据不允许删除～！');
                return false;
            }
            var childs = queryEngineTree.getSelectedChildIds($('#queryEngineTree').tree('find', row.Id));
            if (childs && childs.length > 0) {
                msg.warning('当前节点有子节点数据，不能删除。<br> 请先删除子节点数据!');
                return false;
            }
            var query = 'key=' + row.Id;
            $.messager.confirm('询问提示', '确认要删除选中的数据吗？', function (data) {
                if (data) {
                    $.ajaxjson(controlQueryEngineUrl + 'Delete', query, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            //重新加载
                            var tmpTree = $('#queryEngineTree');
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
            msg.warning('请选择要删除的数据!');
            return false;
        }
        return false;
    }
};