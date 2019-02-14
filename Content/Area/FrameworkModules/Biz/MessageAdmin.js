$(function () {
    pageSizeControl.init({ gridId: 'messageList', gridType: 'datagrid' });
    pdfTree.init();
    autoResize({ dataGrid: '#messageList', gridType: 'datagrid', callback: mygrid.bindGrid, height: 35, width: 230 });
    $('#sendMessage').attr('onclick', 'MessageAdminMethod.sendMessage();');
    $('#readMessage').attr('onclick', 'MessageAdminMethod.readMessage();');
    $('#broadcastMessage').attr('onclick', 'MessageAdminMethod.broadcastMessage();');
    $('#delMessage').attr('onclick', 'MessageAdminMethod.delMessage();');
    $('#refresh').click(function () { //刷新
        mygrid.reload();
    });
});

var pdfTree = {
    init: function () {
        $('#messageCategoryTree').tree({
            lines: true,
            data: [{
                text: '消息功能分类',
                state: 'open',
                iconCls: 'icon16_email_trace',
                children: [{
                    id: 'Message',
                    text: '消息',
                    iconCls: 'icon16_flag_blue'
                }, {
                    id: 'Remind',
                    text: '提示',
                    iconCls: 'icon16_flag_green'
                }, {
                    id: 'UserMessage',
                    text: '用户信息',
                    iconCls: 'icon16_flag_pink'
                }, {
                    id: 'Warning',
                    text: '警示',
                    iconCls: 'icon16_flag_orange'
                }, {
                    id: 'WaitForAudit',
                    text: '待审核事项',
                    iconCls: 'icon16_flag_purple'
                }, {
                    id: 'TodoList',
                    text: '待审核',
                    iconCls: 'icon16_flag_red'
                }, {
                    id: 'RoleMessage',
                    text: '角色信息',
                    iconCls: 'icon16_flag_1'
                }, {
                    id: 'OrganizeMessage',
                    text: '组织机构信息',
                    iconCls: 'icon16_flag_2'
                }, {
                    id: 'SystemPush',
                    text: '系统推送',
                    iconCls: 'icon16_flag_finish'
                }]
            }],
            animate: true,
            onClick: function (node) {
                layer.closeAll('tips');
                $('#messageList').datagrid('load', { functionCode: node.id });
            },
            onSelect: function (node) {
                $(this).tree('expand', node.target);
            }
        });
    },
    getCurrentId: function () {
        return $('#messageCategoryTree').tree('getSelected').id;
    }
};

var navgrid;
var mygrid = {
    bindGrid: function (size) {
        navgrid = $('#messageList').datagrid({
            url: '/Admin/FrameworkModules/MessageAdmin/GetMessageListByFunctionCode/',
            loadMsg: "正在加载消息列表，请稍等...",       
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
                if (row.ISNEW <= 0) {
                    return 'color:#999;'; //显示为灰色字体
                }
            },
            onDblClickRow: function (rowIndex, rowData) {
                document.getElementById('readMessage').click();
            },
            onClickCell: function (rowIndex, field, value) {
                if (field == 'MSGCONTENT') {
                    layer.tips(value, {
                        tips: [1, '#3595CC'],
                        time: 2
                    });
                }
            },
            columns: [[
                { field: 'ck', checkbox: true },
                { title: '功能代码', field: 'FUNCTIONCODE', width: 100, sortable: true },
                { title: '分类代码', field: 'CATEGORYCODE', width: 100, sortable: true },
                { title: '主题', field: 'TITLE', width: 100 },
                { title: '内容', field: 'MSGCONTENT', width: 260 },
                { title: '接收者', field: 'RECEIVERREALNAME', width: 100 },
                { title: '新消息', field: 'ISNEW', width: 60, align: 'center', formatter: statusFormatter },
                { title: '阅读次数', field: 'READCOUNT', width: 60, align: 'right' },
                { title: '阅读日期', field: 'READDATE', width: 130 },
                { title: 'IP地址', field: 'IPADDRESS', width: 60 },
                { title: '发送者', field: 'CREATEBY', width: 100 },
                { title: '状态', field: 'ENABLED', width: 60, align: 'center', formatter: statusFormatter1 }
            ]]
        });
    },
    reload: function () {
        layer.closeAll('tips');
        navgrid.datagrid('reload');
    },
    selected: function () {
        return navgrid.datagrid('getSelected');
    }
};

function statusFormatter(value) {
    if (value == 1) {
        return "<div style='font-weight:700;color:yellow;background-color:green;margin:0px;padding:0px;'>是</div>";
    } else {
        return "<div style='font-weight:700;color:red;background-color:#CCCCCC;text-decoration:line-through'>否</div>";
    }
}

function statusFormatter1(value) {
    if (value == 1) {
        return "<div style='font-weight:700;color:yellow;background-color:green;margin:0px;padding:0px;'>是</div>";
    } else {
        return "<div style='font-weight:700;color:white;background-color:green;margin:0px;padding:0px;'>否</div>";
    }
}

