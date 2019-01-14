var formUrl = "/FrameworkModules/UserAdmin/Form";

$(function () {
    $('#sb').splitbutton({
        iconCls: 'icon16_report_user',
        menu: '#mm'
    });
	pageSizeControl.init({gridId:'userlist',gridType:'datagrid'});
	
    organizeTree.init();
    autoResize({ dataGrid: '#userlist', gridType: 'datagrid', callback: mygrid.bindGrid, height: 35, width: 230 });
    
    $('#a_add').attr('onclick', 'UserAdminMethod.AddUser();');
    $('#a_edit').attr('onclick', 'UserAdminMethod.EditUser();');
    $('#a_delete').attr('onclick', 'UserAdminMethod.DeleteUser();');
    $('#a_editpassword').attr('onclick', 'UserAdminMethod.SetUserPassword();');
    $('#a_refresh').attr('onclick', 'UserAdminMethod.Refreash();');
    $('#btnSearch').attr('onclick', 'UserAdminMethod.SearchData();');
    $('#a_export').attr('onclick', 'UserAdminMethod.ExportData();');
    $('#a_dimission').attr('onclick', 'UserAdminMethod.Dimission();');
    $('#btnLogByUser').attr('onclick', 'UserAdminMethod.LogByUser();');
    $('#btnLogByGeneral').attr('onclick', 'UserAdminMethod.LogByGeneral();');
    $(window).resize(function () {
		pageSizeControl.init({gridId:'userlist',gridType:'datagrid'});
    });
});

var organizeTree = {
    init: function () {
        $('#organizeTree').tree({
            lines: true,
            url: '/Admin/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/?isTree=1',
            animate: true,
            onLoadSuccess: function (node, data) {
                $('body').data('depData', data);
            },
            onClick: function (node) {
                var selectedId = node.id;
                $('#userlist').datagrid('load', { organizeId: selectedId });
            },
            onSelect: function (node) {
                $(this).tree('expand', node.target);
            }
        });
    },
    data: function (opr) {
        var d = JSON.stringify($('body').data('depData'));
        if (opr === '1') {
            d = '[{"id":0,"text":"请选择组织机构"},' + d.substr(1);
        }
        return JSON.parse(d);
    },
    getCurrentId: function () {
        return $('#organizeTree').tree('getSelected').id;
    }
};

