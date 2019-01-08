var queryEngineDefineGrid,
    controlQueryEngineUrl = '/FrameworkModules/QueryEngineDefineAdmin/',
    formUrl = "/FrameworkModules/QueryEngineDefineAdmin/";

$(function () {
    pageSizeControl.init({ gridId: 'queryEngineDefineGrid', gridType: 'datagrid' });
    queryEngineTree.init();
    //autoResize({ dataGrid: '#queryEngineDefineGrid', gridType: 'datagrid', callback: grid.databind, height: 35, width: 230 });    
    autoResize({ dataGrid: '#queryEngineDefineGrid', gridType: 'datagrid', callback: grid.databind, height: 35, width: 0 });    
    $('#a_add').attr('onclick', 'crud.add();');
    $('#a_edit').attr('onclick', 'crud.edit();');
    $('#a_delete').attr('onclick', 'crud.del();');
    $('#a_refresh').attr('onclick', 'crud.refreash();');
    $('#a_prviewData').attr('onclick', 'crud.prviewData();');    
    $(window).resize(function () {
        pageSizeControl.init({ gridId: 'queryEngineDefineGrid', gridType: 'datagrid' });
    });
});

var queryEngineTree = {
    init: function () {
        $('#queryEngineTree').tree({
            lines: true,
            url: '/FrameworkModules/QueryEngineAdmin/GetQueryEngineTreeJson?isTree=1',
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
                $('#queryEngineDefineGrid').datagrid({
                    url: controlQueryEngineUrl + 'GetEngineDefinePageDTByEngineIds',
                    queryParams: { queryEngineId: node.id }
                });

                //清空上次的选择
                $('#detailGrid').datagrid('loadData', { total: 0, rows: []});  
                $('#queryEngineDefineGrid').datagrid('clearSelections');
            }
        });
    },
    selected: function () {
        return $('#queryEngineTree').tree('getSelected');
    },    
    reLoad: function () {
        return $('#queryEngineTree').tree('reload');
    }
};

var grid = {
    databind: function (winsize) {
        queryEngineDefineGrid = $('#queryEngineDefineGrid').datagrid({
            toolbar: '#toolbar',
            width: winsize.width,
            height: winsize.height,
            striped: true,
            fit: true,
            singleSelect: true,
            selectOnCheck: true,
            checkOnSelect: true,
            loadMsg: '正在努力加载中....',            
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            idField: 'ID',
            sortName: 'SORTCODE',
            sortOrder: 'asc',
            pagination: true,
            rownumbers: true,
            pageSize: 20,
            pageList: [20, 10, 30, 50],
            onDblClickRow: function (rowIndex, rowData) {
                //document.getElementById('a_edit').click(); //弹出修改     
                $('#detailGrid').datagrid('loadData', { total: 0, rows: []});
                crud.prviewData();
            },
            onLoadSuccess: function (data) {
                if (data.total == 0) {
                    //添加一个新数据行，第一列的值为你需要的提示信息，然后将其他列合并到第一列来，注意修改colspan参数为你columns配置的总列数
                    $(this).datagrid('appendRow', { CODE: '<div style="text-align:center;color:red">没有相关记录！</div>' }).datagrid('mergeCells', { index: 0, field: 'CODE', colspan: 10 }); //隐藏分页导航条，这个需要熟悉datagrid的html结构，直接用jquery操作DOM对象，easyui datagrid没有提供相关方法隐藏导航条
                    $(this).closest('div.datagrid-wrap').find('div.datagrid-pager').hide();
                }
                //如果通过调用reload方法重新加载数据有数据时显示出分页导航容器
                else $(this).closest('div.datagrid-wrap').find('div.datagrid-pager').show();
            },
            columns: [[
                { title: '编码', field: 'CODE', width: 130 },
                { title: '名称', field: 'FULLNAME', width: 200 },
                { title: 'Id', field: 'ID', hidden: true },
                { title: 'QueryEngineId', field: 'QUERYENGINEID', hidden: true },
                { title: '连接名称', field: 'LINKNAME_CHS', width: 150 },
                { title: '数据源类型', field: 'DATASOURCETYPE', width: 80, align: 'center', formatter: function (v, d, i) {
                    if (v == '1') { return '<span style="color:#0066CC;">表或视图</span>'; }
                    else if (v == '2') { return '<span style="color:#CC3366;">存储过程</span>'; }
                    else { return '<span style="color:#666666;">未知</span>'; }
                }
                },
                { title: '数据源名称', field: 'DATASOURCENAME', width: 120 },
                {
                    title: '有效', field: 'ENABLED', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    }
                },
                {
                    title: '可编辑', field: 'ALLOWEDIT', width: 50, align: 'center', formatter: function (v, d, i) {
                        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
                    }
                },
				{
				    title: '可删除', field: 'ALLOWDELETE', width: 50, align: 'center', formatter: function (v, d, i) {
				        return '<img src="/Content/images/' + (v ? "checkmark.gif" : "checknomark.gif") + '" />';
				    }
				},
                { title: '排序', field: 'SORTCODE', width: 60, align: 'right' },
                { title: '备注', field: 'DESCRIPTION', width: 500 }
            ]]
        });
    },
    reload: function (treeNode) {
        if (treeNode) {
            queryEngineDefineGrid.datagrid({
                url: controlQueryEngineUrl + "GetEngineDefinePageDTByEngineIds",
                queryParams: { queryEngineId: treeNode.id }
            });
        }
    },
    selected: function () {
        return queryEngineDefineGrid.datagrid('getSelected');
    }
};

