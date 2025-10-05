var formUrl = "/Admin/FrameworkModules/UserAdmin/Form/";

layui.use(['tree', 'table', 'layer', 'form', 'dropdown', 'util'], function () {
    var tree = layui.tree;
    var table = layui.table;
    var layer = layui.layer;
    var form = layui.form;
    var dropdown = layui.dropdown;
    var util = layui.util;
    var $ = layui.$;

    var escapeHtml = typeof util.escape === 'function' ? util.escape : function (str) {
        return String(str || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    };
    var throttle = typeof util.throttle === 'function' ? util.throttle : function (fn, wait) {
        var timeout;
        return function () {
            var context = this;
            var args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(function () {
                fn.apply(context, args);
            }, wait || 200);
        };
    };

    var state = {
        organizeId: null,
        currentRow: null,
        searchValue: ''
    };

    var iconMap = {
        'icon16_arrow_refresh': 'layui-icon-refresh',
        'icon16_user_add': 'layui-icon-add-1',
        'icon16_user_edit': 'layui-icon-edit',
        'icon16_user_delete': 'layui-icon-delete',
        'icon16_user_level_filtering': 'layui-icon-password',
        'icon16_aol_messenger': 'layui-icon-group',
        'icon16_user_go': 'layui-icon-export'
    };

    var mygrid = {
        reload: function (reset) {
            reloadTable(reset);
        },
        getSelectedRow: function () {
            return state.currentRow;
        }
    };

    var UserAdminMethod = {
        Refreash: function () {
            reloadTable();
        },
        SearchData: function () {
            state.searchValue = $.trim($('#txtSearchValue').val());
            reloadTable(true);
        },
        ExportData: function () {
            var exportFields = [
                { title: '编号', field: 'CODE' },
                { title: '登录名', field: 'USERNAME' },
                { title: '用户名', field: 'REALNAME' },
                { title: '性别', field: 'GENDER' },
                { title: '公司名称', field: 'COMPANYNAME' },
                { title: '部门名称', field: 'DEPARTMENTNAME' },
                { title: '邮箱', field: 'EMAIL' },
                { title: '出生日期', field: 'BIRTHDAY' },
                { title: '手机', field: 'MOBILE' },
                { title: 'QQ', field: 'QICQ' },
                { title: '有效', field: 'ENABLED' },
                { title: '描述', field: 'DESCRIPTION' }
            ];
            var content = ['<div style="padding:12px 20px 4px;">'];
            content.push('<p style="margin-bottom:8px;">请选择要导出的字段：</p>');
            content.push('<div class="layui-form" style="max-height:260px;overflow:auto;">');
            exportFields.forEach(function (item, idx) {
                content.push('<input type="checkbox" lay-skin="primary" lay-filter="exportField" name="exportField" value="' + item.field + '" title="' + item.title + '"' + (idx < 6 ? ' checked' : '') + ' />');
            });
            content.push('</div></div>');
            layer.open({
                type: 1,
                title: '导出Excel数据',
                area: ['360px', '420px'],
                btn: ['导出', '取消'],
                content: content.join(''),
                success: function () {
                    form.render('checkbox');
                },
                yes: function (index, layero) {
                    var checked = [];
                    layero.find('input[name="exportField"]:checked').each(function () {
                        checked.push($(this).val());
                    });
                    if (!checked.length) {
                        layer.msg('请至少选择一个字段');
                        return false;
                    }
                    var fields = checked.join(',');
                    var query = '/Admin/FrameworkModules/Utility/ExportExcel?tableName=PIUSER&sortField=SORTCODE&fields=' + encodeURIComponent(fields) + '&filters=';
                    window.open(query);
                    layer.close(index);
                }
            });
        },
        AddUser: function () {
            openUserFormDialog({
                title: '添加用户',
                onLoad: function (iframeWin) {
                    if (iframeWin && iframeWin.UserForm) {
                        iframeWin.UserForm.initForAdd();
                    }
                },
                onSubmit: function (data, dialogIndex) {
                    $.ajaxjson('/Admin/FrameworkModules/UserAdmin/SubmitForm/', data, function (d) {
                        if (d.Success) {
                            layer.msg(d.Message || '操作成功');
                            layer.close(dialogIndex);
                            reloadTable();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            });
        },
        EditUser: function () {
            var selectRow = state.currentRow;
            if (!selectRow) {
                layer.msg('请选择待修改的用户');
                return false;
            }
            if (selectRow.USERNAME === 'Administrator' && curUserinfo && selectRow.ID !== curUserinfo.id) {
                layer.msg('你不能修改超级管理员用户！');
                return false;
            }
            openUserFormDialog({
                title: '修改用户',
                onLoad: function (iframeWin) {
                    $.ajaxjson('/Admin/FrameworkModules/UserAdmin/GetEntity/', 'key=' + selectRow.ID, function (data) {
                        if (iframeWin && iframeWin.UserForm && data) {
                            var entity = typeof data === 'string' ? JSON.parse(data) : data;
                            iframeWin.UserForm.setFormData(entity);
                        }
                    });
                },
                onSubmit: function (data, dialogIndex) {
                    $.ajaxjson('/Admin/FrameworkModules/UserAdmin/SubmitForm/?key=' + selectRow.ID, data, function (d) {
                        if (d.Success) {
                            layer.msg(d.Message || '操作成功');
                            layer.close(dialogIndex);
                            reloadTable();
                        } else {
                            MessageOrRedirect(d);
                        }
                    });
                }
            });
            return false;
        },
        DeleteUser: function () {
            var selectRow = state.currentRow;
            if (!selectRow) {
                layer.msg('请选择要删除的用户');
                return false;
            }
            if (selectRow.USERNAME === 'Administrator') {
                layer.msg('不能删除超级管理员！');
                return false;
            }
            if (curUserinfo && selectRow.ID === curUserinfo.id) {
                layer.msg('不能删除当前登录用户！');
                return false;
            }
            layer.confirm('确认要删除用户【' + escapeHtml(selectRow.REALNAME || selectRow.USERNAME) + '】吗？', { icon: 3, title: '提示' }, function (index) {
                $.ajaxjson('/Admin/FrameworkModules/UserAdmin/Delete/', 'key=' + selectRow.ID, function (d) {
                    if (d.Success) {
                        layer.msg(d.Message || '操作成功');
                        reloadTable();
                    } else {
                        MessageOrRedirect(d);
                    }
                });
                layer.close(index);
            });
            return false;
        },
        SetUserPassword: function () {
            var selectRow = state.currentRow;
            if (!selectRow) {
                layer.msg('请选择要修改密码的用户');
                return false;
            }
            if (selectRow.USERNAME === 'Administrator' && curUserinfo && selectRow.ID !== curUserinfo.id) {
                layer.msg('不能修改超级管理员密码');
                return false;
            }
            openPasswordDialog(selectRow);
            return false;
        },
        LogByUser: function () {
            var selectRow = state.currentRow;
            if (!selectRow) {
                layer.msg('请选择一个用户！');
                return false;
            }
            layer.msg('加载中…', { icon: 16, time: 500 });
            AddToTab('用户访问详情', '/Admin/FrameworkModules/LogAdmin/LogByUser/', 'icon16_diagnostic_chart', 'pageLogByUser');
            window.setTimeout(function () {
                var frame = parent.$('#pageLogByUser')[0];
                if (frame && frame.contentWindow) {
                    frame.contentWindow.$('#txtOpuser').val(selectRow.REALNAME);
                    if (typeof frame.contentWindow.Search === 'function') {
                        frame.contentWindow.Search();
                    }
                }
            }, 1200);
            return false;
        },
        LogByGeneral: function () {
            AddToTab('用户访问情况', '/Admin/FrameworkModules/LogAdmin/LogByGeneral/', 'icon16_address_block', 'pageLogByGeneral');
            return false;
        },
        Dimission: function () {
            var selectRow = state.currentRow;
            if (!selectRow) {
                layer.msg('请选择一个用户！');
                return false;
            }
            if (selectRow.USERNAME && (selectRow.USERNAME === 'Administrator' || selectRow.USERNAME === 'Admin')) {
                layer.msg('请选择非管理员用户');
                return false;
            }
            AddToTab('用户离职', '/Admin/FrameworkModules/UserAdmin/UserDimission/', 'icon16_aol_messenger', 'pageUserDimission');
            window.setTimeout(function () {
                var frame = parent.$('#pageUserDimission')[0];
                if (frame && frame.contentWindow && typeof frame.contentWindow.BindPage === 'function') {
                    frame.contentWindow.BindPage(selectRow.ID);
                    frame.contentWindow.$('#Id').val(selectRow.ID);
                }
            }, 800);
            return false;
        }
    };

    window.mygrid = mygrid;
    window.UserAdminMethod = UserAdminMethod;

    enhanceToolbar();
    bindToolbarActions();
    initTree();
    initTable();
    bindGlobalEvents();

    function enhanceToolbar() {
        $('#toolbar .datagrid-btn-separator').remove();
        $('#toolbar a.easyui-linkbutton').each(function () {
            var $btn = $(this);
            var icon = $btn.attr('icon');
            var iconCls = iconMap[icon];
            var disabled = $btn.is('[disabled]');
            $btn.removeClass('easyui-linkbutton').addClass('layui-btn layui-btn-sm');
            if (iconCls) {
                $btn.prepend('<i class="layui-icon ' + iconCls + '"></i> ');
            }
            if (disabled) {
                $btn.addClass('layui-btn-disabled').attr('disabled', true);
            }
        });

        var $splitBtn = $('#sb');
        if ($splitBtn.length) {
            $splitBtn.addClass('layui-btn layui-btn-primary layui-btn-sm');
        }

        var $menu = $('#mm');
        if ($menu.length && $splitBtn.length) {
            var data = [];
            $menu.children('div').each(function () {
                var $item = $(this);
                data.push({
                    id: $item.attr('id'),
                    title: $.trim($item.text()),
                    disabled: $item.attr('disabled') === 'True' || $item.attr('disabled') === 'true'
                });
            });
            dropdown.render({
                elem: '#sb',
                data: data,
                click: function (item) {
                    if (item.disabled) {
                        return false;
                    }
                    if (item.id === 'btnLogByUser') {
                        UserAdminMethod.LogByUser();
                    } else if (item.id === 'btnLogByGeneral') {
                        UserAdminMethod.LogByGeneral();
                    }
                }
            });
            $menu.remove();
        }
    }

    function bindToolbarActions() {
        bindButton('#a_refresh', UserAdminMethod.Refreash);
        bindButton('#a_add', UserAdminMethod.AddUser);
        bindButton('#a_edit', UserAdminMethod.EditUser);
        bindButton('#a_delete', UserAdminMethod.DeleteUser);
        bindButton('#a_editpassword', UserAdminMethod.SetUserPassword);
        bindButton('#a_export', UserAdminMethod.ExportData);
        bindButton('#a_dimission', UserAdminMethod.Dimission);
        $('#btnSearch').on('click', function () {
            UserAdminMethod.SearchData();
        });
        $('#txtSearchValue').on('keypress', function (evt) {
            if (evt.which === 13) {
                evt.preventDefault();
                UserAdminMethod.SearchData();
            }
        });
    }

    function bindButton(selector, handler) {
        var $btn = $(selector);
        if (!$btn.length) {
            return;
        }
        if ($btn.is('[disabled]') || $btn.hasClass('layui-btn-disabled')) {
            $btn.on('click', function (e) { e.preventDefault(); });
            return;
        }
        $btn.on('click', function (e) {
            e.preventDefault();
            handler();
        });
    }

    function initTree() {
        $.getJSON('/Admin/FrameworkModules/OrganizeAdmin/GetOrganizeTreeJson/?isTree=1', function (data) {
            var treeData = normalizeTree(data || []);
            tree.render({
                elem: '#organizeTree',
                onlyIconControl: true,
                data: treeData,
                click: function (obj) {
                    if (obj && obj.data) {
                        state.organizeId = obj.data.id;
                        reloadTable(true);
                    }
                }
            });
            if (treeData.length) {
                state.organizeId = treeData[0].id;
                reloadTable(true);
            }
        });
    }

    function normalizeTree(nodes) {
        return $.map(nodes, function (item) {
            var children = item.children || item.ChildNodes || [];
            return {
                id: item.id || item.ID,
                title: item.text || item.fullname || item.name,
                spread: !!item.checked || (children && children.length > 0),
                children: normalizeTree(children)
            };
        });
    }

    function initTable() {
        table.render({
            elem: '#userTable',
            id: 'userTable',
            url: '/Admin/FrameworkModules/UserAdmin/GetUserPageDTByDepartmentId/',
            method: 'post',
            height: 'full-210',
            page: true,
            limit: 20,
            limits: [20, 30, 50, 100],
            request: {
                pageName: 'page',
                limitName: 'rows'
            },
            where: {
                organizeId: state.organizeId,
                searchValue: state.searchValue
            },
            parseData: function (res) {
                if (typeof res === 'string') {
                    try {
                        res = JSON.parse(res);
                    } catch (e) {
                        res = {};
                    }
                }
                return {
                    code: 0,
                    msg: '',
                    count: res.total || 0,
                    data: res.rows || []
                };
            },
            cols: [[
                { type: 'radio', fixed: 'left', width: 48 },
                { field: 'CODE', title: '编号', width: 140 },
                { field: 'USERNAME', title: '登录名', width: 140 },
                { field: 'REALNAME', title: '用户名', width: 140 },
                { field: 'ENABLED', title: '有效', width: 110, align: 'center', templet: '#enabledTpl' },
                { field: 'ISDIMISSION', title: '离职', width: 90, align: 'center', templet: '#dimissionTpl' },
                { field: 'GENDER', title: '性别', width: 80, align: 'center', templet: '#genderTpl' },
                { field: 'EMAIL', title: '邮箱地址', width: 200 },
                { field: 'MOBILE', title: '手机号码', width: 130 },
                { field: 'COMPANYNAME', title: '所在单位/公司', width: 180 },
                { field: 'SUBCOMPANYNAME', title: '所在子公司', width: 180 },
                { field: 'DEPARTMENTNAME', title: '所在部门', width: 160 },
                { field: 'SUBDEPARTMENTNAME', title: '所在子部门', width: 160 },
                { field: 'WORKGROUPNAME', title: '所在工作组', width: 160 },
                { field: 'PREVIOUSVISIT', title: '上次登录时间', width: 180 },
                { field: 'LOGONCOUNT', title: '登录次数', width: 100, align: 'center' },
                { field: 'IPADDRESS', title: 'IP地址', width: 140 },
                { field: 'DESCRIPTION', title: '描述', minWidth: 200 }
            ]],
            done: function (res, curr, count) {
                var $tbody = $('#userTable').next('.layui-table-view').find('.layui-table-body tbody');
                $tbody.children('tr').each(function (i) {
                    var row = res.data[i];
                    if (row && (row.ENABLED === 0 || row.ENABLED === '0')) {
                        $(this).addClass('layui-disabled-row');
                    }
                });
            }
        });

        table.on('row(userTable)', function (obj) {
            state.currentRow = obj.data;
            obj.tr.addClass('layui-table-click').siblings().removeClass('layui-table-click');
        });

        table.on('rowDouble(userTable)', function (obj) {
            state.currentRow = obj.data;
            UserAdminMethod.EditUser();
        });

        form.on('switch(enabledSwitch)', function (obj) {
            var $elem = $(obj.elem);
            var userId = $elem.data('user-id');
            var original = Number($elem.data('original-enabled')) || 0;
            var newStatus = obj.elem.checked ? 1 : 0;
            updateUserEnabled(userId, original, function (success) {
                if (success) {
                    $elem.data('original-enabled', newStatus);
                } else {
                    obj.elem.checked = original === 1;
                    form.render('checkbox');
                }
            });
        });
    }

    function reloadTable(resetPage) {
        state.currentRow = null;
        if (!state.organizeId) {
            table.reload('userTable', {
                where: { organizeId: '', searchValue: state.searchValue },
                data: []
            });
            return;
        }
        table.reload('userTable', {
            where: {
                organizeId: state.organizeId,
                searchValue: state.searchValue
            },
            page: resetPage ? { curr: 1 } : {}
        });
    }

    function updateUserEnabled(userId, original, callback) {
        if (!userId) {
            callback(false);
            return;
        }
        $.ajaxjson('/FrameworkModules/UserAdmin/SetUserEnabled', 'userId=' + userId + '&isEnabled=' + original, function (d) {
            if (d.Success) {
                layer.msg('状态更新成功');
                reloadTable();
                callback(true);
            } else {
                MessageOrRedirect(d);
                callback(false);
            }
        });
    }

    function openUserFormDialog(options) {
        var index = layer.open({
            type: 2,
            title: options.title,
            area: ['720px', '720px'],
            shadeClose: false,
            resize: false,
            content: formUrl,
            btn: ['保存', '取消'],
            success: function (layero, idx) {
                var iframeWin = window['layui-layer-iframe' + idx];
                if (options.onLoad) {
                    options.onLoad(iframeWin, idx);
                }
            },
            yes: function (idx, layero) {
                var iframeWin = window['layui-layer-iframe' + idx];
                if (!iframeWin || !iframeWin.UserForm) {
                    return false;
                }
                if (!iframeWin.UserForm.validate()) {
                    return false;
                }
                var data = iframeWin.UserForm.getData();
                options.onSubmit && options.onSubmit(data, idx, layero);
                return false;
            }
        });
        return index;
    }

    function openPasswordDialog(row) {
        var tpl = [
            '<form class="layui-form" style="padding:18px 24px 6px;" lay-filter="passwordForm">',
            '  <div class="layui-form-item">',
            '    <label class="layui-form-label">登录名</label>',
            '    <div class="layui-input-block">',
            '      <input type="text" class="layui-input" value="' + escapeHtml(row.USERNAME + ' | ' + (row.REALNAME || '')) + '" readonly />',
            '    </div>',
            '  </div>',
            '  <div class="layui-form-item">',
            '    <label class="layui-form-label">新密码</label>',
            '    <div class="layui-input-block">',
            '      <input type="password" name="password" lay-verify="required" autocomplete="off" placeholder="请输入新密码" class="layui-input" />',
            '    </div>',
            '  </div>',
            '</form>'
        ].join('');
        layer.open({
            type: 1,
            title: '设置用户密码',
            area: ['360px', '220px'],
            btn: ['保存', '取消'],
            content: tpl,
            success: function (layero) {
                form.render();
            },
            yes: function (index, layero) {
                var password = layero.find('input[name="password"]').val();
                if (!password || password.length < 6) {
                    layer.msg('请输入至少6位的新密码');
                    return false;
                }
                $.ajaxjson('/Admin/FrameworkModules/UserAdmin/SetUserPassword/', { userId: row.ID, password: password }, function (d) {
                    if (d.Success) {
                        layer.msg('密码修改成功，请牢记新密码！');
                        layer.close(index);
                        reloadTable();
                    } else {
                        MessageOrRedirect(d);
                    }
                });
                return false;
            }
        });
    }

    function bindGlobalEvents() {
        $(window).on('resize', throttle(function () {
            table.resize('userTable');
        }, 200));
    }
});

function SetUserEnabled() {
    // 已转换为基于layui switch的交互，保留函数以兼容旧引用。
    return false;
}
