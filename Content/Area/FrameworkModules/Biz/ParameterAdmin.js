/*
RDIFramework.NET，基于.NET的快速信息化系统开发、整合框架，给用户和开发者最佳的.Net框架部署方案。
框架官网：http://www.rdiframework.net/
框架博客：http://blog.rdiframework.net/
交流QQ：406590790 
邮件交流：406590790@qq.com

其他博客：
http://www.cnblogs.com/huyong 
http://blog.csdn.net/chinahuyong
*************************************************************************************
* RDIFramework.NET框架“系统参数管理”业务界面逻辑
*
* 主要完成系统参数的增加、修改、删除、导出等。
* 修改记录：
*   1、 2015-08-05 EricHu V3.0 新增本业务逻辑的编写。
*/

var controlUrl = '/FrameworkModules/ParameterAdmin/',
    formUrl = '/FrameworkModules/ParameterAdmin/Form?n=' + Math.random();

$(function () {
    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.bindGrid, height: 5 });

    $('#a_refresh').click(function () { //刷新
        mygrid.reload();
    });
    $('#a_add').attr('onclick', 'ParameterAdmin.AddParameter();');
    $('#a_edit').attr('onclick', 'ParameterAdmin.EditParameter();');  //修改系统参数
    $('#a_del').attr('onclick', 'ParameterAdmin.DelParameter();');  //删除系统参数
    $('#a_export').attr('onclick', "exportData();");
});

var exportData = function () {
    var exportData = new ExportExcel('list');
    exportData.go('CIParameter', 'CREATEON');
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
                { title: '分类键值', field: 'CATEGORYKEY', width: 100, sortable: true },
                { title: '参数主键', field: 'PARAMETERID', width: 300 },
                { title: '参数编号', field: 'PARAMETERCODE', width: 120 },
                { title: '参数内容', field: 'PARAMETERCONTENT', width: 150 },
                { title: '有效', field: 'ENABLED', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    } 
                },
                { title: '允许编辑', field: 'ALLOWEDIT', width: 50, align: 'center', formatter: function (v, d, i) {
                    return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    } 
                },
                { title: '允许删除', field: 'ALLOWDELETE', width: 50, align: 'center', formatter: function (v, d, i) {
                    return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    } 
                },
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

var ParameterAdmin = {
    AddParameter: function () { //新增系统参数
        var addDailog = top.$.hDialog({
            title: '添加系统参数', width: 295, height: 338, href: formUrl, iconCls: 'icon16_cog_add',
            onLoad: function () {
                top.$('#Enabled,#AllowEdit,#AllowDelete').attr('checked', true);
                top.$('#CategoryKey').focus();
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var postData = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson("/FrameworkModules/ParameterAdmin/SubmitForm", postData, function (d) {     
                        if (d.Success) {
                            msg.ok(d.Message);
                            addDailog.dialog('close');
                            mygrid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
                return false;
            }
        });
        return false;
    },
    EditParameter: function () { //修改系统参数
        var curParameter = mygrid.selected();
        if (curParameter) {
            if (!curParameter.ALLOWEDIT) {
                layer.msg('当前所选数据不允许编辑...');
                return false;
            }
            var editDailog = top.$.hDialog({
                title: '修改系统参数', width: 295, height: 338, href: formUrl, iconCls: 'icon16_cog_edit',
                onLoad: function () {
                    var parm = 'key=' + curParameter.ID;
                    $.ajaxjson("/FrameworkModules/ParameterAdmin/GetEntity", parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                    });

                    top.$('#CategoryKey').focus();
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        var postData = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson("/FrameworkModules/ParameterAdmin/SubmitForm?key=" + curParameter.ID, postData, function (d) {
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
            layer.msg('请选择待修改的数据...');
        }
        return false;
    },
    DelParameter: function () {
        //功能代码逻辑...
        var row = mygrid.selected();
        if (row) {
            if (!row.ALLOWDELETE) {
                layer.msg('当前所选数据不允许删除...');
                return false;
            }

            $.messager.confirm('询问提示', '确认要删除所选系统参数吗?', function (data) {
                if (data) {
                     var parm = 'key=' + row.ID;
                     $.ajaxjson("/FrameworkModules/ParameterAdmin/Delete", parm, function (d) {
                        if (d.Data > 0) {
                            msg.ok('系统参数删除成功。');
                            mygrid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            });
        } else {
            layer.msg('请选择待删除的数据...');
        }
        return false;
    }
};