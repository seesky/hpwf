var controlUrl = '/Admin/FrameworkModules/TableFieldAdmin/';

$(function () {
    var size = { width: $(window).width(), height: $(window).height() };
    mylayout.init(size);
    tableList.init();

    autoResize({ dataGrid: '#tableFieldGird', gridType: 'datagrid', callback: mygrid.databind, height: 36, width: 230 });
    $('#btnBatchSet').attr('onclick', 'TableFieldAdminMethod.BatchSet();');
    $('#btnSetTablePermission').attr('onclick', 'SetTablePermissionMethod();');
    $('#btnExport').attr('onclick', 'TableFieldAdminMethod.ExportData();');
    $('#btnRefresh').attr('onclick', 'TableFieldAdminMethod.Refreash();');
    $(window).resize(function () {
        size = { width: $(window).width(), height: $(window).height() };
        mylayout.resize(size);
    });
});

var mylayout = {
    init: function (size) {
        $('#layout').width(size.width - 4).height(size.height - 4).layout();
        var center = $('#layout').layout('panel', 'center');
        center.panel({
            onResize: function (w, h) {
                $('#tableFieldGird').datagrid('resize', { width: w - 6, height: h - 36 });
            }
        });
    },
    resize: function (size) {
        mylayout.init(size);
        $('#layout').layout('resize');
    }
};

var tableList = {
    init: function () {
        $('#tbData').datagrid({
            noheader: true,
            nowrap: false,
            rownumbers: true,
            resizable: true,
            singleSelect: true,
            collapsible: false,
            url: controlUrl + 'GetTableNameAndCode/',
            columns: [[
                 { title: '表名', field: 'TABLENAME', width: 260 },
                 { title: 'TableCode', field: 'TABLECODE', hidden: true }
            ]],
            onLoadSuccess: function (data) {
            },
            onClickRow: function (rowIndex, rowData) {
                var cc = rowData.TABLECODE;
                $('#tableFieldGird').datagrid({
                    url: controlUrl + 'GetDTByTable/',
                    queryParams: { tableCode: cc }
                });
            }
        });
    },
    selectRow: function () {
        return $('#tbData').datagrid('getSelected');
    }
};

var mygrid = {
    databind: function (size) {
        $('#tableFieldGird').datagrid({
            title: "表字段明细",
            loadMsg: "正在加载表字段明细，请稍等...",
            width: size.width,
            height: size.height,
            idfield: 'ID',
            singleSelect: true,
            striped: true,
            rownumbers: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            columns: [[
                    { field: 'ck', checkbox: true },
                    { title: 'Id', field: 'id', hidden: true },
                    { title: '英文名称', field: 'columncode', width: 130 },
                    { title: '数据类型', field: 'datatype', width: 70 },
                    { title: '中文名称', field: 'columnname', width: 130 },
                    { title: '公开', field: 'ispublic', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '访问权限', field: 'columnaccess', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '编辑权限', field: 'columnedit', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '拒绝访问', field: 'columndeney', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '启用约束', field: 'useconstraint', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '查询列', field: 'issearchcolumn', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '展示列', field: 'isexhibitcolumn', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '允许编辑', field: 'allowedit', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '允许删除', field: 'allowdelete', align: "center", width: 50, formatter: imgcheckbox },
                    { title: '有效', field: 'enabled', width: 50, align: 'center', formatter: imgcheckbox },
                    { title: '描述', field: 'description', width: 260 }
                ]]
        });
    },
    reload: function (cc) {
        $('#tableFieldGird').datagrid({
            url: controlUrl + 'GetDTByTable',
            queryParams: { tableCode:cc }
        });
    },
    selectRow: function () {
        return $('#tableFieldGird').datagrid('getSelected');
    }
};

var imgcheckbox = function (cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};

var tableFieldBacthFormatter = function (cellvalue, options, rowObject) {
    if (cellvalue) {
        if (cellvalue == '√')
            return '<font color=\"#39CB00\"><b>' + cellvalue + '</b></font>';
        else return cellvalue;
    } 
};

