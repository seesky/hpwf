var grd, actionWFCommonBizUrl = '/WorkFlow/WorkFlowCommonBiz/';

$(function () {
    autoResize({ dataGrid: '#list', gridType: 'datagrid', callback: mygrid.databind, height: 30 });
    
    $('#btnSearch').attr('onclick', 'search();');
    $('#btnRefresh').attr('onclick', 'refreash();');
    $('#btnClaimTask').attr('onclick', 'claimTask();');
    $('#toolbar').css({
        height: '60px'
    });
});

var mygrid = {
    databind: function (size) {
        grd = $('#list').datagrid({
            url: actionWFCommonBizUrl + 'GetMyUnClaimedTaskList',
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
                { field: 'ck', checkbox: true },
                { title: '流程编号', field: 'WORKFLOWNO', width: 150 },
                { title: '业务名称', field: 'FLOWINSCAPTION', width: 260 },
                { title: '任务名称', field: 'TASKINSCAPTION', width: 150 },
                { title: '任务提交人', field: 'POPERATEDDES', width: 150 },
                { title: '优先级', field: 'PRIORITY', width: 50, formatter: function (v, d, i) {
                        if (v == '1') { return '<span style="color:#0066CC;">普通</span>'; }
                        else if (v == '2') { return '<span style="color:#CC3366;">紧急</span>'; }
                        else if (v == '3') { return '<span style="color:#FF0033;">特急</span>'; }
                        else { return '<span style="color:#666666;">未知</span>'; }
                    }
                },
                { title: '任务到达时间', field: 'TASKSTARTTIME', width: 144 },
                { title: '流程开始时间', field: 'FLOWSTARTTIME', width: 144 },
                { title: '备注', field: 'DESCRIPTION', width: 300 },
                { title: 'OPERATORINSID', field: 'OPERATORINSID', width: 0,hidden:true }
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

function refreash() {
    mygrid.reload();
}

function search() {
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
}

function claimTask() {
    var row = mygrid.selectedRow();
    if (row) {
        var query = 'operatorId=' + row.OPERATORINSID + "&workTaskInsId=" + row.WORKTASKINSID;
        $.messager.confirm('询问提示', '确认认领任务[' + row.FLOWINSCAPTION + ']吗？', function (data) {
            if (data) {
                $.ajaxjson(actionWFCommonBizUrl + 'ClaimTask', query, function (d) {
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
        msg.warning('请选择要认领的任务!');
        return false;
    }
    return false;
}