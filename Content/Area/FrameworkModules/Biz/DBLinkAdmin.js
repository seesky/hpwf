var navgrid,
    actionUrl = '/FrameworkModules/DBLinkAdmin/',
    formUrl = "/FrameworkModules/DBLinkAdmin/Form?n=" + Math.random();

$(function () {
    autoResize({ dataGrid: '#dbLinkGrid', gridType: 'datagrid', callback: grid.databind, height: 0 });
    $('#btnAdd').attr('onclick', 'DBLinkAdminMethod.AddDBLink();');
    $('#btnEdit').attr('onclick', 'DBLinkAdminMethod.EditDBLink();');
    $('#btnDelete').attr('onclick', 'DBLinkAdminMethod.DeleteDBLink();'); 
    $('#btnRefresh').attr('onclick', 'DBLinkAdminMethod.Refreash();');
});

var grid = {
    databind: function (size) {
        navgrid = $('#dbLinkGrid').datagrid({
            title: '数据库连接列表',
            iconCls: 'icon16_database_link',
            noheader: true,
            width: size.width,
            height: size.height,
            nowrap: false,
            rownumbers: true,
            resizable: true,
            singleSelect: true,
            collapsible: false,
            onRowContextMenu:pageContextMenu.createDataGridContextMenu,
            url: actionUrl + 'GriListJson',
            idfield: 'ID',
			onDblClickRow:function(rowIndex, rowData){
				document.getElementById('btnEdit').click();
			},
            frozenColumns: [[
               { field: 'ck', checkbox: true },
               { title: '连接名称', field: 'LINKNAME', width: 150 }
            ]],
            columns: [[
                 { title: 'Id', field: 'ID', hidden: true },
                 { title: '数据库类型', field: 'LINKTYPE', width: 90 },                 
                 { title: '有效', field: 'ENABLED', width: 40, align: 'center', formatter: imgcheckbox },
                 { title: '描述', field: 'DESCRIPTION', width: 399 }
            ]]
        });
    },
    reload: function () {
        navgrid.datagrid('reload');
    },
    selected: function () {
        return navgrid.datagrid('getSelected');
    }
};

var imgcheckbox = function (cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/../../Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/../../Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};

var DBLinkAdminMethod = {
    Refreash: function () {
        grid.reload();
    },
    AddDBLink: function () {
        var addDialog = top.$.hDialog({
            title: '新增数据库连接',
            iconCls: 'icon16_database_add',
            href: formUrl,
            width: 650,
            height: 340,
            onLoad: function () {
                top.$('#Enabled').attr("checked", true);
                pageMethod.bindCategory('LinkType', 'DataBaseType');
                top.$('#LinkName').focus();
            },
            submit: function () {
                var vlinktype = top.$('#LinkType').combobox('getValue');
                if (top.$('#uiform').validate().form()) {
                    var queryString = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson(actionUrl + 'SubmitForm', queryString, function (d) {
                        if (d.Data > 0) {
                            msg.ok('新增数据库连接成功!');
                            addDialog.dialog('close');
                            grid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            }
        });
        return false;
    },
    EditDBLink: function () {
        var row = grid.selected();
        if (row) {
            var editDailog = top.$.hDialog({
                href: formUrl + '?v=' + Math.random(),
                title: '修改数据库连接',
                iconCls: 'icon16_database_edit',
                width: 650,
                height: 340,
                onLoad: function () {
                    pageMethod.bindCategory('LinkType', 'DataBaseType');            
                    var parm = 'key=' + row.ID;
                    $.ajaxjson(actionUrl + 'GetEntity', parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                    });
                    top.$('#LinkName').focus();
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        var queryString = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson(actionUrl + 'SubmitForm?key=' + row.ID, queryString, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                editDailog.dialog('close');
                                grid.reload();
                            } else {
                                MessageOrRedirect(d);
                            }
                        });
                    }
                }
            });
        }
        else {
            msg.warning('请选择待修改的数据。');
        }
        return false;
    },
    DeleteDBLink: function () {
        var row = grid.selected();
        if (row) {
            $.messager.confirm('询问提示', '确认要删除[' + row.LINKNAME + ']数据库连接吗?', function (data) {
                if (data) {
                    $.ajaxjson(actionUrl + 'Delete', 'key=' + row.ID, function (d) {
                        if (d.Data > 0) {
                            msg.ok('数据库连接删除成功。');
                            grid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            });
        } else {
            msg.warning('请选择待删除的数据。');
        }
        return false;
    }
};