var navgrid;
var mygrid = {
    bindGrid: function (size) {
        navgrid = $('#userlist').datagrid({
            url: "/Admin/FrameworkModules/UserAdmin/GetUserPageDTByDepartmentId/",
            //title: "系统用户列表",
            loadMsg: "正在加载用户数据，请稍等...",
            //iconCls: 'icon icon-list',
            width: size.width,
            height: size.height,
            rownumbers: true, //行号
            striped: true, //隔行变色
            idfield: 'ID', //主键
            singleSelect: true, //单选
            pagination: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            pageSize: 20,
            pageList: [20, 10, 30, 50],
            checkOnSelect: true,  
            rowStyler: function(index, row) {
                if (row.ENABLED <= 0) {
                    return 'color:#999;'; //显示为灰色字体
                }
            },
			onDblClickRow:function(rowIndex, rowData){
				document.getElementById('a_edit').click();
			},
            frozenColumns: [[
                { field: 'ck', checkbox: true, rowspan: 2 },
                { title: '编号', field: 'CODE', width: 150, rowspan: 2 },
                    { title: '登录名', field: 'USERNAME', width: 150, sortable: true, rowspan: 2 },
                    { title: '用户名', field: 'REALNAME', width: 150, rowspan: 2 }
                ]],
                columns: [[
                    { title: '有效', field: 'ENABLED', width: 35, rowspan: 2, formatter: function (v, d, i) {
                            if (d.USERNAME != 'Administrator') { //超级管理员不应该设置其是否有效
                                return '<img style="cursor:pointer" title="设置用户的可用性（启用或禁用）" onclick="javascript:SetUserEnabled(' + "'" + d.ID + "'" + ',' + v + ')" src="/Content/Styles/icon/bullet_' + (v ? "tick.png" : "minus.png") + '" />';
                            }
                        }
                    },
                    { title: '离职', field: 'ISDIMISSION', align: "center", width: 35,rowspan: 2, formatter: lizhicheckbox },
                    {
                        title: '性别', field: 'GENDER', width: 35, rowspan: 2, formatter: function (v, d, i) {
                            if (d.GENDER === '男'){
                                return '<img src="/Content/Styles/icon/user_b.png" alt="男" title="男" />';
                            }
                            else if (d.GENDER === '女') {
                                return '<img src="/Content/Styles/icon/user_green.png" alt="女" title="女" />';
                            } else {
                                return '<img src="/Content/Styles/icon/question_button.png" alt="性别未知" title="未设置性别" />';
                            }
                        }
                    },
                    { title: '联系方式', colspan: 2 },
                    { title: '组织机构信息', colspan: 5 },
                    { title: '登录信息', colspan: 3 },
                    { title: '描述', field: 'DESCRIPTION', width: 300, rowspan: 2}],
                    [{ title: '邮箱地址', field: 'EMAIL', width: 150, rowspan: 1 },
                    { title: '手机号码', field: 'MOBILE', width: 100, rowspan: 1 },
                    { title: '所在单位/公司', field: 'COMPANYNAME', width: 100, rowspan: 1 },
                    { title: '所在子公司', field: 'SUBCOMPANYNAME', width: 100, rowspan: 1 },
                    { title: '所在部门', field: 'DEPARTMENTNAME', width: 100, rowspan: 1 },
                    { title: '所在子部门', field: 'SUBDEPARTMENTNAME', width: 100, rowspan: 1 },
                    { title: '所在工作组', field: 'WORKGROUPNAME', width: 100, rowspan: 1 },
                    { title: '上次登录时间', field: 'PREVIOUSVISIT', width: 150, sortable: true, rowspan: 1 },
                    { title: '登录次数', field: 'LOGONCOUNT', width: 60, sortable: true, rowspan: 1 },
                    { title: 'IP地址', field: 'IPADDRESS', width: 80, sortable: true, rowspan: 1 }
                ]],
                onLoadSuccess: function (data) {
                    var panel = $(this).datagrid('getPanel');
                    var tr = panel.find('div.datagrid-body tr');
                    refreshCellsStyle(tr);
                    var trHead = panel.find('div.datagrid-header tr');
                    trHead.each(function () {
                        var tds = $(this).children('td');
                        tds.each(function () {
                            $(this).find('span,div').css({ "font-size": "14px" });
                        });
                    });
                }
        });
    },
    reload:function(){
        navgrid.datagrid('reload');
    },
    getSelectedRow: function () {
        return navgrid.datagrid('getSelected'); 
    }
};

function refreshCellsStyle(tr) {
    tr.each(function () {
        var tds = $(this).children('td');
        tds.each(function () {
            if ($(this).attr("field") == "USERNAME") {
                var text = $(this).text();
                var cssObj = { "text-align": "left" };
                if (text == "Administrator") {
                    cssObj["color"] = "green";
                    cssObj["font-weight"] = "700";
                    cssObj["font-size"] = "16px";
                }
                $(this).children("div").css(cssObj);
            }
        });
    });
}