var MessageAdminMethod = {
    sendMessage: function () {   
        var sendDailog = top.$.hDialog({
            id: 'sendMessage', title: '发送消息', width: 1000, height: 500, href: '/Admin/FrameworkModules/MessageAdmin/SendMessageForm/', iconCls: 'icon16_comment_edit',
            buttons: [
                    {
                        text: '发 送',
                        iconCls: 'icon16_email_to_friend',
                        handler: function () {
                            window.setTimeout(function () {
                                var AddresseeJson = new Array();
                                top.$("#AddresseeList").find("a").each(function () {
                                    //var Addressee = { Id: $(this).attr('id'), AddresseeName: $(this).html() };
                                    var Addressee = { Id: $(this).attr('id') };
                                    AddresseeJson.push(JSON.stringify(Addressee));
                                });

                                var postData = {
                                    Title: top.$('#Title').val(),                              //内容              
                                    MSGContent: top.$('#MSGContent').val(),                     //内容
                                    AddresseeJson: "[" + eval(AddresseeJson) + "]",             //收件人Json               
                                };
                                $.ajaxjson("/Admin/FrameworkModules/MessageAdmin/SendMessage/", postData, function (d) {
                                    if (d.Success) {
                                        msg.ok(d.Message);
                                        sendDailog.dialog('close');
                                        mygrid.reload();
                                    } else {
                                        MessageOrRedirect(d);
                                    }
                                });
                            }, 200);
                            return false;
                        }
                    },
                    {
                        text: '关 闭',
                        iconCls: 'icon16_application_form_delete',
                        handler: function () {
                            sendDailog.dialog('close');
                            return false;
                        }
                    }
            ],
            onLoad: function () {
                top.$('#Title').focus();
            },
            submit: function () {
                return false;
            }
        });
        return false;
    },
    readMessage: function () {
        var row = mygrid.selected();
        if (row) {
            var parm = 'key=' + row.ID;
            $.ajaxjson("/Admin/FrameworkModules/MessageAdmin/ReadMessage/", parm, function (d) {
                if (d.Success) {
                    $('#messageList').datagrid('load', { functionCode: $('#messageCategoryTree').tree('getSelected').id }); 
                } else {
                    //top.$.messager.alert('Warning', '标记为已读失败！');
                    msg.warning('标记为已读失败!');
                }
            });
        } else {
            msg.warning('请选择数据');
        }
        return false;
    },
    broadcastMessage:function() {
        var broadcastDailog = top.$.hDialog({
            id: 'broadcastMessage', title: '广播消息', width: 1000, height: 470, href: '/Admin/FrameworkModules/MessageAdmin/BroadcastMessageForm/', iconCls: 'icon16_comments_add',
            buttons: [
                    {
                        text: '发 送',
                        iconCls: 'icon16_email_to_friend',
                        handler: function () {
                            var messageControl = top.$('#MSGContent');
                            if (messageControl.val() && messageControl.val().length >= 10 && messageControl.val().length <=500) {
                                top.$.messager.confirm('询问提示', '你确定广播本条消息吗?', function (r) {
                                    if (r) {
                                        window.setTimeout(function () {
                                            var postData = {
                                                message: messageControl.val()  //内容             
                                            };
                                            $.ajaxjson("/Admin/FrameworkModules/MessageAdmin/BroadcastMessage/", postData, function (d) {
                                                if (d.Success) {
                                                    //top.$.messager.show('message', d.Message);
                                                    msg.ok(d.Message);
                                                    broadcastDailog.dialog('close');
                                                    mygrid.reload();
                                                } else {
                                                    MessageOrRedirect(d);
                                                }
                                            });
                                        }, 200);
                                    }
                                });
                            } else {
                                if (messageControl.val() && messageControl.val().length <= 10) {
                                    top.$.messager.alert('Warning', '亲，信息内容长度不能小于10！');
                                } else if (messageControl.val() && messageControl.val().length > 500) {
                                    top.$.messager.alert('Warning', '亲，信息内容长度不能大于500！');
                                }else {
                                    top.$.messager.alert('Warning', '亲，信息内容不能为空！');
                                }
                                messageControl.focus();
                            }
                            return false;
                        }
                    },
                    {
                        text: '关 闭',
                        iconCls: 'icon16_application_form_delete',
                        handler: function () {
                            broadcastDailog.dialog('close');
                            return false;
                        }
                    }
            ],
            onLoad: function () {
                top.$('#MSGContent').focus();
            },
            submit: function () {
                return false;
            }
        });
        return false;
    },
    delMessage: function () {
        var row = mygrid.selected();
        if (row) {
            $.messager.confirm('询问提示', '确认删除选中的数据吗?', function (data) {
                if (data) {
                    var parm = 'key=' + row.ID;
                    $.ajaxjson("/Admin/FrameworkModules/MessageAdmin/Delete/", parm, function (d) {
                        if (d.Data > 0) {
                            msg.ok('删除成功。');
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