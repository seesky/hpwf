var formUrl = "/FrameworkModules/StaffAdmin/Form";

$(function () {
	pageSizeControl.init({gridId:'staffGird',gridType:'datagrid'});
	organizeTree.init();
    autoResize({ dataGrid: '#staffGird', gridType: 'datagrid', callback: mygrid.databind, height: 36, width: 230 });
    
    $('#btnAddStaff').attr('onclick', 'StaffAdminMethod.AddStaff();'); //新增员工（职员）
    $('#btnEditStaff').attr('onclick', 'StaffAdminMethod.EditStaff();');//修改员工（职员）
    $('#btnDeleteStaff').attr('onclick', 'StaffAdminMethod.DeleteStaff();'); //删除员工（职员）
    $('#btnMoveTo').attr('onclick', 'StaffAdminMethod.MoveTo();');//移动员工（职员）
    $('#btnExport').attr('onclick', 'StaffAdminMethod.Export();');//导出员工（职员）
    $('#btnRefresh').attr('onclick', 'StaffAdminMethod.Refreash();');//刷新
	
    $(window).resize(function () { 
		pageSizeControl.init({gridId:'staffGird',gridType:'datagrid'});
    });
});

var mylayout = {
    init: function (size) {
        $('#layout').width(size.width - 4).height(size.height - 4).layout();
        var center = $('#layout').layout('panel', 'center');
        center.panel({
            onResize: function (w, h) {
                $('#staffGird').datagrid('resize', { width: w-6, height: h-36 });
            }
        });
    },
    resize: function (size) {
        mylayout.init(size);
        $('#layout').layout('resize');
    }
};

var organizeTree = {
    init: function() {
        $('#organizeTree').tree({
            lines: true,
            url: '/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson?isTree=1',
            animate: true,
            onLoadSuccess:function(node,data) {
                $('body').data('depData', data);
            },onClick: function(node) {
                var selectedId = node.id;    
                $('#staffGird').datagrid('load', { organizeId: selectedId });
            },
            onSelect: function (node) {
                $(this).tree('expand', node.target);
            }
        });
    },
    data: function(opr){
        var d = JSON.stringify($('body').data('depData'));
        if (opr === '1') {
            d = '[{"id":0,"text":"请选择组织机构"},' + d.substr(1);
        }
        return JSON.parse(d);
    }    
};

