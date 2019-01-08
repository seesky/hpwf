$(function () {
    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.databind, height: 5 });
    $('#btnDelete').attr('onclick', 'DeleteException();');
    $('#btnDeleteAll').attr('onclick', 'ClearException();');
    $('#btnViewDetail').attr('onclick', 'ViewExceptionDetail();');
    $('#btnRefresh').attr('onclick', 'Refreash();');
    $('#btnExport').attr('onclick', 'ExportData();');
});

var mygrid = {
    databind: function(size) {
        grd = $('#list').datagrid({
            url: "/FrameworkModules/ExceptionAdmin/GridPageListJson",
            toolbar: '#toolbar',
            width: size.width,
            height: size.height,
            idField: 'ID',
            sortName: 'CREATEON',
            sortOrder: 'desc',
            striped: true,
            pagination: true,
            singleSelect: false,
            selectOnCheck: true,
            checkOnSelect: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            pageSize: 20,
            pageList: [20, 10, 30, 50],
			onDblClickRow:function(rowIndex, rowData){
				document.getElementById('btnViewDetail').click();
			},
            columns: [[
                { field: 'ck', checkbox: true },
                { title: '发生日期', field: 'CREATEON', width: 150 },
                { title: '异常信息来源', field: 'CREATEBY', width: 100 },
                { title: '异常信息', field: 'THREADNAME', width: 200 },
                { title: '异常信息描述', field: 'MESSAGE', width: 500 },
                { title: 'FORMATTEDMESSAGE', field: 'FORMATTEDMESSAGE', hidden: true },
                { title: 'ID', field: 'ID', hidden: true }
            ]],
            onDblClickRow: function(rowIndex, rowData) {
                showExceptionInfo(rowData);
            }
        });
    },
    reload:function() {
        grd.datagrid('reload', {});
    },
    getSelectedRow: function () {
        return grd.datagrid('getSelected');
    }
};

var Refreash = function () {
    mygrid.reload();
};

var ExportData = function() {
    var exportData = new ExportExcel('list');
    exportData.go('CIEXCEPTION', 'CREATEON');
};

//清空全部异常数据
var ClearException = function () {
    if (confirm('确定清空所有异常数据吗？')) {
        $.ajaxjson('/FrameworkModules/ExceptionAdmin/DeleteAll', "", function (data) {
            if (d.Data > 0) {
                msg.ok('清空异常数据成功！');
                mygrid.reload();
            }
            else {
                msg.warning(msg);
            }
        });
    }
    return false;
};

//删除所选异常记录
var DeleteException = function () {
    var checkedItems = $('#list').datagrid('getChecked');
    var keys = [];
    $.each(checkedItems, function (index, item) {
        keys.push(item.ID);
    });

    if (keys.length > 0) {
        $.messager.confirm('询问提示', '确认删除所选异常记录吗？', function (data) {
            if (data) {
                $.ajaxjson('/FrameworkModules/ExceptionAdmin/Delete', "keys=" + keys.join(','), function (d) {
                    if (d.Data > 0) {
                        msg.ok('所选异常删除成功！');
                        mygrid.reload();
                    } else {
                        msg.warning(d);
                    }
                });
            }
        });
    } else {
        msg.warning('请选择要删除的异常记录。');
    }
    return false;
};

var ViewExceptionDetail = function () {
    var selectRow = mygrid.getSelectedRow();
    if (selectRow != null) {
        showExceptionInfo(selectRow);
    } else {
        msg.warning('请选择一条异常记录。');
    }
    return false;
};

var showExceptionInfo = function (oExceptionInfo) {
    //弹窗
    top.$('#w').hWindow({ html: editFormHtml, width: 630, height: 510, title: '系统异常详细信息', iconCls: 'icon16_table_error', submit: function () { top.$('#w').window('close'); } });
    //初始化相关数据
    top.$('#txtUserName').val(oExceptionInfo.CREATEBY);
    top.$('#txtCreateOn').val(oExceptionInfo.CREATEON);
    top.$('#txtFormattedMessage').val(oExceptionInfo.FORMATTEDMESSAGE);
};

var editFormHtml = '<form  id="uiform"><table class="grid2"  cellspacing=1 width=100%>';
    editFormHtml += '<tr><td>用户：</td><td><input  id="txtUserName"  name="UserName" required="true" type="text" class="txt03" /></td></tr>';
    editFormHtml += '<tr><td>发生日期：</td><td><input id="txtCreateOn" name="CreateOn"  required="true" type="text" class="txt03" /></td></tr>';
    editFormHtml += '<tr><td>错误信息：</td><td><textarea  id="txtFormattedMessage" style="width:500px; height:330px;" name="FormattedMessage" class="txt03" /></td></tr>';
    editFormHtml += '</table></form>';