var actionUrl = '/Admin/FrameworkModules/DailyBizAdmin/';


$(function () {
    pageSizeControl.init({ gridId: 'taskList', gridType: 'datagrid' });
    myWFBizTree.init();
    autoResize({ dataGrid: '#taskList', gridType: 'datagrid', callback: mygrid.bindGrid, height: 30, width: 230 });
    $('#startTask').attr('onclick', 'DailyBizAdminMethod.StartTask();');//开始任务
    $(window).resize(function () {
        pageSizeControl.init({ gridId: 'taskList', gridType: 'datagrid' });
    });
});

var myWFBizTree = {
    init: function () {
        $('#myWFBizTree').tree({
            lines: true,
            url: actionUrl + 'GetAvailableBizClass/',
            animate: true,
            onLoadSuccess: function (node, data) {
                $('body').data('depData', data);
            }, onClick: function (node) {
                showProcess(true, '温馨提示', '加载中...');
                $('#taskList').datagrid('load', { classId: node.id });
            }
        });
    }, 
    getSelected: function () {
        return $('#myWFBizTree').tree('getSelected');
    }
};

var navgrid;
var mygrid = {
    bindGrid: function (size) {
        navgrid = $('#taskList').datagrid({
            url: actionUrl + "GetWorkFlowByClassId",
            title: "任务列表",
            //loadMsg: "正在加载业务流程数据，请稍等...",
            iconCls: 'icon16_list',
            width: size.width,
            height: size.height,
            rownumbers: true, 
            striped: true, 
            idfield: 'WFCLASSID', 
            singleSelect: true, 
            checkOnSelect: true,
            onRowContextMenu: pageContextMenu.createDataGridContextMenu,
            frozenColumns: [[
                { title: '流程名称', field: 'FLOWCAPTION', width: 200, sortable: true, styler: function (value, row, index) {
                    return 'background-color:#ffee00;color:green;';} 
                }
            ]], 
            columns: [[
                { title: '工作流ID', field: 'WORKFLOWID', width: 350 },
                { title: '工作任务ID', field: 'WORKTASKID', width: 350 }
            ]],
            onLoadSuccess:function(data) {
                showProcess(false);
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

var DailyBizAdminMethod = {
    StartTask: function () { //启动任务
        //if ($(this).linkbutton('options').disabled == true) {
        //    return false;
        //}

        var selectRow = mygrid.getSelectedRow();
        if (selectRow) {
            var workFlowId = selectRow.WORKFLOWID;
            var workTaskId = selectRow.WORKTASKID;
            window.open('/WorkFlow/StartWorkFlow.aspx?workFlowId=' + workFlowId + '&workTaskId=' + workTaskId, selectRow.FLOWCAPTION.replace(/\-/g, ""), 'fullscreen=1,toolbar=no,menubar=no,scrollbars=yes, resizable=yes,location=no, status=no');
//            var tmpDailog = top.$.hWindow({
//                href: '/WorkFlow/StartWorkFlow.aspx?workFlowId=' + workFlowId + '&workTaskId=' + workTaskId,
//                width: 800,
//                height: 600,
//                maximizable: true,
//                //max:true, //最大化
//                title: '启动流程',
//                iconCls: 'icon-brick_edit',
//                fit:true,
//                onLoad: function () {
//                   
//                }
//           });
           
        } else {
            msg.warning('请选择待启动的业务流程。');
            return false;
        }
        return false;
    }
};