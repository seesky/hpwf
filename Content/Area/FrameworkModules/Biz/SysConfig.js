//系统全局设置
var _data = {
    theme: [
        { "title": "默认皮肤", "name": "default" },
        { "title": "流行灰", "name": "gray" },        
        { "title": "黑色", "name": "black" },
        { "title": "bootstrap", "name": "bootstrap" },
        { "title": "metro", "name": "metro" },
        { "title": "metro-blue", "name": "metro-blue" },
        { "title": "metro-gray", "name": "metro-gray" },
        { "title": "metro-green", "name": "metro-green" },
        { "title": "metro-orange", "name": "metro-orange" },
        { "title": "metro-red", "name": "metro-red" },
        { "title": "ui-cupertino", "name": "ui-cupertino" },
        { "title": "ui-dark-hive", "name": "ui-dark-hive" },
        { "title": "ui-pepper-grinder", "name": "ui-pepper-grinder" },
        { "title": "ui-sunny", "name": "ui-sunny" }
    ],
    navType: [{ "id": "AccordionTree", "text": "手风琴+树形目录(2级+)", "selected": true }
            , { "id": "Tree", "text": "树形结构" }
            , { "id": "Accordion", "text": "手风琴形式（2级）" }]
};

function initCtrl() {
    $('#txtTheme').combobox({
        data: _data.theme, panelHeight: 'auto', editable: false, valueField: 'name', textField: 'title'
    });
    $('#txtNavShowType').combobox({
        data: _data.navType, panelHeight: 'auto', editable: false, valueField: 'id', textField: 'text', width: 180
    });
    $('#txtGridRows').val(20).numberspinner({ min: 10, max: 500, increment: 10 });
    $.ajaxjson('/Admin/FrameworkModules/SysConfig/GetDefaultConfig/', '', function (d) {
        if (d) {
            $('#txtTheme').combobox('setValue', d.theme.name);
            $('#txtGridRows').numberspinner('setValue', d.gridRows);
            $('#txtNavShowType').combobox('setValue', d.navType);
        }
    });
}

$(function () {
    initCtrl();
    $('#btnok').click(saveConfig);
    $('body').css('overflow', 'auto');
});

function saveConfig() {
    var theme = $('#txtTheme').combobox('getValue');
    var gridrows = $('#txtGridRows').numberspinner('getValue');
    var navtype = $('#txtNavShowType').combobox('getValue');

    var findThemeObj = function () {
        var obj = null;
        $.each(_data.theme, function (i, n) {
            if (n.name == theme)
                obj = n;
        });
        return obj;
    };
    var configObj = { theme: findThemeObj(), navType: navtype, gridRows: gridrows };

    var str = JSON.stringify(configObj);

    $.ajaxtext('/Admin/FrameworkModules/SysConfig/UpdateUserConfig/', 'themeJson=' + str, function (d) {
        if (d == 1)
            msg.ok('恭喜，全局设置保存成功,按F5看效果');
        else
            alert(d);
    });
}