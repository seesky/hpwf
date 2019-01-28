//操作符
var arr_op = [{ "txt": "等于", "val": "eq" },
                { "txt": "不等于", "val": "ne" },
                { "txt": "大于", "val": "gt" },
                { "txt": "大于等于", "val": "ge" },
                { "txt": "小于", "val": "lt" },
                { "txt": "小于等于", "val": "le" },
                { "txt": "包含", "val": "cn" },
                { "txt": "以xx开始", "val": "bw" },
                { "txt": "以xx结束", "val": "ew" }];

var rule = '<tr>\
                <td class="filter-first-td"></td>\
                <td class="columns"><select class="fields"></select></td>\
                <td class="operators"><select class="selectopts"></select></td>\
                <td class="data"><input type="text" style="width: 98%; "  class="input-data"/></td>\
                <td><input type="button" class="del-rule" value="-" title="删除条件"/></td>\
            </tr>';

var group = '<tr><td class="filter-first-td"></td><td colspan="4"><table width="98%" class="group" style="border:0px none;"><tr><th colspan="5" align="left"><select class="opsel"><option value="AND" selected="selected">And</option><option value="OR">Or</option></select><input type="button" value="+ {}" title="Add subgroup" class="add-group"><input type="button" value="+" title="Add rule" class="add-rule ui-add"><input type="button" value="-" title="Delete group" class="del-group"></th></tr></table></td></tr>';

