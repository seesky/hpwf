function ExportExcel(gridid, useField) {
    this.grid = $('#' + gridid);
    if (useField) {
        this.fields = JSON.parse(useField);
    }
}

ExportExcel.prototype = {
    /**
	 * go() export datagrid data.
	 *
	 * @param <String> tableName
	 * @param <String> sortField
	 * @return 
	 */
    go: function (tableName, sortField) {
        var hDialog = top.$.hDialog({
            iconCls: 'icon16_table_export',
            content: '<p><b>请选择要导出的字段：</b>&nbsp;&nbsp;&nbsp;&nbsp;<input style="vertical-align:middle" type="checkbox" checked id="__check_all" /><label style="vertical-align:middle" for="__check_all">全选</label></p><ul class="checkbox" id="field_list"></ul>', width: 430, height: 320, title: '导出Excel数据',
            submit: function () {
                var selectedFields = '';
                top.$('#field_list :checked').each(function () {
                    var v = $(this).val();
                    //selectedFields += v.split('|')[0] + ' as  ' + v.split('|')[1] + ","; //暂时取消用户自定义标题的显示，调用分页会有问题。
                    selectedFields += v.split('|')[0] + ",";
                });
                if (selectedFields != '')
                    selectedFields = selectedFields.substr(0, selectedFields.length - 1);
                else
                    selectedFields = " * ";
                var where = $('body').data('where');
                if (!where)
                    where = "";
                window.open('/Admin/FrameworkModules/Utility/ExportExcel?tableName=' + tableName + '&sortField=' + sortField + '&fields=' + selectedFields + '&filters=' + where);
            }
        });

        //[{ 'title': 'id', 'field': 'ID',hidden:true,width=60 }, { 'title': '模块名称', 'field': 'FULLNAME',width:200 }];
        var lis = '';

        if (this.fields) {  //物理指定导出列
            $.each(this.fields, function (i, n) {
                lis += '<li><input type="checkbox" checked style="vertical-align:middle" value="' + n.field + '|' + n.title + '" id="' + n.title + '"  ><label style="vertical-align:middle" for="' + n.field + '">' + n.title + '</label></li>';
            });
        } else {   //根据DataGrid动态生成导出列
            //自动处理了多表头、冻结列、隐藏列等情况。
            var columns = this.grid.datagrid('options').columns[0];
            var columns1 = this.grid.datagrid('options').columns[1];
            var frozeCol = this.grid.datagrid('options').frozenColumns[0];

            if (frozeCol) {
                $.each(frozeCol, function () {
                    if (this.title && !this.hidden) {
                        lis += '<li><input type="checkbox" checked style="vertical-align:middle" value="' + this.field + '|' + this.title + '" id="' + this.title + '"  ><label style="vertical-align:middle" for="' + this.field + '">' + this.title + '</label></li>';
                    }
                });
            }

            $.each(columns, function () {
                if (this.field && this.title && !this.hidden) {
                    lis += '<li><input type="checkbox" checked style="vertical-align:middle" value="' + this.field + '|' + this.title + '" id="' + this.title + '"  ><label style="vertical-align:middle" for="' + this.field + '">' + this.title + '</label></li>';
                }
            });

            if (columns1) {
                $.each(columns1, function () {
                    if (this.field && this.title && !this.hidden) {
                        lis += '<li><input type="checkbox" checked style="vertical-align:middle" value="' + this.field + '|' + this.title + '" id="' + this.title + '"  ><label style="vertical-align:middle" for="' + this.field + '">' + this.title + '</label></li>';
                    }
                });
            }
        }
        top.$('#field_list').empty().append(lis);
        top.$('#__check_all').click(function () {
            var flag = $(this).is(":checked");
            top.$('#field_list :checkbox').attr('checked', flag);
        });
    }
};