var mygrid = {
    databind: function (size) {
        $('#staffGird').datagrid({
            url: "/FrameworkModules/StaffAdmin/GetStaffByOrganizeId",
            title: "员工（职员）列表",
            loadMsg: "正在加载员工（职员）数据，请稍等...",
            width: size.width,
            height: size.height,
            idfield: 'ID',
            singleSelect: true,
            striped: true,
            rownumbers: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            rowStyler: function (index, row) {
                if (row.ENABLED <= 0 && row.USERID == "") {
                    return 'color:#999;'; 
                }
                if (row.ENABLED <= 0 && row.USERID != "") {
                    return 'color:#969;'; 
                }
                if (row.USERID != "") {
                    return 'color:#869;';
                }
            },
			onDblClickRow:function(rowIndex, rowData){
				document.getElementById('btnEditStaff').click();
			},
            columns: [[
                    { field: 'ck', checkbox: true, rowspan: 2 },
                    { title: '主键', field: 'ID', hidden: true, rowspan: 2 },
                    { title: '编号', field: 'CODE', width: 100, rowspan: 2 },
                    { title: '姓名', field: 'REALNAME', width: 100, rowspan: 2 },
                    {
                        title: '性别', field: 'GENDER', width: 50, rowspan: 2, formatter: function (v, d, i) {
                            if (d.GENDER === '男') {
                                return '<img src="../../Content/Styles/icon/user_b.png" alt="男" title="男" />';
                            }
                            else if (d.GENDER === '女') {
                                return '<img src="../../Content/Styles/icon/user_green.png" alt="女" title="女" />';
                            } else {
                                return '<img src="../../Content/Styles/icon/question_button.png" alt="性别未知" title="未设置性别" />';
                            }
                        }
                    },
					{ title: '联系方式', colspan: 4 },
					{ title: '有效', field: 'ENABLED', width: 50, align: 'center', formatter: statusFormatter, rowspan: 2 },
                    { title: '描述', field: 'DESCRIPTION', width: 260, rowspan: 2 },
                    { title: 'UserId', field: 'USERID', hidden: true, rowspan: 2 }
					], [
                    { title: '出生日期', field: 'BIRTHDAY', align: "center", width: 90, rowspan: 1 },
                    { title: '手机号码', field: 'MOBILE', width: 120, rowspan: 1 },
                    { title: '办公电话', field: 'OFFICEPHONE', width: 120, rowspan: 1 },
                    { title: '邮箱地址', field: 'EMAIL', width: 150, rowspan: 1 }

                ]],
            onLoadSuccess: function (data) {
                if (data.rows.length > 0) {
                    $('#staffGird').datagrid("selectRow", 0);
                }
            }
        });
    },
    reload: function () {
        $('#staffGird').datagrid('clearSelections').datagrid('reload');
    },
    selectRow: function () {
        return $('#staffGird').datagrid('getSelected');
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
    return cellvalue ? '<img src="../../Content/Styles/icon/bullet_tick.png" alt="正常" title="正常" />' : '<img src="../../Content/Styles/icon/bullet_minus.png" alt="禁用" title="禁用" />';
};

var StaffAdminMethod = {
    Refreash:function() {
        mygrid.reload();
    },
    initData: function (organizeId) {
        top.$('#Education,#Degree,#Title,#TitleLevel,#WorkingProperty,#Party,#Gender').combobox({ panelHeight: 'auto' });
        top.$('#Birthday,#TitleDate,#WorkingDate,#DimissionDate,#JoinInDate').datebox({
            formatter: function (date) {
                return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate();
            },
            arser: function (date) {
                return new Date(Date.parse(date.replace(/-/g, "/")));
            }
        });

        var _organizeId = organizeId || 0;
        top.$('#OrganizeId').combotree({
            data: organizeTree.data('1'),
            valuefield: 'ID',
            textField: 'text',
            value: _organizeId
        });
        //绑定各数据字典
        pageMethod.bindCategory('Gender', 'Gender');
        pageMethod.bindCategory('Education', 'Education');
        pageMethod.bindCategory('WorkingProperty', 'WorkingProperty');
        pageMethod.bindCategory('Degree', 'Degree');
        pageMethod.bindCategory('Gender', 'Gender');
        pageMethod.bindCategory('Title', 'Title');
        pageMethod.bindCategory('TitleLevel', 'TitleLevel');
        pageMethod.bindCategory('Nationality', 'Nationality');
        pageMethod.bindCategory('Party', 'PoliticalStatus');
        top.$('#staffTab').tabs({
            onSelect: function () {
                top.$('.validatebox-tip').remove();
            }
        });
        top.$('#passSalt').val(randomString());

    },
    AddStaff: function () { //增加员工（职员）
        var addDialog = top.$.hDialog({
            href: formUrl + '?v=' + Math.random(),
            width: 680,
            height: 410,
            title: '新增员工（职员）',
            iconCls: 'icon16_vcard_add',
            onLoad: function () {
                var dep = $('#organizeTree').tree('getSelected');
                var depID = 0;
                if (dep) {
                    depID = dep.id || 0;
                };
                top.$('#Enabled').attr("checked", true);
                //如果左侧有选中组织机构，则添加的时候，部门默认选中
                StaffAdminMethod.initData(depID);
            },
            closed: false,
            submit: function () {
                var tab = top.$('#staffTab').tabs('getSelected');
                var index = top.$('#staffTab').tabs('getTabIndex', tab);
                if (top.$('#uiform').form('validate')) {
                    var vOrganizeId = top.$('#OrganizeId').combobox('getValue');                   
                    var postData = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson("/FrameworkModules/StaffAdmin/SubmitForm?organizeId=" + vOrganizeId, postData, function (d) {                    
                        if (d.Success) {
                            msg.ok('添加成功');
                            mygrid.reload();
                            addDialog.dialog('close');
                        } else {
                            if (d.Data == -2) {
                                msg.error('用户名已存在，请更改用户名。');
                                if (index > 0) {
                                    top.$('#staffTab').tabs('select', 0);
                                }
                                top.$('#username').select();
                            } else {
                                MessageOrRedirect(d);
                            }
                        }
                    });
                } else {
                    if (index > 0)
                        top.$('#staffTab').tabs('select', 0);
                }
            }
        });
        return false;
    },
    EditStaff: function () { //编辑员工（职员）
        var row = mygrid.selectRow();
        if (row) {
            var editDailog = top.$.hDialog({
                href: formUrl + '?v=' + Math.random(),
                title: '修改员工（职工）',
                iconCls: 'icon16_vcard_edit',
                width: 680,
                height: 410,
                onLoad: function () {
                    var dep = $('#organizeTree').tree('getSelected');
                    var depID = 0;
                    if (dep) {
                        depID = dep.id || 0;
                    }

                    StaffAdminMethod.initData(depID);
                    var parm = 'key=' + row.ID;
                    $.ajaxjson('/FrameworkModules/StaffAdmin/GetEntity', parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);                           
                        }
                    });
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        var vOrganizeId = top.$('#OrganizeId').combobox('getValue');
                        var postData = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson("/FrameworkModules/StaffAdmin/SubmitForm?organizeId=" + vOrganizeId + "&key=" + row.ID, postData, function (d) {
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
            msg.warning('请选择待修改的员工（职工）!');
            return false;
        }
        return false;
    },
    DeleteStaff: function () { //删除员工（职员）
        var row = mygrid.selectRow();
        if (row != null) {            
            $.messager.confirm('询问提示', '确定要删除选中的员工（职员）吗？', function (data) {
                if (data) {
                    var parm = 'key=' + row.ID;
                    $.ajaxjson("/FrameworkModules/StaffAdmin/Delete", parm, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            mygrid.reload();
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
            msg.warning('请选择要删除的员工（职员）!');
            return false;
        }
        return false;
    },
    MoveTo: function () { //移动员工（职员）
        var row = mygrid.selectRow();
        if (row != null) {
            var ad = top.$.hDialog({
                max: false,
                width: 300,
                height: 500,
                title: '移动员工（职员） ━ ' + row.REALNAME,
                iconCls: 'icon16_arrow_switch',
                content: '<ul id="orgTree"></ul>',
                submit: function () {
                    var node = top.$('#orgTree').tree('getSelected');
                    if (node) {
                        $.ajaxjson("/FrameworkModules/StaffAdmin/MoveTo", 'staffId=' + row.ID + '&organizeId=' + node.id, function (d) {
                            if (d.Success) {
                                msg.ok('移动成功！');
                                mygrid.reload();
                                ad.dialog('close');
                            } else if (d.Data == 0) {
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
            top.$('#orgTree').tree({
                data: organizeTree.data('0'),
                valuefield: 'ID',
                textField: 'text',
                animate: true,
                lines: true,
                onLoadSuccess: function (node, data) {
                    top.$.hLoading.hide(); //加载完毕后隐藏loading
                },
                onClick: function (node) {
                    var selectedId = node.id;
                }
            });
            
        } else {
            msg.warning('请选择要移动的员工（职员）!');
            return false;
        }
        return false;
    },
    Export: function () { //导出员工（职员）
        var exportData = new ExportExcel('staffGird');
        exportData.go('PISTAFF', 'SORTCODE');
        return false;
    }
};