var formUrl = '/Admin/FrameworkModules/RoleAdmin/Form/';

$(function () {
        autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.bindGrid, height: 5 });

        $('#a_refresh').click(function () { //刷新
            mygrid.reload();
        });
        
        $('#a_add').attr('onclick', 'RoleAdminMethod.AddRole();');
        $('#a_edit').attr('onclick', 'RoleAdminMethod.EditRole();');  //修改角色        
        $('#a_del').attr('onclick', 'RoleAdminMethod.DelRole();');  //删除角色
        $('#a_roleuser').attr('onclick', 'RoleAdminMethod.RoleUser();');//角色用户设置        
        $('#a_export').attr('onclick', "exportData();");
        $('#a_print').attr('onclick', 'RoleAdminMethod.Print();'); //打印
        BindCategory();
    });

    var exportData = function () {
        var exportData = new ExportExcel('list');
        exportData.go('PIROLE', 'SORTCODE');
    };

    var navgrid;
    var mygrid = {
        bindGrid: function (size) {
            navgrid = $('#list').datagrid({
                url: '/Admin/FrameworkModules/RoleAdmin/GridPageListJson/',
                toolbar: '#toolbar',
                width: size.width,
                height: size.height,
                idField: 'ID',
                sortName: 'SORTCODE',
                sortOrder: 'asc',
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
                { title: '编号', field: 'CODE', width: 120 },
                { title: '名称', field: 'REALNAME', width: 150 },
                { title: '分类', field: 'CATEGORY', width: 130, sortable: true },
                { title: '有效', field: 'ENABLED', width: 40, align: 'center', formatter: statusFormatter },
                { title: '允许编辑', field: 'ALLOWEDIT', width: 60, align: 'center', formatter: imgcheckbox },
                { title: '允许删除', field: 'ALLOWDELETE', width: 60, align: 'center', formatter: imgcheckbox },
                { title: '排序', field: 'SORTCODE', width: 80, sortable: true },
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

    function statusFormatter(value) {
        if (value == 1) {
            return "<div style='font-weight:700;color:yellow;background-color:green;margin:0px;padding:0px;'>有效</div>";
        } else {
            return "<div style='font-weight:700;color:red;background-color:#CCCCCC;text-decoration:line-through'>无效</div>";
        }
    }

    var imgcheckbox = function (cellvalue, options, rowObject) {
        return cellvalue ? '<img src="/Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
    };

    var BindCategory = function () {
        $('#role_Category').combobox({   
        url: '/Admin/FrameworkModules/RoleAdmin/GetRoleCategory/?categoryCode=RoleCategory',
        method: 'get',
        valueField: 'ITEMVALUE',
        textField: 'ITEMNAME',
        editable: false,
        panelHeight: 'auto',
        onChange: function () {
            var curCategory;
            curCategory = $("#role_Category").combobox('getValue');
            var ruleArr = [];
            if (curCategory !== '0') {
                ruleArr.push({ "field": "CATEGORY", "op": "eq", "data": escape(curCategory) });
                var filterObj = { groupOp: 'AND', rules: ruleArr };
                $('#list').datagrid('load', { filter: JSON.stringify(filterObj) });
            } else {
                mygrid.reload();
            }
        }
    });
};

var RoleAdminMethod = {
    AddRole: function () { //新增角色   
        var addDailog = top.$.hDialog({
            title: '添加角色', width: 430, height: 290, href: formUrl, iconCls: 'icon16_group_add',
            onLoad: function () {
                pageMethod.bindCategory('category', 'RoleCategory');
                top.$('#enabled').attr("checked", true);
                top.$('#code').focus();
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var postData = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson("/Admin/FrameworkModules/RoleAdmin/SubmitForm/?key=", postData, function (d) {
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
                    msg.warning('请输入角色名称');
                    top.$('#RealName').focus();
                }
                return false;
            }
        });
        return false;
    },
    EditRole: function () { //修改角色
        var curRole = mygrid.selected();
        if (curRole) {
            var editDailog = top.$.hDialog({
                title: '修改角色', width: 430, height: 290, href: formUrl, iconCls: 'icon16_group_edit',
                onLoad: function () {
                    pageMethod.bindCategory('category', 'RoleCategory');
                    var parm = 'key=' + curRole.ID;
                    $.ajaxjson("/Admin/FrameworkModules/RoleAdmin/GetEntity/", parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                    });
                    top.$('#code').focus();
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        var postData = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson("/Admin/FrameworkModules/RoleAdmin/SubmitForm/?key=" + curRole.ID, postData, function (d) {
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
    DelRole: function () {
        var row = mygrid.selected();
        if (row) {
            $.messager.confirm('询问提示', '确认要删除[' + row.REALNAME + ']角色吗?', function (data) {
                if (data) {
                    var parm = 'key=' + row.id;
                    $.ajaxjson("/Admin/FrameworkModules/RoleAdmin/Delete/", parm, function (d) {
                        if (d.Data > 0) {
                            msg.ok('角色删除成功。');
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
    },
    RoleUser: function () { //角色用户设置
        var currentRole = mygrid.selected();
        if (currentRole) {
            var rDialog = top.$.hDialog({
                href: '/Admin/FrameworkModules/PermissionSet/RoleUserSet/', width: 600, height: 500, title: '角色用户关联', iconCls: 'icon16_group_link',
                onLoad: function () {
                    top.$('#rlayout').layout();
                    top.$('#roleName').text(currentRole.REALNAME);
                    top.$('#allUsers,#selectedUser').datagrid({
                        width: 255,
                        height: 350,
                        iconCls: 'icon-users',
                        nowrap: false, //折行
                        rownumbers: true, //行号
                        striped: true, //隔行变色
                        idField: 'ID', //主键
                        singleSelect: true, //单选
                        columns: [[
                       { title: '登录名', field: 'USERNAME', width: 100 },
                       { title: '用户名', field: 'REALNAME', width: 120 }
                        ]],
                        pagination: false,
                        pageSize: 20,
                        pageList: [20, 40, 50]
                    });

                    top.$('#allUsers').datagrid({
                        url: '/Admin/FrameworkModules/UserAdmin/GetUserListJson/',
                        onDblClickRow: function (rowIndex, rowData) {
                            top.$('#aSelectUser').click();
                        }
                    });

                    top.$('#selectedUser').datagrid({
                        url: '/Admin/FrameworkModules/UserAdmin/GetDTByRole/?roleId=' + currentRole.ID,
                        onDblClickRow: function (rowIndex, rowData) {
                            top.$('#aDeleteUser').click();
                        }
                    });
                    top.$('#aSelectUser').click(function () {
                        var _row = top.$('#allUsers').datagrid('getSelected');
                        if (_row) {
                            var hasUserName = false;
                            var users = top.$('#selectedUser').datagrid('getRows');
                            $.each(users, function (i, n) {
                                if (n.USERNAME == _row.USERNAME) {
                                    hasUserName = true;
                                }
                            });
                            if (!hasUserName) {
                                top.$('#selectedUser').datagrid('appendRow', _row);
                                //添加用户                               
                                var query = 'roleId=' + currentRole.ID + '&addUserIds=' + _row.ID;
                                $.ajaxjson('/Admin/FrameworkModules/RoleAdmin/AddUserToRole/', query, function (d) {
                                    if (d.Data != '1') {
                                        msg.warning(d.Message);
                                    } else {
                                        msg.ok(d.Message);
                                    }
                                });
                            }
                            else {
                                msg.warning('用户已存在，请不要重复添加。');
                                return false;
                            }
                        } else {
                            msg.warning('请选择用户。');
                        }
                        return false;
                    });
                    top.$('#aDeleteUser').click(function () {
                        var trow = top.$('#selectedUser').datagrid('getSelected');
                        if (trow) {
                            var rIndex = top.$('#selectedUser').datagrid('getRowIndex', trow);
                            top.$('#selectedUser').datagrid('deleteRow', rIndex).datagrid('unselectAll');
                            //移除角色
                            var query = 'roleId=' + currentRole.ID + '&userId=' + trow.ID;
                            $.ajaxjson('/Admin/FrameworkModules/RoleAdmin/RemoveUserFromRole/', query, function (d) {
                                if (d.Data == 1) {
                                    msg.ok(d.Message);                                    
                                } else {
                                    msg.warning(d.Message);
                                }
                            });
                        } else {
                            msg.warning('请选择用户。');
                        }
                    });
                },
                submit: function () {
                    rDialog.dialog('close');
                }
            });
        } else {
            msg.warning('请选择一个角色哦！');
        }
        return false;
    },
    Print: function () {
        var colModel = $("#list").datagrid('options').columns[0]; //$("#staffGird").datagrid('getColumnFields');
        var dataModel = $("#list").datagrid("getRows");
        var footerData = $("#list").datagrid("getFooterRows");

        var htmlContent = "<table class='grid'><tr>";
        $.each(colModel, function (i) {
            var title = colModel[i].title;
            if (title) {
                var width = colModel[i].width;
                htmlContent += "<td style=\"width:" + (width - 5) + "px;\">" + title + "</td>";
            }
        });
        htmlContent += "</tr>";
        for (var i = 0; i < dataModel.length; i++) {
            htmlContent += "<tr>";
            $.each(colModel, function (j) {
                var title = colModel[j].title;
                if (title) {
                    var width = colModel[j].width;
                    htmlContent += "<td style=\"width:" + (width - 5) + "px;\">" + dataModel[i]["" + colModel[j].field + ""] + "</td>";
                }
            });
            htmlContent += "</tr>";
        }
        if (footerData) {
            htmlContent += "<tr>";
            $.each(colModel, function (j) {
                var title = colModel[j].title;
                if (title) {
                    var width = colModel[j].width;
                    htmlContent += "<td style=\"width:" + (width - 5) + "px;\">" + footerData["" + colModel[j].field + ""] + "</td>";
                }
            });
            htmlContent += "</tr>";
        }
        htmlContent += "</table>";
        $("#divPrint").html(htmlContent);
        $("#divPrint").show();
        $("#divPrint").jqprint();
        $("#divPrint").hide();
        return false;
    }
};