var crud = {
    refreash: function () {
        grid.reload(queryEngineTree.selected());
    },
    bindCtrl: function (navId) {
        var treeData = '';
        $.ajaxtext('/FrameworkModules/QueryEngineAdmin/GetQueryEngineTreeJson', '', function (data) {
            if (data) {
                treeData = data.replace(/Id/g, 'id').replace(/FullName/g, 'text');
                if (treeData === '[]' || !treeData) {
                    treeData = '[{"id":0,"selected":true,"text":"请选择父级"}]';
                } else {
                    treeData = '[' + treeData.substr(1, treeData.length - 1);
                }

                top.$('#QueryEngineId').combotree({
                    data: JSON.parse(treeData),
                    valueField: 'id',
                    textField: 'text',
                    panelWidth: '520',
                    editable: false,
                    lines: true,
                    onSelect: function (item) {
                        var nodeId = top.$('#QueryEngineId').combotree('getValue');
                        if (item.id == navId) {
                            top.$('#QueryEngineId').combotree('setValue', nodeId);
                            msg.warning('上级不能与当前相同!');
                        }
                    }
                }).combotree('setValue', 0);
            }
        });
        top.$('#DataBaseLinkName').combobox({
            url: controlQueryEngineUrl + 'GetDataBaseLink',
            method: 'get',
            valueField: 'Id',
            textField: 'LinkName',
            editable: false,
            panelHeight: 'auto'
        });
        top.$('#Code').focus();
        top.$('#Enabled,#AllowEdit,#AllowDelete').attr("checked", true);
    },
    add: function () {
        var treeSelected = queryEngineTree.selected(),
            row = grid.selected();
        if (!row) {
            row = treeSelected;
        }
        var addDialog = top.$.hDialog({
            href: formUrl + 'QueryEngineDefineForm?n=' + Math.random(), title: '添加查询引擎', iconCls: 'icon16_table_add', width: 660, height: 600,
            onLoad: function () {
                crud.bindCtrl();
                if (treeSelected) {
                    setTimeout(function () { top.$('#QueryEngineId').combotree('setValue', treeSelected.id); }, 300);
                }
            },
            submit: function () {
                if (top.$('#uiform').validate().form()) {
                    var queryString = pageMethod.serializeJson(top.$('#uiform'));
                    $.ajaxjson(controlQueryEngineUrl + 'SubmitForm', queryString, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
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
        var rowEdit = grid.selected();
        if (rowEdit) {
            if (rowEdit.ALLOWEDIT == '0') {
                msg.warning('该数据不允许修改～！');
                return false;
            }
            var editDailog = top.$.hDialog({
                href: formUrl + 'QueryEngineDefineForm?n=' + Math.random(), title: '修改查询引擎', iconCls: 'icon16_table_edit', width: 660, height: 600,
                onLoad: function () {
                    crud.bindCtrl(rowEdit.ID);
                    var parm = 'key=' + rowEdit.ID;
                    $.ajaxjson('/FrameworkModules/QueryEngineDefineAdmin/GetEntity', parm, function (data) {
                        if (data) {
                            SetWebControls(data, true);
                        }
                        setTimeout(function () { top.$('#QueryEngineId').combotree('setValue', data.QueryEngineId); }, 300);
                        setTimeout(function () { top.$('#DataBaseLinkName').combobox('setValue', data.DataBaseLinkName); }, 300);
                    });
                },
                submit: function () {
                    if (top.$('#uiform').validate().form()) {
                        var queryString = pageMethod.serializeJson(top.$('#uiform'));
                        $.ajaxjson(controlQueryEngineUrl + 'SubmitForm?key=' + rowEdit.ID, queryString, function (d) {
                            if (d.Success) {
                                msg.ok(d.Message);
                                grid.reload(queryEngineTree.selected());
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
        if (row != null) {
            if (row.ALLOWDELETE == '0') {
                msg.warning('该数据不允许删除～！');
                return false;
            }
            var query = 'key=' + row.ID;
            $.messager.confirm('询问提示', '确认要删除选中的数据吗？', function (data) {
                if (data) {
                    $.ajaxjson(controlQueryEngineUrl + 'Delete', query, function (d) {
                        if (d.Success) {
                            msg.ok(d.Message);
                            //重新加载
                            grid.reload(queryEngineTree.selected());
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
    },
    prviewData: function () { //预览数据
        $('#hid_pageNumber').val(1);
        var row = grid.selected();
        if (!row || !row.ID) {
            return false;
        }
        $('#p2').panel({ title: '数据样例：' + row.FULLNAME });
        loadPreviewData(row.ID);
    }
};

function loadPreviewData(id) {
    var parm = 'queryEngineDefineId=' + id + '&pageNumber=' + $('#hid_pageNumber').val() + '&pageSize=' + $('#hid_pageSize').val();
    $.post('/FrameworkModules/QueryEngineDefineAdmin/GetDynamicJsonByQueryEngineDefineId', parm, showGrid, "json")
    .error(function () {
        msg.error("加载数据出错，请检查连接定义或网络连接等！"); 
    });
}

//处理返回结果，并显示数据表格（分页还是有问题，待处理）
function showGrid(data) {
    if (data.data[0].rows.length == 0) {
        msg.warning("没有数据!");
    }
    var options = {
        width: "auto",
        height: "auto",
        fit: true,
        singleSelect: true,
        pagination: true,
        loadMsg: '正在努力加载中....',
        rownumbers: true
    };
    options.columns = eval(data.columns); //把返回的数组字符串转为对象，并赋于datagrid的column属性  
    var tmpGrid = $("#detailGrid");
    tmpGrid.datagrid(options); //根据配置选项，生成datagrid  
    tmpGrid.datagrid("loadData", data.data[0].rows); //载入本地json格式的数据  

    var p = tmpGrid.datagrid('getPager');
    $(p).pagination({
        total: data.data[0].total,
        pageNumber: data.data[0].page,
        //pageSize: 10, //每页显示的记录条数，默认为10 
        pageList: [20, 10, 30, 50], //可以设置每页记录条数的列表 
        beforePageText: '第', //页数文本框前显示的汉字 
        afterPageText: '页    共 {pages} 页',
        displayMsg: '显示 {from} 到 {to}    共 {total} 条记录',
        onSelectPage: function (pageNumber, pageSize) {
            $(this).pagination('loading');
            $(this).pagination('loaded');
            $('#hid_pageNumber').val(pageNumber);
            $('#hid_pageSize').val(pageSize);
            loadPreviewData(grid.selected().ID);
        },
        onChangePageSize: function (pageSize) {
            $('#hid_pageSize').val(pageSize);
            loadPreviewData(grid.selected().ID);
        }
    });
}  