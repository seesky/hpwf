

//得到select项的个数
jQuery.fn.selectCount = function() {
    return jQuery(this).get(0).options.length;
}
//获得选中项的索引
jQuery.fn.getSelectedIndex = function() {
    return jQuery(this).get(0).selectedIndex;
}
//获得当前选中项的文本
jQuery.fn.getSelectedText = function() {
    if (this.selectCount() == 0) {
        return "下拉框中无选项";
    }
    else {
        var index = this.getSelectedIndex();
        return jQuery(this).get(0).options[index].text;
    }
}
//获得当前选中项的值
jQuery.fn.getSelectedValue = function() {
    if (this.selectCount() == 0) {
        return "下拉框中无选中值";
    }
    else {
        return jQuery(this).val();
    }
}
//设置select中值为value的项为选中
jQuery.fn.setSelectedValue = function (value) {
    jQuery(this).get(0).value = value;
    return jQuery(this);
}
//设置select中文本为text的第一项被选中
jQuery.fn.setSelectedText = function(text) {
    var isExist = false;
    var count = this.selectCount();
    for (var i = 0; i < count; i++) {
        if (jQuery(this).get(0).options[i].text == text) {
            jQuery(this).get(0).options[i].selected = true;
            isExist = true;
            break;
        }
    }
    if (!isExist) {
        alert("下拉框中不存在该项");
    }
}
//设置选中指定索引项
jQuery.fn.setSelectedIndex = function(index) {
    var count = this.selectCount();
    if (index >= count || index < 0) {
        alert("选中项索引超出范围");
    }
    else {
        jQuery(this).get(0).selectedIndex = index;
    }
}
//判断select项中是否存在值为value的项
jQuery.fn.isExistItem = function(value) {
    var isExist = false;
    var count = this.selectCount();
    for (var i = 0; i < count; i++) {
        if (jQuery(this).get(0).options[i].value == value) {
            isExist = true;
            break;
        }
    }
    return isExist;
}

//获取所有选项的VALUE,并返回数据ARRAY
jQuery.fn.getAllOptions = function () {
    var arr = new Array();
    var count = this.selectCount();
    for (var i = 0; i < count; i++) {
        arr.push(jQuery(this).get(0).options[i].value);
    }
    return arr;
}

//向select中添加一项，显示内容为text，值为value,如果该项值已存在，则提示
jQuery.fn.addOption = function (text, value) {
    if (this.isExistItem(value)) {
        alert(text + " 已存在!");
        return false;
    }
    else {
        jQuery(this).get(0).options.add(new Option(text, value));
    }
}

jQuery.fn.addOptionTitle = function(text, value, title) {
    if (this.isExistItem(value)) {
        alert("待添加项的值已存在");
    }
    else {
        var newOption = new Option(text, value);
        $(newOption).attr("title", title);
        jQuery(this).get(0).options.add(newOption);
    }
}
//向select中添加一项，则提示
jQuery.fn.addOptions = function(option) {
    var o = $(option);
    jQuery(this).addOptionTitle(o.attr("text"), o.attr("value"), o.attr("title"));
}

//删除select中值为value的项，如果该项不存在，则提示
jQuery.fn.removeItem = function(value) {
    if (this.isExistItem(value)) {
        var count = this.selectCount();
        for (var i = 0; i < count; i++) {
            if (jQuery(this).get(0).options[i].value == value) {
                jQuery(this).get(0).remove(i);
                break;
            }
        }
    }
    else {
        alert("待删除的项不存在!");
    }
}
//删除select中指定索引的项
jQuery.fn.removeIndex = function(index) {
    var count = this.selectCount();
    if (index >= count || index < 0) {
        alert("待删除项索引超出范围");
    }
    else {
        jQuery(this).get(0).remove(index);
    }
}
//删除select中选定的项
jQuery.fn.removeSelected = function() {
    var index = this.getSelectedIndex();
    this.removeIndex(index);
}
//清除select中的所有项
jQuery.fn.clearAll = function() {
    jQuery(this).get(0).options.length = 0;
}
