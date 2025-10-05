(function (global) {
    'use strict';

    var HPWFIndex = {
        onlyOpenTitle: '我的桌面',
        openTabs: 7,
        tabFilter: 'mainTabs',
        homeTabId: 'home-tab',
        contextMenuSelector: '#closeMenu',
        homeUrl: '/Admin/StartPage',
        modules: {},
        loadingIndex: null,

        init: function (options) {
            options = options || {};
            if (!global.layui) {
                console.warn('Layui is required to initialize the HPWF admin shell.');
                return;
            }

            this.modules.element = options.element || layui.element;
            this.modules.layer = options.layer || layui.layer;
            this.modules.form = options.form || layui.form;
            this.modules.util = options.util || layui.util;
            this.modules.$ = options.$ || layui.$ || global.jQuery;

            if (options.onlyOpenTitle) {
                this.onlyOpenTitle = options.onlyOpenTitle;
            }
            if (options.openTabs) {
                this.openTabs = options.openTabs;
            }
            if (options.homeTabId) {
                this.homeTabId = options.homeTabId;
            }
            if (options.homeUrl) {
                this.homeUrl = options.homeUrl;
            } else if (options.homeUrl === null) {
                this.homeUrl = '';
            }

            this.ensureContainers();
            this.ensureHomeTab();
            this.bindTabEvents();
            this.bindGlobalActions();
        },

        ensureContainers: function () {
            var $ = this.modules.$;
            if (!$) { return; }
            var $tabs = $('#mainTabs');
            if (!$tabs.length) { return; }
            if (!$tabs.children('.layui-tab-title').length) {
                $tabs.append('<ul class="layui-tab-title"></ul><div class="layui-tab-content"></div>');
            }
        },

        ensureHomeTab: function () {
            var $ = this.modules.$;
            var element = this.modules.element;
            if (!$ || !element) { return; }
            var $tabs = $('#mainTabs');
            if (!$tabs.length) { return; }

            var selector = '.layui-tab-title li[lay-id="' + this.homeTabId + '"]';
            if (!$tabs.find(selector).length) {
                element.tabAdd(this.tabFilter, {
                    title: this.buildTabTitle(this.onlyOpenTitle, 'layui-icon layui-icon-home'),
                    id: this.homeTabId,
                    content: this.homeUrl ? this.createFrame(this.homeUrl) : ''
                });
            }
            this.setHomeTabState();
            element.tabChange(this.tabFilter, this.homeTabId);
        },

        setHomeTabState: function () {
            var $ = this.modules.$;
            if (!$) { return; }
            var $tabs = $('#mainTabs');
            var $home = $tabs.find('.layui-tab-title li[lay-id="' + this.homeTabId + '"]');
            if (!$home.length) { return; }
            $home.attr('lay-allowclose', 'false').addClass('tab-home');
            $home.find('.layui-tab-close').remove();
        },

        getTabId: function (title) {
            return encodeURIComponent(title || 'tab');
        },

        buildTabTitle: function (title, iconCls) {
            var iconHtml = '';
            if (iconCls) {
                if (iconCls.indexOf('layui-icon') === 0 && iconCls.indexOf(' ') === -1) {
                    iconHtml = '<i class="layui-icon ' + this.escapeHtml(iconCls) + '"></i>';
                } else {
                    iconHtml = '<i class="' + this.escapeHtml(iconCls) + '"></i>';
                }
            }
            return '<span class="tab-label">' + iconHtml + '<cite>' + this.escapeHtml(title || '') + '</cite></span>';
        },

        escapeHtml: function (text) {
            return String(text || '')
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        },

        createFrame: function (url) {
            return '<iframe class="main-iframe" scrolling="auto" frameborder="0" src="' + (url || '') + '"></iframe>';
        },

        addTab: function (title, url, icon) {
            var $ = this.modules.$;
            var element = this.modules.element;
            var layer = this.modules.layer;
            if (!$ || !element) { return; }
            var $tabs = $('#mainTabs');
            if (!$tabs.length) {
                if (url) {
                    global.location.href = url;
                }
                return;
            }

            var targetUrl = url && url !== '#' ? url : '/error/error404';
            var tabId = this.getTabId(title);
            var $existing = $tabs.find('.layui-tab-title li[lay-id="' + tabId + '"]');
            var closableCount = $tabs.find('.layui-tab-title li').not('[lay-id="' + this.homeTabId + '"]').length;
            var self = this;

            var add = function () {
                if (!$existing.length) {
                    element.tabAdd(self.tabFilter, {
                        title: self.buildTabTitle(title, icon),
                        id: tabId,
                        content: self.createFrame(targetUrl)
                    });
                } else {
                    self.refreshTabContentById(tabId, targetUrl, false);
                }
                element.tabChange(self.tabFilter, tabId);
            };

            if (!$existing.length && closableCount >= this.openTabs) {
                if (layer) {
                    layer.confirm('<b>打开页面过多，可能会影响程序的展现效率，继续打开？</b>', { icon: 3, title: '系统提示' }, function (index) {
                        add();
                        layer.close(index);
                    });
                } else {
                    add();
                }
            } else {
                add();
            }
        },

        refreshTabContentById: function (tabId, url, force) {
            var $ = this.modules.$;
            if (!$) { return; }
            var $tabs = $('#mainTabs');
            var $title = $tabs.find('.layui-tab-title li[lay-id="' + tabId + '"]');
            if (!$title.length) { return; }
            var index = $title.index();
            var $content = $tabs.find('.layui-tab-content .layui-tab-item').eq(index);
            var $iframe = $content.find('iframe');
            if (!$iframe.length) { return; }
            if (force) {
                $iframe[0].contentWindow.location.reload(true);
                return;
            }
            if (url && $iframe.attr('src') !== url) {
                $iframe.attr('src', url);
            }
        },

        bindTabEvents: function () {
            var $ = this.modules.$;
            var element = this.modules.element;
            if (!$ || !element) { return; }
            var self = this;
            var $tabs = $('#mainTabs');
            if (!$tabs.length) { return; }

            var $menu = $(this.contextMenuSelector);
            $tabs.on('dblclick', '.layui-tab-title li', function () {
                var layId = $(this).attr('lay-id');
                if (layId === self.homeTabId) { return; }
                self.closeTab('close', layId);
            });

            $tabs.on('contextmenu', '.layui-tab-title li', function (evt) {
                var layId = $(this).attr('lay-id');
                if (layId === self.homeTabId) { return; }
                evt.preventDefault();
                element.tabChange(self.tabFilter, layId);
                if ($menu.length) {
                    $menu.css({ left: evt.pageX, top: evt.pageY }).addClass('layui-anim layui-anim-upbit').show();
                }
            });

            $(document).on('click', function () {
                if ($menu.length) {
                    $menu.hide();
                }
            });

            if ($menu.length) {
                $menu.on('click', '[data-action]', function (evt) {
                    var action = $(this).data('action');
                    self.closeTab(action);
                    $menu.hide();
                    evt.stopPropagation();
                });
            }
        },

        bindGlobalActions: function () {
            var $ = this.modules.$;
            var layer = this.modules.layer;
            var self = this;
            if (!$) { return; }

            $('#loginOut').on('click', function () {
                if (!layer) {
                    global.location.href = '/Admin/Index/';
                    return;
                }
                layer.confirm('您确定要退出本次登录吗?', { icon: 3, title: '系统提示' }, function (index) {
                    layer.close(index);
                    setTimeout(function () {
                        if ($.ajaxjson) {
                            $.ajaxjson('/Admin/OutLogin/', {}, function () {
                                global.location.href = '/Admin/Index/';
                            });
                        } else {
                            global.location.href = '/Admin/Index/';
                        }
                    }, 200);
                });
            });

            $('#editPass').on('click', function () {
                self.openPasswordDialog();
            });

            $(global).on('load', function () {
                $('#loading').fadeOut();
            });
        },

        openPasswordDialog: function () {
            var $ = this.modules.$;
            var layer = this.modules.layer;
            var form = this.modules.form;
            if (!layer || !$) { return; }

            var loginName = $('#curname').text() || '';
            var content = [
                '<form class="layui-form layui-form-pane password-form" lay-filter="passwordForm" style="padding: 12px 24px 4px;">',
                '  <div class="layui-form-item">',
                '    <label class="layui-form-label">登录名</label>',
                '    <div class="layui-input-block">',
                '      <input type="text" class="layui-input" value="' + this.escapeHtml(loginName) + '" readonly />',
                '    </div>',
                '  </div>',
                '  <div class="layui-form-item">',
                '    <label class="layui-form-label">原密码</label>',
                '    <div class="layui-input-block">',
                '      <input type="password" name="oldPassword" lay-verify="required" required placeholder="请输入原密码" autocomplete="off" class="layui-input" />',
                '    </div>',
                '  </div>',
                '  <div class="layui-form-item">',
                '    <label class="layui-form-label">新密码</label>',
                '    <div class="layui-input-block">',
                '      <input type="password" name="newPassword" lay-verify="required|passlen" required placeholder="请输入新密码" autocomplete="off" class="layui-input" />',
                '    </div>',
                '  </div>',
                '</form>'
            ].join('');

            if (form && form.verify) {
                form.verify({
                    passlen: function (value) {
                        if (value && value.length < 6) {
                            return '密码长度不能小于6位';
                        }
                    }
                });
            }

            var dialogIndex = layer.open({
                type: 1,
                title: '修改密码',
                area: '360px',
                shadeClose: true,
                content: content,
                btn: ['保存', '取消'],
                success: function () {
                    if (form && form.render) {
                        form.render();
                    }
                },
                yes: function () {
                    var $form = $('.password-form');
                    var oldPassword = $.trim($form.find('input[name="oldPassword"]').val());
                    var newPassword = $.trim($form.find('input[name="newPassword"]').val());
                    if (!oldPassword || !newPassword) {
                        layer.msg('请完整填写密码信息', { icon: 0 });
                        return;
                    }
                    if (newPassword.length < 6) {
                        layer.msg('新密码长度不能小于6位', { icon: 0 });
                        return;
                    }
                    layer.close(dialogIndex);
                    this.submitPasswordChange(oldPassword, newPassword);
                }.bind(this)
            });
        },

        submitPasswordChange: function (oldPassword, newPassword) {
            var $ = this.modules.$;
            var layer = this.modules.layer;
            var self = this;
            if (!$) { return; }

            $.ajax({
                type: 'POST',
                url: '/Login/ChangePassword',
                data: {
                    newPassword: newPassword,
                    oldPassword: oldPassword
                },
                dataType: 'json',
                headers: (typeof $.cookie === 'function') ? { 'X_CSRFToken': $.cookie('csrftoken') } : {},
                beforeSend: function () {
                    if (layer) {
                        self.loadingIndex = layer.load(2);
                    }
                },
                complete: function () {
                    if (layer && self.loadingIndex !== null) {
                        layer.close(self.loadingIndex);
                        self.loadingIndex = null;
                    }
                },
                success: function (msg) {
                    if (msg && msg.Data > 0) {
                        layer.msg('成功修改登录密码，请重新登录！', { icon: 1 });
                        setTimeout(function () {
                            if ($.ajaxjson) {
                                $.ajaxjson('/Login/OutLogin', {}, function () {
                                    top.location.href = '../Login/Index';
                                });
                            } else {
                                top.location.href = '../Login/Index';
                            }
                        }, 200);
                    } else {
                        var message = (msg && msg.Message) ? msg.Message : '密码修改失败，请稍后重试。';
                        layer.alert(message, { icon: 5, title: '温馨提示' });
                    }
                },
                error: function () {
                    if (layer) {
                        layer.alert('密码修改请求失败，请稍后重试。', { icon: 5, title: '温馨提示' });
                    }
                }
            });
        },

        closeTab: function (action, targetId) {
            var $ = this.modules.$;
            var element = this.modules.element;
            if (!$ || !element) { return; }
            var $tabs = $('#mainTabs');
            if (!$tabs.length) { return; }
            var $titles = $tabs.find('.layui-tab-title li');
            var $current = targetId ? $titles.filter('[lay-id="' + targetId + '"]') : $titles.filter('.layui-this');
            if (!$current.length) { return; }

            var currentId = $current.attr('lay-id');
            var currentIndex = $current.index();
            var self = this;

            switch (action) {
                case 'refresh':
                    this.refreshTabByIndex(currentIndex);
                    break;
                case 'close':
                    if (currentId !== this.homeTabId) {
                        element.tabDelete(this.tabFilter, currentId);
                    }
                    break;
                case 'closeall':
                    $titles.each(function () {
                        var id = $(this).attr('lay-id');
                        if (id !== self.homeTabId) {
                            element.tabDelete(self.tabFilter, id);
                        }
                    });
                    element.tabChange(this.tabFilter, this.homeTabId);
                    break;
                case 'closeother':
                    $titles.each(function () {
                        var id = $(this).attr('lay-id');
                        if (id !== self.homeTabId && id !== currentId) {
                            element.tabDelete(self.tabFilter, id);
                        }
                    });
                    element.tabChange(this.tabFilter, currentId);
                    break;
                case 'closeright':
                    $titles.each(function () {
                        var index = $(this).index();
                        var id = $(this).attr('lay-id');
                        if (index > currentIndex && id !== self.homeTabId) {
                            element.tabDelete(self.tabFilter, id);
                        }
                    });
                    break;
                case 'closeleft':
                    $titles.each(function () {
                        var index = $(this).index();
                        var id = $(this).attr('lay-id');
                        if (index < currentIndex && id !== self.homeTabId) {
                            element.tabDelete(self.tabFilter, id);
                        }
                    });
                    break;
                case 'exit':
                    $(this.contextMenuSelector).hide();
                    break;
            }
        },

        refreshTabByIndex: function (index) {
            var $ = this.modules.$;
            if (!$) { return; }
            var $iframe = $('#mainTabs .layui-tab-content .layui-tab-item').eq(index).find('iframe');
            if ($iframe.length) {
                var src = $iframe.attr('src');
                $iframe.attr('src', src);
            }
        }
    };

    global.HPWFIndex = HPWFIndex;
})(window);
