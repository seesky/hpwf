/*
RDIFramework.NET，基于.NET的快速信息化系统开发、整合框架，给用户和开发者最佳的.Net框架部署方案。
框架官网：http://www.rdiframework.net/
框架博客：http://blog.rdiframework.net/
交流QQ：406590790 
邮件交流：406590790@qq.com

其他博客：
http://www.cnblogs.com/huyong 
http://blog.csdn.net/chinahuyong


* RDIFramework.NET框架“序列管理”业务界面逻辑
*
* 主要完成序列的增加、修改、删除、导出等。
* 修改记录：
*   1、 2015-08-05 EricHu V3.0 新增本业务逻辑的编写。
*/

var controlUrl = '/FrameworkModules/SequenceAdmin/',
    formUrl = '/FrameworkModules/SequenceAdmin/Form?n=' + Math.random();

$(function () {
    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.bindGrid, height: 5 });

    $('#a_refresh').click(function () { //刷新
        mygrid.reload();
    });
    $('#a_add').attr('onclick', 'SequenceAdmin.AddSequence();');
    $('#a_edit').attr('onclick', 'SequenceAdmin.EditSequence();');  //修改序列
    $('#a_del').attr('onclick', 'SequenceAdmin.DelSequence();');  //删除序列
    $('#a_export').attr('onclick', "exportData();");
});

var exportData = function () {
    var exportData = new ExportExcel('list');
    exportData.go('CISEQUENCE', 'CREATEON');
};

var navgrid;
var mygrid = {
    bindGrid: function (size) {
        navgrid = $('#list').datagrid({
            url: controlUrl + 'GridPageListJson',
            toolbar: '#toolbar',
            width: size.width,
            height: size.height,
            idField: 'ID',
            sortName: 'CREATEON',
            sortOrder: 'desc',
            singleSelect: true,
            striped: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            pagination: true,
            rownumbers: true,
            pageSize: 20,
            pageList: [20, 10, 30, 50],
            rowStyler: function (index, row) {
                if (row.ENABLED <= 0) {
                    return 'color:#999;'; //显示为灰色字体
                }
            },
            onDblClickRow: function (rowIndex, rowData) {
                document.getElementById('a_edit').click();
            },
            columns: [[
                { field: 'ck', checkbox: true },
                { title: '名称', field: 'FULLNAME', width: 150, sortable: true },
                { title: '前缀', field: 'PREFIX', width: 130 },
                { title: '分隔符', field: 'SEPARATE', width: 80 },
                { title: '增序列', field: 'SEQUENCE', width: 100 },
                { title: '减序列', field: 'REDUCTION', width: 100 },
                { title: '步骤', field: 'STEP', width: 80 },
                { title: '描述', field: 'DESCRIPTION', width: 300 }
            ]]
        });
    },
    reload: function () {
        navgrid.datagrid('reload', {});
    },
    selected: function () {
        return navgrid.datagrid('getSelected');
    }
};

var SequenceAdmin = {
    AddSequence: function () { //新增序列
        var addDailog = top.$.hDialog({
            title: '添加序列', width: 295, height: 365, href: formUrl, iconCls: 'icon16_table_add',
            onLoad: function () {
                top.$('#Sequence').numberbox('setValue', 1000001);
                top.$('#Reduction').numberbox('setValue',9999999);
                top.$('#Step').numberbox('setValue', 1);
                top.$('#FullName').focus();
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var postData = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson("/FrameworkModules/SequenceAdmin/SubmitForm", postData, function (d) {                
                        if (d.Success) {
                            msg.ok(d.Message);
                            addDailog.dialog('close');
                            mygrid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
                else {                   
                    top.$('#RealName').focus();
                }
                return false;
            }
        });
        return false;
    },
    EditSequence: function () { //修改序列
        var curSequence = mygrid.selected();
        if (curSequence) {
            var editDailog = top.$.hDialog({
                title: '修改序列', width: 295, height: 365, href: formUrl, iconCls: 'icon16_table_edit',
                onLoad: function () {
                    var parm = 'key=' + curSequence.ID;
                    $.ajaxjson("/FrameworkModules/SequenceAdmin/GetEntity", parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                    });
                    top.$('#FullName').focus();
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        var postData = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson("/FrameworkModules/SequenceAdmin/SubmitForm?key=" + curSequence.ID, postData, function (d) {
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
            msg.warning('请选择待修改的数据。');
        }
        return false;
    },
    DelSequence: function () {
        //功能代码逻辑...
        var row = mygrid.selected();
        if (row) {
            $.messager.confirm('询问提示', '确认要删除[' + row.FULLNAME + ']序列吗?', function (data) {
                if (data) {
                     var parm = 'key=' + row.ID;
                     $.ajaxjson("/FrameworkModules/SequenceAdmin/Delete", parm, function (d) {
                        if (d.Data > 0) {
                            msg.ok('序列删除成功。');
                            mygrid.reload();
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