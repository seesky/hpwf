var grd, actionWFCommonBizUrl = '/WorkFlow/WorkFlowCommonBiz/';

$(function () {
    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.databind, height: 30 });
    $('#toolbar').css({
        height: '60px'
    });
    
    $('#btnSearch').attr('onclick', 'MonitorMethod.Search();');
    $('#btnViewWfChart').attr('onclick', 'MonitorMethod.ViewWFChart();');
    $('#btnProcessStep').attr('onclick', 'MonitorMethod.ProcessStep();');
    $('#btnRefresh').attr('onclick', 'MonitorMethod.Refreash();');
});

var mygrid = {
    databind: function (size) {
        grd = $('#list').datagrid({
            url: actionWFCommonBizUrl + 'GetWorkFlowInstanceDTByPage',
            toolbar: '#toolbar',
            width: size.width,
            height: size.height,
            idField: 'WORKFLOWINSID',
            sortName: 'STARTTIME',
            sortOrder: 'desc',
            striped: true,
            pagination: true,
            singleSelect: true,
            selectOnCheck: true,
            checkOnSelect: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            pageSize: 20,
            pageList: [20, 10, 30, 50],
            columns: [[
                { field: 'ck', checkbox: true },
                { title: '流程编号', field: 'WORKFLOWNO', width: 150 },
                { title: '流程实例名称', field: 'FLOWINSCAPTION', width: 260 },
                { title: '开始时间', field: 'STARTTIME', width: 144 },
                { title: '结束时间', field: 'ENDTIME', width: 144 },
                { title: '当前状态', field: 'STATUS', width: 100, formatter: function (value, row, index) {
                    if (value == '1') {
                        return '还未执行';
                    } else if (value == '2') {
                        return '正在办理';
                    } else if (value == '3') {
                        return '正常结束';
                    } else if (value == '4') {
                        return '流程废弃';
                    } else if (value == '5') {
                        return '流程挂起';
                    } else {
                        return '未知状态';
                    }
                }
                },
                { title: '说明', field: 'DESCRIPTION', width: 300 }
            ]],
            rowStyler: function(index, row) {
                if (row.STATUS == '1') {
                    return 'background-color:orange;';
                } else if (row.STATUS == '2') {
                    return 'background-color:#FFFFCC;';
                } else if (row.STATUS == '3') {
                    return 'background-color:green;';
                } else if (row.STATUS == '4') {
                    return 'background-color:silver;';
                } else if (row.STATUS == '5') {
                    return 'background-color:black;';
                } else {
                    
                }
            }
        });
    },
    reload: function () {
        grd.datagrid('reload', {});
    },
    selectedRow: function () {
        return grd.datagrid('getSelected');
    }
};

var MonitorMethod = {
    Refreash:function() {
        mygrid.reload();
    },
    Search: function () {
        var wfInsFullName = $('#txtWFInsFullName').val();
        var fromStartDate = $('#txtFromStartDate').val();
        var toStartDate = $('#txtToStartDate').val();
        var ruleArr = [];
        if (wfInsFullName !== '')
            ruleArr.push({ "field": "FLOWINSCAPTION", "op": "cn", "data": wfInsFullName });
        if (fromStartDate !== '')
            ruleArr.push({ "field": "STARTTIME", "op": "ge", "data": fromStartDate });
        if (toStartDate !== '')
            ruleArr.push({ "field": "STARTTIME", "op": "le", "data": toStartDate });

        if (ruleArr.length > 0) {
            var filterObj = { groupOp: 'AND', rules: ruleArr };
            $('#list').datagrid('load', { filter: JSON.stringify(filterObj) });
        } else {
            mygrid.reload();
        }
    },
    ProcessStep: function () {
        var selectRow = mygrid.selectedRow();
        if (selectRow) {
            var workFlowInsId = selectRow.WORKFLOWINSID;
            var tmpProcessStepDialog = top.$.hDialog({
                content: '<div id="tmpGridList" style="width:100px;"></div>',
                width: 730,
                height: 580,
                title: '流程处理记录(流程轨迹)',
                iconCls: 'icon16_page_white_text',
                buttons:[{
                    text: '关闭',
                    iconCls: 'icon16_cancel',
                    handler: function () {
                        tmpProcessStepDialog.dialog("close");
                    }
                }],
                onOpen: function () {
                    top.$('#tmpGridList').datagrid({
                        url: '/WorkFlow/WorkFlowCommonBiz/GetWorkFlowHistory?workFlowInsId=' + workFlowInsId,
                        singleSelect: true,
                        selectOnCheck: true,
                        checkOnSelect: true,
                        width: 700,
                        height: 500,
                        idField: 'WORKTASKINSID',
                        sortName: 'TASKENDTIME',
                        sortOrder: 'asc',
                        pagination: false,
                        rownumbers: true,
                        columns: [[
                                { field: 'ck', checkbox: true },
                                { title: '流程名称', field: 'FLOWCAPTION', width: 150 },
                                { title: '任务名称', field: 'TASKCAPTION', width: 150, sortable: true },
                                { title: '任务处理者', field: 'OPERATEDDES', width: 300 },
                                { title: '处理时间', field: 'TASKENDTIME', width: 150 },
                                { title: '处理者ID', field: 'OPERATORINSID', width: 200 }
                            ]]
                    });
                }
            });
        } else {
            msg.warning('请选择待查看的流程。');
            return false;
        }
        return false;
    },
    ViewWFChart: function () {
        var selectRow = mygrid.selectedRow();
        if (selectRow) {
            var workFlowId = selectRow.WORKFLOWID;
            var workFlowInsId = selectRow.WORKFLOWINSID;
            //window.open('ViewWorkFlowChart.aspx?workFlowId=' + workFlowId + '&workFlowInsId=' + workFlowInsId, selectRow.FLOWCAPTION.replace(/\-/g, ""), 'fullscreen=1,toolbar=no,menubar=no,scrollbars=no, resizable=yes,location=no, status=no');
            var tmpDailog = top.$.hDialog({
                href: '/WorkFlow/ViewWorkFlowChart.aspx?workFlowId=' + workFlowId + '&workFlowInsId=' + workFlowInsId,
                width: 700,
                height: 600,
                maximizable: true,
                resizable:true,
                //max:true, //最大化
                title: '流程监视器',
                iconCls: 'icon16_monitort',
                buttons: [{
                    text: '关闭',
                    iconCls: 'icon16_cancel',
                    handler: function () {
                        tmpDailog.dialog("close");
                    }
                }]
            });

        } else {
            msg.warning('请选择待查看的流程。');
            return false;
        }
        return false;
    }
};