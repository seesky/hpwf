var grd, actionWFCommonBizUrl = '/WorkFlow/WorkFlowCommonBiz/';

$(function () {
    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.databind, height: 30 });
    $('#toolbar').css({
        height: '60px'
    });
    $('#btnSearch').attr('onclick', 'MyParticipantTaskMethod.Search();');
    $('#btnViewTask').attr('onclick', 'MyParticipantTaskMethod.ViewTask();');
    $('#btnViewWfChart').attr('onclick', 'MyParticipantTaskMethod.ViewWFChart();');
    $('#btnProcessStep').attr('onclick', 'MyParticipantTaskMethod.ProcessStep();');
    $('#btnRefresh').attr('onclick', 'MyParticipantTaskMethod.Refreash();');
});

var mygrid = {
    databind: function (size) {
        grd = $('#list').datagrid({
            url: actionWFCommonBizUrl + 'GetWorkFlowAllTaskByPage',
            toolbar: '#toolbar',
            width: size.width,
            height: size.height,
            idField: 'WORKTASKINSID',
            sortName: 'TASKSTARTTIME',
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
                { field: 'ck', checkbox: true, rowspan: 2 },
                { title: '流程编号', field: 'WORKFLOWNO', width: 150, rowspan: 2 },
                { title: '业务名称', field: 'FLOWINSCAPTION', width: 260, rowspan: 2 },
                
                { title: '流程任务', colspan: 6 }, 
                { title: '流程信息', colspan: 3},
                
                { title: '备注', field: 'DESCRIPTION', width: 300, rowspan: 2  },
                { title: 'OPERATORINSID', field: 'OPERATORINSID', width: 0, hidden: true}], 
                [{ title: '任务名称', field: 'TASKINSCAPTION', width: 150, rowspan: 1 },
                { title: '任务提交人', field: 'POPERATEDDES', width: 150, rowspan: 1 },
                { title: '状态', field: 'STATUS', width: 60, rowspan: 1, formatter: function (v, d, i) {
                    if (v == '0') { return '<span style="color:#CCCC66;">保留</span>'; }
                    else if (v == '1') { return '<span style="color:#660033;">未执行</span>'; }
                    else if (v == '2') { return '<span style="color:#CC6600;">执行中</span>'; }
                    else if (v == '3') { return '<span style="color:#CCCC00;">执行完毕</span>'; }
                    else if (v == '4') { return '<span style="color:#FF0033;">异常终止</span>'; }
                    else { return '<span style="color:#CCCCFF;">未知</span>'; }
                }},
                { title: '任务到达时间', field: 'TASKSTARTTIME', width: 144, rowspan: 1 },
                { title: '任务结束时间', field: 'TASKENDTIME', width: 144, rowspan: 1 },
                { title: '处理时间', field: 'OPERDATETIME', width: 144, rowspan: 1 },
                { title: '优先级', field: 'PRIORITY', width: 50, rowspan: 1, formatter: function (v, d, i) {
                    if (v == '1') { return '<span style="color:#0066CC;">普通</span>'; }
                    else if (v == '2') { return '<span style="color:#CC3366;">紧急</span>'; }
                    else if (v == '3') { return '<span style="color:#FF0033;">特急</span>'; }
                    else { return '<span style="color:#666666;">未知</span>'; }
                } },
                { title: '流程开始时间', field: 'FLOWSTARTTIME', width: 144, rowspan: 1 },
                { title: '流程结束时间', field: 'FLOWENDTIME', width: 144, rowspan: 1 }
            ]],
            rowStyler: function (index, row) {
                if (row.PRIORITY == '2') {
                    return 'background-color:#FFCCCC;';
                }
                if (row.PRIORITY == '3') {
                    return 'background-color:#CCCC00;';
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

var MyParticipantTaskMethod = {
    Refreash:function() {
        mygrid.reload();
    },
    Search: function () {
        var wfInsFullName = $('#txtWFInsFullName').val();
        var fromStartDate = $('#txtFromStartDate').val();
        var toStartDate = $('#txtToStartDate').val();
        var ruleArr = [];
        if (wfInsFullName !== '')
            ruleArr.push({ "field": "FLOWINSCAPTION", "op": "cn", "data": escape(wfInsFullName) });
        if (fromStartDate !== '')
            ruleArr.push({ "field": "TASKSTARTTIME", "op": "ge", "data": fromStartDate });
        if (toStartDate !== '')
            ruleArr.push({ "field": "TASKSTARTTIME", "op": "le", "data": toStartDate });

        if (ruleArr.length > 0) {
            var filterObj = { groupOp: 'AND', rules: ruleArr };
            $('#list').datagrid('load', { filter: JSON.stringify(filterObj) });
        } else {
            mygrid.reload();
        }
    },
    ViewTask: function () {
        var selectRow = mygrid.selectedRow();
        if (selectRow) {
            var operatorInsId = selectRow.OPERATORINSID;
            var worktaskInsId = selectRow.WORKTASKINSID;
            var worktaskId = selectRow.WORKTASKID;
            var param = 'operatorInsId=' + operatorInsId + '&worktaskInsId=' + worktaskInsId + '&worktaskId=' + worktaskId + '&workFlowInsId=' + selectRow.WORKFLOWINSID + '&workFlowId=' + selectRow.WORKFLOWID + '&taskInsCaption=' + selectRow.TASKINSCAPTION + '&state=查看';
            window.open('/WorkFlow/ProcessingWorkFlowTask.aspx?' + param, selectRow.FLOWINSCAPTION.replace(/\-/g, ""), 'fullscreen=1,toolbar=no,menubar=no,scrollbars=yes, resizable=yes,location=no, status=no');

        } else {
            msg.warning('请选择要查看的任务。');
            return false;
        }
        return false;
    },
    ViewWFChart: function () {
        var selectRow = mygrid.selectedRow();
        if (selectRow) {
            var workFlowId = selectRow.WORKFLOWID;
            var workFlowInsId = selectRow.WORKFLOWINSID;
            var tmpDailog = top.$.hDialog({
                href: '/WorkFlow/ViewWorkFlowChart.aspx?workFlowId=' + workFlowId + '&workFlowInsId=' + workFlowInsId,
                width: 700,
                height: 600,
                maximizable: true,
                resizable: true,
                max: true, //最大化
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
                buttons: [{
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
    }
};