var imgcheckbox = function (cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="/Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};

var lizhicheckbox = function (cellvalue, options, rowObject) {
    return cellvalue ? '<img src="/Content/Styles/icon/checkbox_yes.png" alt="离职" title="离职" />' : '<img src="/Content/Styles/icon/checkbox_no.png" alt="未离职" title="未离职" />';
};

var date2str = function (cellvalue, options, rowObject) {
    if (cellvalue)
        return $D(cellvalue).strftime("%Y-%m-%d");
    else
        return '';
};
var UserAdminMethod = {
    Refreash: function () {
        $('#userlist').datagrid('reload');
    },
    SearchData: function () {
        var curSearchValue = $('#txtSearchValue').val();
        var curOrganizeId = organizeTree.getCurrentId();
        if (curSearchValue) {
            $('#userlist').datagrid('load', { searchValue: curSearchValue, organizeId: curOrganizeId });
        } else {
            $('#userlist').datagrid('load', { organizeId: curOrganizeId });
        }
    },
    ExportData: function () {
        var fieldList = '[{"title":"编号","field":"CODE"},' +
                        '{"title":"登录名","field":"USERNAME"},' +
                        '{"title":"用户名","field":"REALNAME"},' +
                        '{"title":"性别","field":"GENDER"},' +
                        '{"title":"公司名称","field":"COMPANYNAME"},' +
                        '{"title":"部门名称","field":"DEPARTMENTNAME"},' +
                        '{"title":"邮箱","field":"EMAIL"},' +
                        '{"title":"出生日期","field":"BIRTHDAY"},' +
                        '{"title":"手机","field":"MOBILE"},' +
                        '{"title":"QQ","field":"QICQ"},' +
                        '{"title":"有效","field":"ENABLED"},' +
                        '{"title":"描述","field":"DESCRIPTION"}]';
        var exportData = new ExportExcel('userlist', fieldList);
        exportData.go('PIUSER', 'SORTCODE');
    },
    initData: function () {
        //绑定各数据字典
        pageMethod.bindCategory('Gender', 'Gender');
        pageMethod.bindCategory('RoleId', 'undefined');
        pageMethod.bindCategory('CompanyId', 'Company');
        pageMethod.bindCategory('SubCompanyId', 'SubCompany');
        pageMethod.bindCategory('DepartmentId', 'Department');
        pageMethod.bindCategory('SubDepartmentId', 'SubDepartment');
        pageMethod.bindCategory('WorkgroupId', 'Workgroup');
    },
    AddUser: function () { //添加用户
        var addDialog = top.$.hDialog({
            href: formUrl,
            title: '添加用户',
            width: 610,
            height: 640,
            iconCls: 'icon16_user_add',
            onLoad: function () {
                UserAdminMethod.initData();
                top.$('#Enabled').attr("checked", true);
                top.$('#Description').val("");
                top.$('#UserName').focus();
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {                    
                    var postData = pageMethod.serializeJson(top.$('#uiform'));
                    postData.CompanyName = top.$('#CompanyId').combobox('getText');
                    postData.SubCompanyName = top.$('#SubCompanyId').combobox('getText');
                    postData.DepartmentName = top.$('#DepartmentId').combobox('getText');
                    postData.SubDepartmentName = top.$('#SubDepartmentId').combobox('getText');
                    postData.WorkgroupName = top.$('#WorkgroupId').combobox('getText');
                    $.ajaxjson("/FrameworkModules/UserAdmin/SubmitForm", postData, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            addDialog.dialog('close');
                            mygrid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                } else {
                    msg.warning('请输入用户名称。');
                    top.$('#UserName').focus();
                }
            }
        });
        return false;
    },
    EditUser: function () { //修改用户
        var selectRow = mygrid.getSelectedRow();
        if (selectRow != null) {
            if (selectRow.USERNAME != '' && selectRow.USERNAME == 'Administrator' && curUserinfo.username != 'Administrator') {
                $.messager.alert('警告提示', '你不能修改超级管理员用户！', 'warning');
                return false;
            }

            //弹窗
            var editDailog = top.$.hDialog({
                href: formUrl,
                width: 610,
                height: 640,
                title: '修改用户',
                iconCls: 'icon16_user_edit',
                onLoad: function () {
                    UserAdminMethod.initData();
                    var parm = 'key=' + selectRow.ID;
                    $.ajaxjson('/FrameworkModules/UserAdmin/GetEntity', parm, function (data) {
                        if (data) {
                            //初始化相关数据
                            SetWebControls(data, true);
                            top.$('#UserPassword').after('******').remove();
                        }
                    });
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {                      
                        var postData = pageMethod.serializeJson(top.$('#uiform'));   
                        postData.CompanyName = top.$('#CompanyId').combobox('getText');
                        postData.SubCompanyName = top.$('#SubCompanyId').combobox('getText');
                        postData.DepartmentName = top.$('#DepartmentId').combobox('getText');
                        postData.SubDepartmentName = top.$('#SubDepartmentId').combobox('getText');
                        postData.WorkgroupName = top.$('#WorkgroupId').combobox('getText');
                        $.ajaxjson("/FrameworkModules/UserAdmin/SubmitForm?key=" + selectRow.ID, postData, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                editDailog.dialog('close');
                                mygrid.reload();
                            }
                            else {
                                MessageOrRedirect(d);
                            }
                        });
                    }
                }
            });
        } else {
            msg.warning('请选择待修改的用户。');
            return false;
        }
        return false;
    },
    DeleteUser: function () { //删除用户
        var selectRow = mygrid.getSelectedRow();
        if (selectRow) {
            if (selectRow.USERNAME != '' && selectRow.USERNAME == 'Administrator') {
                msg.warning('不能删除超级管理员！');
                return false;
            }

            if (selectRow.ID != '' && selectRow.ID == curUserinfo.id) {
                msg.warning('不能删除当前登录用户！');
                return false;
            }

            $.messager.confirm('询问提示', '确认要删除用户【' + selectRow.REALNAME + '】吗？', function (data) {
                if (data) {
                    var parm = 'key=' + selectRow.ID;
                    $.ajaxjson("/FrameworkModules/UserAdmin/Delete", parm, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            mygrid.reload();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            });
        }
        else {
            msg.warning('请选择要删除的用户。');
            return false;
        }
        return false;
    },
    SetUserPassword: function () { //设置用户密码  
        var selectRow = mygrid.getSelectedRow();
        if (selectRow != null) {
            var tempDialog = top.$.hDialog({
                content: formeditpass,
                width: 300,
                height: 160,
                title: '设置用户密码',
                iconCls: 'icon16_user_level_filtering',
                submit: function () {
                    if (top.$('#txtNewPassword').validatebox('isValid')) {
                        var parm = 'userId=' + selectRow.ID + '&password=' + top.$('#txtNewPassword').val();
                        $.ajaxjson("/FrameworkModules/UserAdmin/SetUserPassword", parm, function (d) {
                            if (d.Data > 0) {
                                msg.ok('密码修改成功，请牢记新密码！');
                                mygrid.reload();
                                tempDialog.dialog('close');
                            } else {
                                MessageOrRedirect(d);
                            }
                        });
                    } else {
                        msg.warning('新密码不能为空～！');
                        top.$('#NewPassword').focus();
                    }
                }
            });
            top.$('#loginname').text(selectRow.USERNAME + ' | ' + selectRow.REALNAME);
            top.$('#txtNewPassword').validatebox();
            top.$('#txtNewPassword').focus();
        } else {
            msg.warning('请选择要修改密码的用户。');
            return false;
        }
        return false;
    },
    LogByUser: function () {
        
        var selectRow = mygrid.getSelectedRow();
        if (selectRow) {
            var index = top.layer.msg('加载中', { icon: 16 });
            AddToTab('用户访问详情', '/FrameworkModules/LogAdmin/LogByUser', 'icon16_diagnostic_chart', 'pageLogByUser');
            window.setTimeout(function () {
                var test = parent.$("#pageLogByUser")[0].contentWindow;
                test.$('#txtOpuser').val(selectRow.REALNAME);
                test.Search();
            }, 2000);
            layer.close(index);
        } else {
            msg.warning('请选择一个用户！');
        }
        //AddToTab('用户访问详情', '/FrameworkModules/LogAdmin/LogByUser', 'icon16_diagnostic_chart', 'pageLogByUser');
    },
    LogByGeneral: function () {
        AddToTab('用户访问情况', '/FrameworkModules/LogAdmin/LogByGeneral', 'icon16_address_block', 'pageLogByGeneral');
    },
    Dimission: function () {
        var selectRow = mygrid.getSelectedRow();
        if (selectRow) {
            if (selectRow.USERNAME && (selectRow.USERNAME == 'Administrator' || selectRow.USERNAME == 'Admin')) {
                msg.warning('请选择非管理员！');
                return false;
            }
            var index = top.layer.msg('加载中', { icon: 16 });
            AddToTab('用户离职', '/FrameworkModules/UserAdmin/UserDimission', 'icon16_aol_messenger', 'pageUserDimission');
            window.setTimeout(function () {
                var test = parent.$("#pageUserDimission")[0].contentWindow;
                test.BindPage(selectRow.ID);
                test.$('#Id').val(selectRow.ID);
            }, 1000);
            layer.close(index);
        } else {
            msg.warning('请选择一个用户！');
        }
    }
};

function SetUserEnabled(id, val) {
    var parm = 'userId=' + id  + '&isEnabled=' + val;
    $.ajaxjson("/FrameworkModules/UserAdmin/SetUserEnabled", parm, function (d) {
        if(d.Success){
            mygrid.reload();
        }else{
            MessageOrRedirect(d);
        }
    });
}

var formeditpass = '<table class="grid" id="epform">';
formeditpass += '<tr><td>登录名：</td><td><span id="loginname"></span></td></tr>';
formeditpass += '<tr><td>新密码：</td><td><input  validType="safepass"  required="true" id="txtNewPassword" name="password" type="password" class="txt03" /></td></tr>';
formeditpass += '</table>';