var gridid = '';
var search = {
    go: function (gridId) {
        gridid = gridId;
        var sDialog = top.$.hDialog({
            href: '/Admin/FrameworkModules/Utility/Search/?n=' + Math.random(),
            title: '高级查询', iconCls: 'icon16_molecule', width: 500, height: 400,
            cache: false, closable: true,
            toolbar: [
                {
                    text: '查看条件', iconCls: 'icon16_sql', handler: function () {
                        top.$.hDialog({
                            iconCls: 'icon16_sql',
                            content: '<div style="padding:10px; font-family:consolas; font-size:14px; line-height:20px;">' + search.toSqlWhere() + '</div>',
                            width: 400, height: 300, showbtn: false, cache: false, title: '条件 SQL 语句 ', modal: false
                        });
                    }
                },
                {
                    text: '条件重置', iconCls: 'icon16_picasa', handler: function () {
                        sDialog.dialog('refresh');
                    }
                }
            ],
            onLoad: function () {
                top.$('.add-group').die().live('click', function () {
                    search.addGroup(this);
                });

                top.$('.del-group').die().live('click', function () {
                    search.delGroup(this);
                });

                top.$('.add-rule').die().live('click', function () {
                    search.addRule(this);
                }).click();

                top.$('.del-rule').die().live('click', function () {
                    search.delRule(this);
                });
            }, submit: function () {
                var _filter = search.buildFilterObj();
                if (_filter && _filter.rules.length === 1 && _filter.rules[0].data === '') {
                    $('#' + gridid).datagrid('reload', { filter: '' });
                } else {
                    if (search.toSqlWhere(_filter) == '')
                        $('#' + gridid).datagrid('reload', { filter: '' });
                    else
                        $('#' + gridid).datagrid('reload', { filter: JSON.stringify(_filter) });
                }
            }
        });
    },
    initFields: function (sel) {
        var columns = $('#' + gridid).datagrid('options').columns[0];
        var columns1 = $('#' + gridid).datagrid('options').columns[1];
        var frozeCol = $('#' + gridid).datagrid('options').frozenColumns[0];
        var $obj = top.$('#filterForm .fields');
        if (sel)
            $obj = top.$(sel);
        $obj.empty();
        
        if (frozeCol) {
            $.each(frozeCol, function () {
                if (this.title && !this.hidden) {
                    $obj.append('<option value="' + this.field + '">' + this.title + '</option>');
                }
            });
        }
        
        $.each(columns, function () {
            if (this.field && this.title && !this.hidden) {
                $obj.append('<option value="' + this.field + '">' + this.title + '</option>');
            }   
        });

        if (columns1) {
            $.each(columns1, function () {
                if (this.field && this.title && !this.hidden) {
                    $obj.append('<option value="' + this.field + '">' + this.title + '</option>');
                }
            });
        }
        
        //Enumerable.from(columns).select('<option value="$.field">$.title</option>')
    },
    initOp: function (sel) {
        var $obj = top.$('#filterForm .selectopts');
        if (sel)
            $obj = top.$(sel);
        $obj.empty();
        $.each(arr_op, function () {
            $obj.append('<option value="' + this.val + '">' + this.txt + '</option>');
        });
    },
    addRule: function (obj) {
        var $brouther = top.$(obj).parent().parent().siblings();
        var $last = $brouther.length > 0 ? $brouther.last() : top.$(obj).parent().parent();
        var $tr = $(rule).insertAfter($last);
        var $ddl = $('>td select', $tr);

        search.initFields($ddl.filter('.fields')[0]);
        search.initOp($ddl.filter('.selectopts')[0]);
    },
    delRule: function (btndel) {
        $(btndel).parent().parent().remove();
    },
    addGroup: function (obj) {
        var $brouther = top.$(obj).parent().parent().siblings();
        var $last = $brouther.length > 0 ? $brouther.last() : top.$(obj).parent().parent();
        $last.after(group);
        search.setGroupBgcolor();
    },
    delGroup: function (btn) {
        top.$(btn).closest('table.group').parent().parent().remove();
        search.setGroupBgcolor();
    },
    setGroupBgcolor: function () {
        top.$('table.group').each(function (i) {
            if (i % 2 == 0)
                $(this).css({ 'background-color': '#FCCEF7' });
            else
                $(this).css({ 'background-color': '#B2FF95' });
        });
    },
    buildFilterObj: function () {
        var buildFilterGroup = function (gtb) {
            var $groupOP = top.$(gtb).find('.opsel').first();
            var $ruleArr = $groupOP.parent().parent().nextAll();
            var _filter = {};
            _filter.groupOp = $groupOP.val();
            _filter.rules = [];
            _filter.groups = [];
            $.each($ruleArr, function (i, n) {
                var $tds = $('>td', $(n));
                if ($tds.length > 2) {
                    var _rule = {};
                    _rule.field = $tds.find('.fields').val();
                    _rule.op = $tds.find('.selectopts').val();
                    _rule.data = $tds.find('.input-data').val();

                    _filter.rules.push(_rule);
                }

                var groupTable = $(n).find('table.group');
                if (groupTable.length > 0)
                    _filter.groups.push(buildFilterGroup(groupTable));

            });
            return _filter;
        };
        var filterGroup;
        filterGroup = buildFilterGroup(top.$('.filter'));

        return filterGroup;
    },
    toSqlWhere: function () {
        var filterObj = search.buildFilterObj();

        var filter2sql = function (filter) {
            if (filter.rules.length == 0 && filter.groups.length == 0)
                return "";


            var _sqlWhere = '(';
            var flag = false;
            if (filter.rules.length > 0) {
                $.each(filter.rules, function (i, n) {
                    if (flag)
                        _sqlWhere += ' ' + filter.groupOp + ' ';
                    _sqlWhere += ruleFormatter(n);
                    flag = true;
                });
            }

            if (filter.groups.length > 0) {
                $.each(filter.groups, function (i, n) {
                    if (flag)
                        _sqlWhere += ' ' + filter.groupOp + ' ';
                    _sqlWhere += filter2sql(n);
                    flag = true;
                });
            }

            _sqlWhere += ')';
            return _sqlWhere;
        };
        var op2word = function (op) {
            switch (op) {
                case "eq": return " = ";
                case "gt": return " > ";
                case "ge": return " >= ";
                case "nu": return " IS NULL ";
                case "nn": return " IS NOT NULL ";
                case "lt": return " < ";
                case "le": return " <= ";
                case "cn": return " like ";
                case "bw": return " like ";
                case "ew": return " like ";
                case "ne": return " <> ";
                case "in": return " IN ";
                case "ni": return " NOT IN ";
                default: return " = ";
            }
        };
        var ruleFormatter = function (rule) {
            var result = '';
            if (rule) {
                var _op = op2word(rule.op);
                switch (rule.op) {
                    case "bw":
                        result = rule.field + _op + "'" + rule.data + "%'";
                        break;
                    case "ew":
                        result = rule.field + _op + "'%" + rule.data + "'";
                        break;
                    case "cn":
                    case "nc":
                        result = rule.field + _op + "'%" + rule.data + "%'";
                        break;
                    case "in":
                    case "ni":
                        result = rule.field + _op + "(" + rule.data + ")";
                        break;
                    case "nu":
                    case "nn":
                        result = (rule.field + _op);
                        break;
                    default:
                        result = rule.field + _op + "'" + rule.data + "'";
                        break;
                }
                return result;
            }
            else
                return "";
        };
        return filter2sql(filterObj);
    }
};