var lastIndex = 0;
var TableFieldAdminMethod = {
    Refreash:function() {
        var curRow = tableList.selectRow();
        if (curRow) {
            mygrid.reload(curRow.TABLECODE);
        }
        else {
            msg.warning('请选择数据表。');
        }
    },
    ExportData:function() {
        var curTableCode = tableList.selectRow();
        if (curTableCode) {
            var exportData = new ExportExcel('tableFieldGird');
            $('body').data('where', 'TABLECODE=\'' + curTableCode.TABLECODE + '\''); //指定导出条件
            exportData.go('CITABLECOLUMNS', 'SORTCODE');
        } else {
            msg.warning('请先选择要导出的数据表！');
            return false;
        }
        return false;
    },
    BatchSet: function () {
        var curTable = tableList.selectRow();
        if (!curTable) {
            msg.warning('请选择数据表！');
            return false;
        }
        var ad = top.$.hDialog({
            max: true,
            title: '表字段明细批量设置-当前数据表：' + curTable.TABLENAME,
            content: '<div style="padding:2px;overflow:hidden;"><table id="nb"></table></div>',
            toolbar: [
                { text: '全选', iconCls: 'icon16_check_box', handler: function () { TableFieldAdminMethod.btnchecked(true); } },
                { text: '取消全选', iconCls: 'icon16_check_box_uncheck', handler: function () { TableFieldAdminMethod.btnchecked(false); } },
                '-',
                { text: '编辑全部', iconCls: 'icon16_pencil', handler: function () { TableFieldAdminMethod.apply('beginEdit'); } },
                { text: '取消编辑', iconCls: 'icon16_pencil_delete', handler: function () { TableFieldAdminMethod.apply('cancelEdit'); } },
                '-',
                { text: '应用', iconCls: 'icon16_disk_multiple', handler: function () { TableFieldAdminMethod.apply('endEdit'); } }
            ],
            submit: function() {
                TableFieldAdminMethod.apply('endEdit');
                var data = TableFieldAdminMethod.getChanges(curTable);
                if (data) {
                    ad.dialog('close');
                    $.ajaxjson(controlUrl + 'TableFieldBatchSet', 'jsonData=' + data, function (d) {
                        if (d.Data > 0) {
                            msg.ok('设置成功。');
                            mygrid.reload(tableList.selectRow().TABLECODE);
                            ad.dialog('close');
                        } else {
                            alert('设置失败啦！');
                        }
                    });
                } else {
                    alert('您没有设置任何选项！');
                }
            }
        });

        var nb = top.$('#nb').treegrid({
            title: '表字段明细',
            url: '/Admin/FrameworkModules/TableFieldAdmin/GetDTForEditByTable/?tableCode=' + curTable.TABLECODE,
            height: ad.dialog('options').height - 115,
            idField: 'ID',
            treeField: 'COLUMNNAME',
            iconCls: 'icon-nav',
            nowrap: false,
            striped: true,
            rownumbers: true,
            collapsible: false,
            animate: true,
            frozenColumns: [[
                { title: '英文名称', field: 'COLUMNCODE', width: 130 },
                { title: '中文名称/描述', field: 'COLUMNNAME', width: 180 }
            ]],
            columns: [[
                    { title: '数据类型', field: 'DATATYPE', width: 80 },
                    { title: '公开', field: 'ISPUBLIC', align: "center", width: 50, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '访问权限', field: 'COLUMNACCESS', align: "center", width: 60, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '编辑权限', field: 'COLUMNEDIT', align: "center", width: 60, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '拒绝访问', field: 'COLUMNDENEY', align: "center", width: 60, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '启用约束', field: 'USECONSTRAINT', align: "center", width: 60, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '查询列', field: 'ISSEARCHCOLUMN', align: "center", width: 50, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '展示列', field: 'ISEXHIBITCOLUMN', align: "center", width: 50, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '允许编辑', field: 'ALLOWEDIT', align: "center", width: 60, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '允许删除', field: 'ALLOWDELETE', align: "center", width: 60, formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '有效', field: 'ENABLED', width: 50, align: 'center', formatter: tableFieldBacthFormatter, editor: { type: 'checkbox', options: { on: '√', off: 'x' } } },
                    { title: '描述', field: 'DESCRIPTION', width: 260 }
            ]],
            onClickRow: function (row) {
                if (lastIndex != row.ID) {
                    nb.treegrid('endEdit', lastIndex);
                }
                TableFieldAdminMethod.apply('beginEdit', row.ID);
                lastIndex = row.ID;
            },
            onContextMenu: function (e, row) {
                TableFieldAdminMethod.rowCMenu(e, row);
            }
        });
        return false;
    },
    rowCMenu: function (e, row) { //row 右键菜单
        var createRowMenu = function () {
            var rmenu = top.$('<div id="rmenu" style="width:100px;"></div>').appendTo('body');
            var menus = [
                { title: '编辑并全选', iconCls: '' }, { title: '编辑', iconCls: 'icon16_edit' }, '-',
                { title: '全选', iconCls: 'icon16_check_box' }, { title: '取消全选', iconCls: 'icon16_check_box_uncheck' }, '-',
                { title: '取消编辑', iconCls: '' }, { title: '应用', iconCls: 'icon16_ok' }
            ];
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

        top.$('#nb').treegrid('select', row.ID);
        if (lastIndex != row.ID) { nb.treegrid('endEdit', lastIndex); }
        lastIndex = row.ID;

        top.$('#rmenu').menu({
            onClick: function (item) {
                switch (item.text) {
                    case '全选': TableFieldAdminMethod.btnchecked(true); break;
                    case '取消全选': TableFieldAdminMethod.btnchecked(false); break;
                    case '编辑': TableFieldAdminMethod.apply('beginEdit', row.ID); break;
                    case '编辑并全选':
                        TableFieldAdminMethod.apply('beginEdit', row.ID);
                        TableFieldAdminMethod.btnchecked(true);
                        break;
                    case '取消编辑': TableFieldAdminMethod.apply('cancelEdit', row.ID); break;
                    case '应用': TableFieldAdminMethod.apply('endEdit', row.ID); break;
                    default:
                        break;
                }
            }
        }).menu('show', { left: e.pageX, top: e.pageY });
    },
    findCtrl: function (g, fieldname, keyId) {
        return g.treegrid('getEditor', { id: keyId, field: fieldname }).target;
    },
    btnchecked: function (flag) {
        var rows = top.$('#nb').treegrid('getSelections');
        if (rows) {
            $.each(rows, function (i, n) {
                var editors = top.$('#nb').treegrid('getEditors', n.ID);
                $.each(editors, function () {
                    if (!$(this.target).is(":hidden"))
                        $(this.target).attr('checked', flag);

                });
            });
        } else {
            msg.warning('请选择菜单。');
        }
    },
    apply: function (action, id) {
        if (!id) {
            top.$('#nb').treegrid('selectAll');
        }

        if(id){
            top.$('#nb').treegrid(action, id);
        }

        var rows = top.$('#nb').treegrid('getSelections');
        $.each(rows, function (i, n) {
            top.$('#nb').treegrid(action, this.ID);
            if (action == 'beginEdit') {
                var editors = top.$('#nb').treegrid('getEditors', n.ID);
            }
        });

        if (action != "beginEdit"){
            top.$('#nb').treegrid('clearSelections');
        }
    },
    getChanges: function (vTableField) {
        var rows = top.$('#nb').treegrid('getChildren');
        var o = { TableCode: vTableField.TABLECODE, data: [] };
        Enumerable.from(rows).forEach(function (x) {
            var rowdata = Enumerable.from(x).where('t=>t.value=="√"').select('$.key').toArray();
            if (rowdata.length > 0) {
                var n = { keyId: x.ID, subdata: [] };
                n.subdata = rowdata;
                o.data.push(n);
            }
        });
        if (o.data.length > 0){
            return JSON.stringify(o);
        }
        return "";
    }
};

function SetTablePermissionMethod() {
    var currentRole = tableList.selectRow();
    if (currentRole) {
        var rDialog = top.$.hDialog({
            href: '/Admin/FrameworkModules/TableFieldAdmin/SetTablePermission/', width: 660, height: 515, title: '设置需要做表权限控件的数据表', iconCls: 'icon16_table_lightning',
            onLoad: function () {
                top.$('#rlayout').layout();
                //top.$('#roleName').text(currentRole.REALNAME);
                top.$('#allDataTables').datagrid({
                    width: 285,
                    height: 350,
                    iconCls: 'icon16_data_table',
                    nowrap: false, //折行
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'TABLECODE', //主键
                    singleSelect: true, //单选
                    columns: [[
                       { title: '数据表', field: 'TABLENAME', width: 240 },
                       { title: 'TableCode', field: 'TABLECODE', hidden: true }
                    ]],
                    pagination: false
                });
                top.$('#selectDataTables').datagrid({
                    width: 285,
                    height: 350,
                    iconCls: 'icon16_data_table',
                    nowrap: false, //折行
                    rownumbers: true, //行号
                    striped: true, //隔行变色
                    idField: 'ID', //主键
                    singleSelect: true, //单选
                    columns: [[
                       { title: '英语名', field: 'ITEMVALUE', width: 100 },
                       { title: '中文名', field: 'ITEMNAME', width: 135 }
                    ]],
                    pagination: false
                });

                top.$('#allDataTables').datagrid({
                    url: '/Admin/FrameworkModules/TableFieldAdmin/GetTableNameAndCodeForPermission/',
                    onDblClickRow: function (rowIndex, rowData) {
                        top.$('#aSelectTable').click();
                    }
                });

                top.$('#selectDataTables').datagrid({
                    url: '/Admin/FrameworkModules/TableFieldAdmin/GetTablePermissionScopeList/',
                    onDblClickRow: function (rowIndex, rowData) {
                        top.$('#aDeleteTable').click();
                    }
                });
                top.$('#aSelectTable').click(function () {
                    var _row = top.$('#allDataTables').datagrid('getSelected');
                    if (_row) {
                        var hasUserName = false;
                        var users = top.$('#selectDataTables').datagrid('getRows');
                        $.each(users, function (i, n) {
                            if (n.ITEMVALUE == _row.TABLECODE) {
                                hasUserName = true;
                            }
                        });
                        if (!hasUserName) {
                            //top.$('#selectDataTables').datagrid('appendRow', _row);
                            var tabname = _row.TABLENAME;
                            //tabname = tabname.substring(tabname.lastIndexOf('［') + 1, tabname.lastIndexOf('］'));
                           
                            top.$('#selectDataTables').datagrid('appendRow', {
                                ITEMVALUE: _row.TABLECODE,
                                ITEMNAME: tabname
                            });

                            //添加权限控制表
                            var query = 'tableName=' + _row.TABLENAME;
                            $.ajaxjson('/Admin/FrameworkModules/TableFieldAdmin/AddTablePermissionScope/', query, function (d) {
                                if (d.Data > 0) {
                                    top.$('#allDataTables').datagrid('deleteRow', top.$('#allDataTables').datagrid('getRowIndex', _row.TABLECODE));
                                } else {
                                    msg.warning('添加失败。');
                                }
                            });
                        }
                        else {
                            alert('已存在，请不要重复添加。');
                            return false;
                        }
                    } else {
                        alert('请选择数据表');
                    }
                });
                top.$('#aDeleteTable').click(function () {
                    var trow = top.$('#selectDataTables').datagrid('getSelected');
                    if (trow) {
                        var rIndex = top.$('#selectDataTables').datagrid('getRowIndex', trow);
                        top.$('#selectDataTables').datagrid('deleteRow', rIndex).datagrid('unselectAll');
                        //移除数据表
                        var query = 'itemValue=' + trow.ITEMVALUE;
                        $.ajaxjson('/Admin/FrameworkModules/TableFieldAdmin/DeleteTablePermissionScope/', query, function (d) {
                            if (d.Data > 0 ) {
                                top.$('#allDataTables').datagrid('appendRow', {
                                    TABLENAME: trow.ITEMNAME,
                                    TABLECODE: trow.ITEMVALUE
                                    //TABLENAME: trow.ITEMVALUE + '［' + trow.ITEMNAME + '］'
                                });
                            } else {
                                msg.warning('移除失败。');
                            }
                        });
                    } else {
                        alert('请选择数据表');
                    }
                });
            },
            submit: function () {
                rDialog.dialog('close');
            }
        });
    } else {
        msg.warning('请选择一个数据表！');
    }
    return false;
}