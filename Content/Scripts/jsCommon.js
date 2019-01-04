/***Jquery扩展&JavaScript 通用工具类 2013-05-28***/

//使用说明：所有扩展的方法都使用to开头
//1、Object.toXXX   Object为JavaScript自身的Object,每个方法都有中文提示
//2、Date扩展，包括Date的实例对象扩展 如var date=new Date();  Date.toXXXX(),  date.toXXX();
//3、String扩展，包括String实例对象如 var a="aaaa"; a.toXXXX;
//4、Number 数字 扩展，也是toXXX的用法
//5、Function 函数对象 扩展 也是toXXX的用法

/*********************Base*********************/

(function () {
    //闭包环境，防止变量冲突，任何变量在外部不可用
    var _toString = Object.prototype.toString,
       NULL_TYPE = 'Null',
       UNDEFINED_TYPE = 'Undefined',
       BOOLEAN_TYPE = 'Boolean',
       NUMBER_TYPE = 'Number',
       STRING_TYPE = 'String',
       OBJECT_TYPE = 'Object',
       FUNCTION_CLASS = '[object Function]',
       BOOLEAN_CLASS = '[object Boolean]',
       NUMBER_CLASS = '[object Number]',
       STRING_CLASS = '[object String]',
       ARRAY_CLASS = '[object Array]',
       DATE_CLASS = '[object Date]',
       NATIVE_JSON_STRINGIFY_SUPPORT = window.JSON &&
         typeof JSON.stringify === 'function' &&
         JSON.stringify(0) === '0';


    // 一个静态方法表示继承, 目标对象将拥有源对象的所有属性和方法
    Object.extend = function (destination, source) {
        for (var property in source) {
            destination[property] = source[property];   // 利用动态语言的特性, 通过赋值动态添加属性与方法
        }
        return destination;   // 返回扩展后的对象
    };
    Object.extend(Object, {
        // 一个静态方法, 传入一个对象, 返回对象的字符串表示
        toInspect: function (object) {
            try {
                if (object == undefined) return 'undefined'; // 处理undefined情况
                if (object == null) return 'null';     // 处理null情况
                // 如果对象定义了inspect方法, 则调用该方法返回, 否则返回对象的toString()值
                return object.inspect ? object.inspect() : object.toString();
            } catch (e) {
                if (e instanceof RangeError) return '...'; // 处理异常情况
                throw e;
            }
        },
        // 一个静态方法, 传入一个对象, 返回该对象中所有的属性, 构成数组返回
        toKeys: function (object) {
            var keys = [];
            for (var property in object)
                keys.push(property);     // 将每个属性压入到一个数组中
            return keys;
        },
        // 一个静态方法, 传入一个对象, 返回该对象中所有属性所对应的值, 构成数组返回
        toValues: function (object) {
            var values = [];
            // 将每个属性的值压入到一个数组中
            for (var property in object) values.push(object[property]);
            return values;
        },
        // 一个静态方法, 传入一个对象, 克隆一个新对象并返回
        toClone: function (object) {
            return Object.extend({}, object);
        }

    });

    //判断类型
    function Type(o) {
        switch (o) {
            case null: return NULL_TYPE;
            case (void 0): return UNDEFINED_TYPE;
        }
        var type = typeof o;
        switch (type) {
            case 'boolean': return BOOLEAN_TYPE;
            case 'number': return NUMBER_TYPE;
            case 'string': return STRING_TYPE;
        }
        return OBJECT_TYPE;
    }

    //克隆数组
    //hasObjcet,数组是否存在对象
    function cloneArray(array, hasObjcet) {
        var newArray = [];
        if (array) {
            if (hasObjcet == true) {
                for (var i = 0, len = array.length; i < len; i++) {
                    if (typeof (array[i]) == "object") {
                        newArray.push(cloneObjcet(array[i]));
                    } else {
                        newArray.push(array[i]);
                    }
                }
            } else {
                newArray = null;
            }
        }
        return newArray;
    }

    //是否为对象元素
    function isElement(object) {
        return !!(object && object.nodeType == 1);
    }

    //是否为数组
    function isArray(object) {
        return _toString.call(object) === ARRAY_CLASS;
    }

    var hasNativeIsArray = (typeof Array.isArray == 'function')
      && Array.isArray([]) && !Array.isArray({});

    if (hasNativeIsArray) {
        isArray = Array.isArray;
    }
    //格式化为Html
    function toHTML(object) {
        return object && object.toHTML ? object.toHTML() : String.interpret(object);
    }
    function isHash(object) {
        return object instanceof Hash;
    }

    //是否为函数类型
    function isFunction(object) {
        return _toString.call(object) === FUNCTION_CLASS;
    }
    //是否为字符串类型
    function isString(object) {
        return _toString.call(object) === STRING_CLASS;
    }

    //是否为数字类型
    function isNumber(object) {
        return _toString.call(object) === NUMBER_CLASS;
    }
    //是否为日期类型
    function isDate(object) {
        return _toString.call(object) === DATE_CLASS;
    }
    //是否为日期类型的字符串
    function isDateStr(dateStr) {
        var r = /^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2})/.test(dateStr);
        return r;
    }
    //是否为Undefined
    function isUndefined(object) {
        return typeof object === "undefined";
    }


    //转换为Json对象
    function toJSON(value) {
        return Str('', { '': value }, []);
    }

    function stringify(object) {
        return JSON.stringify(object);
    }
    function stringToJson(str) {
        return eval('(' + str + ')');
    }


    function inspect(object) {
        try {
            if (isUndefined(object)) return 'undefined';
            if (object === null) return 'null';
            return object.inspect ? object.inspect() : String(object);
        } catch (e) {
            if (e instanceof RangeError) return '...';
            throw e;
        }
    }

    function Str(key, holder, stack) {
        var value = holder[key],
            type = typeof value;

        if (Type(value) === OBJECT_TYPE && typeof value.toJSON === 'function') {
            value = value.toJSON(key);
        }

        var _class = _toString.call(value);

        switch (_class) {
            case NUMBER_CLASS:
            case BOOLEAN_CLASS:
            case STRING_CLASS:
                value = value.valueOf();
        }

        switch (value) {
            case null: return 'null';
            case true: return 'true';
            case false: return 'false';
        }

        type = typeof value;
        switch (type) {
            case 'string':
                return value.inspect(true);
            case 'number':
                return isFinite(value) ? String(value) : 'null';
            case 'object':

                for (var i = 0, length = stack.length; i < length; i++) {
                    if (stack[i] === value) { throw new TypeError(); }
                }
                stack.push(value);

                var partial = [];
                if (_class === ARRAY_CLASS) {
                    for (var i = 0, length = value.length; i < length; i++) {
                        var str = Str(i, value, stack);
                        partial.push(typeof str === 'undefined' ? 'null' : str);
                    }
                    partial = '[' + partial.join(',') + ']';
                } else {
                    var keys = Object.keys(value);
                    for (var i = 0, length = keys.length; i < length; i++) {
                        var key = keys[i], str = Str(key, value, stack);
                        if (typeof str !== "undefined") {
                            partial.push(key.inspect(true) + ':' + str);
                        }
                    }
                    partial = '{' + partial.join(',') + '}';
                }
                stack.pop();
                return partial;
        }
    }

    function getFunctionName(obj) {
        if (typeof obj != "function" || obj === null)
            return null;
        else
            return /\s([^(]+)/.exec(obj.toString())[1];
    }
    Object.extend(Object, {
        toType: Type,
        toHTML: toHTML,
        toIsElement: isElement,
        toIsArray: isArray,
        toIsHash: isHash,
        toIsFunction: isFunction,
        toIsString: isString,
        toIsNumber: isNumber,
        toIsDate: isDate,
        toIsDateStr: isDateStr,
        toIsUndefined: isUndefined,
        toStringToJson: stringToJson,
        toCloneArray: cloneArray,
        toGetFunctionName:getFunctionName,
        //外部也可直接使用的函数
        toQueryString: _QueryString,
        toStringFormat: _StringFormat,
        toIsJSON: _IsJSON,
        toEvalScripts: _EvalScripts,
        toEscapeHTML: _EscapeHTML,
        toUnescapeHTML: _UnescapeHTML,
        toEscapeWeizhichar: _EscapeWeizhichar,
        toDecimal: _ToDecimal,
        toCheckStringLength: _CheckStringLength,
        toJsonToString: _JsonToString,
        toDateObjectFormat: _DateObjectFormat,
        toAjaxJson: _ajaxJson,
        toAjaxDownloadFile: _ajaxDownloadFile,
        toJsonToArr: _JsonToArr,
        toArrToJon: _ArrToJson,
        toShowModalDialog: showtoModalDialog,
        toShowLoading: _showLoading,
        toCloseLoading: _closeLoading,
        toCreateXmlDoc: _createXmlDoc,
        toRefreshPage: _refreshPage,
        toBuildUrl: buildUrl,
        toGetTimeRandomNum: _GetTimeRandomNum,
        toGetRandomNum: _GetRandomNum,
        toGetDateDiff: _GetDateDiff,
        toGuid: _GetGuid(),
        toGetIEVersionNo: _getIEVersionNumber,
        toIsHadBindClickEvent: _isHadBindClickEvent
    });
})();
/*********************Base End*********************/


/***************Number 扩展************************/
Object.extend(Number.prototype, (function () {
    //转十六进制
    function toColorPart() {
        return this.toPaddedString(2, 16);
    }
    //加1
    function succ() {
        return this + 1;
    }
    //位数，不足左边加0，radix：进制基数，即2二进制，10十进制，8八进制，16进制
    function toPaddedString(length, radix) {
        var string = this.toString(radix || 10);
        return '0'.toCopyTimes(length - string.length) + string;
    }
    //取绝对数
    function abs() {
        return Math.abs(this);
    }

    //四舍五入取整
    function round() {
        return Math.round(this);
    }
    //向上取整
    function ceil() {
        return Math.ceil(this);
    }
    //向下取整
    function floor() {
        return Math.floor(this);
    }
    return {
        toColorPart: toColorPart,
        toSucc: succ,
        toPaddedString: toPaddedString,
        toAbs: abs,
        toTound: round,
        toCeil: ceil,
        toFloor: floor,
        toDecimal: _ThisToDecimal
    };
})());

/***************Number 扩展结束************************/


/***************String 扩展************************/
Object.extend(String, {
    toInterpret: function (value) {
        return value == null ? '' : String(value);
    },
    toSpecialChar: {
        '\b': '\\b',
        '\t': '\\t',
        '\n': '\\n',
        '\f': '\\f',
        '\r': '\\r',
        '\\': '\\\\'
    }
});

Object.extend(String.prototype, {
    toTrim: _Stringtrim,
    toTrimTags: _StringtrimTags,
    toStartWith: _StringStartWith,
    toEndWith: _StringEndWith,
    toCapitalize: _StringCapitalize,
    toIncludeString: _IncludeString,
    toTruncate: _Truncate,
    toSucc: _Succ,
    toCopyTimes: _CopyTimes
});
Date.prototype.toDateFormat = _DateFormat;


/*********************String扩展结束******************************************/

/*********************Date 扩展结束******************************************/
Object.extend(Date, {
    toGetDatePeriodDay:
    //两个日期相隔多少天
    function getDatePeriodDay(startDate, endDate) {
        return (Math.abs(startDate * 1 - endDate * 1) / 60 / 60 / 1000 / 24).toFloor();
    }
});


Object.extend(Date.prototype, (function () {
    var R_ISO8601_STR = /^(\d{4})-?(\d\d)-?(\d\d)(?:T(\d\d)(?::?(\d\d)(?::?(\d\d)(?:\.(\d+))?)?)?(Z|([+-])(\d\d):?(\d\d))?)?$/;
    function toISOString() {
        return this.getUTCFullYear() + '-' +
          (this.getUTCMonth() + 1).toPaddedString(2) + '-' +
          this.getUTCDate().toPaddedString(2) + 'T' +
          this.getUTCHours().toPaddedString(2) + ':' +
          this.getUTCMinutes().toPaddedString(2) + ':' +
          this.getUTCSeconds().toPaddedString(2) + 'Z';
    }


    function toJSON() {
        return this.toISOString();
    }

    function jsonStringToDate(string) {
        var match;
        if (match = string.match(R_ISO8601_STR)) {
            var date = new Date(0),
                    tzHour = 0,
                    tzMin = 0,
                    dateSetter = match[8] ? date.setUTCFullYear : date.setFullYear,
                    timeSetter = match[8] ? date.setUTCHours : date.setHours;
            if (match[9]) {
                tzHour = toInt(match[9] + match[10]);
                tzMin = toInt(match[9] + match[11]);
            }
            dateSetter.call(date, toInt(match[1]), toInt(match[2]) - 1, toInt(match[3]));
            var h = toInt(match[4] || 0) - tzHour;
            var m = toInt(match[5] || 0) - tzMin;
            var s = toInt(match[6] || 0);
            var ms = Math.round(parseFloat('0.' + (match[7] || 0)) * 1000);
            timeSetter.call(date, h, m, s, ms);
            return date;
        }
        return string;
    }

    //两个日期相隔多少天
    function getDatePeriodDay(startDate, endDate) {
        return (Math.abs(startDate * 1 - endDate * 1) / 60 / 60 / 1000 / 24).toFloor();
    }
    //获取日期所在月的第一天
    function getFirstDateInMonth(date) {
        if (date == null) date = this;
        return new Date(date.getFullYear(), date.getMonth(), 1);
    }
    //获取日期所在月的最后天
    function getLastDateInMonth(date) {
        if (date == null) date = this;
        return new Date(date.getFullYear(), date.getMonth() + 1, 0);
    }
    //获取日期所在季的第一天
    function getFirstDateInQuarter(date) {
        if (date == null) date = this;
        return new Date(date.getFullYear(), ~~(date.getMonth() / 3) * 3, 1);
    }
    //获取日期所在季的第一天
    function getLastDateInQuarter(date) {
        if (date == null) date = this;
        return new Date(date.getFullYear(), ~~(date.getMonth() / 3) * 3 + 3, 0);
    }
    //是否为闰年
    function isLeapYear() {
        return new Date(this.getFullYear(), 2, 0).getDate() == 29;
    }
    //获取当前月份的天数
    function getDaysInMonth(date) {
        if (date == null) date = this;
        return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    }

    return {
        toDateFormat: _DateFormat,
        toISOString: toISOString,
        toJSON: toJSON,
        toJsonStringToDate: jsonStringToDate,
        toGetDatePeriodDay: getDatePeriodDay,
        toGetFirstDateInMonth: getFirstDateInMonth,
        toGetLastDateInMonth: getLastDateInMonth,
        toGetFirstDateInQuarter: getFirstDateInQuarter,
        toGetLastDateInQuarter: getLastDateInQuarter,
        toIsLeapYear: isLeapYear,
        toGetDaysInMonth: getDaysInMonth
    };
})());

/*********************Function扩展开始******************************************/
Object.extend(Function.prototype, (function () {
    var slice = Array.prototype.slice;
    //内部用
    function update(array, args) {
        var arrayLength = array.length, length = args.length;
        while (length--) array[arrayLength + length] = args[length];
        return array;
    }
    //合并两个数据到第一个数组中
    function merge(array, args) {
        //截取数组
        array = slice.call(array, 0);
        return update(array, args);
    }

    //获取函数的形参，以字符串数组形式返回
    function argumentNames() {
        var names = this.toString().match(/^[\s\(]*function[^(]*\(([^)]*)\)/)[1]
          .replace(/\/\/.*?[\r\n]|\/\*(?:.|[\r\n])*?\*\//g, '')
          .replace(/\s+/g, '').split(',');
        return names.length == 1 && !names[0] ? [] : names;
    }

    function bind(context) {
        if (arguments.length < 2 && Object.isUndefined(arguments[0])) return this;
        var __method = this, args = slice.call(arguments, 1);
        return function () {
            var a = merge(args, arguments);
            return __method.apply(context, a);
        };
    }

    function bindAsEventListener(context) {
        var __method = this, args = slice.call(arguments, 1);
        return function (event) {
            var a = update([event || window.event], args);
            return __method.apply(context, a);
        };
    }
    //函数的柯里化，用于一个操作分成多步进行，并可以改变原函数的行为
    function curry() {
        if (!arguments.length) return this;
        var __method = this, args = slice.call(arguments, 0);
        return function () {
            var a = merge(args, arguments);
            return __method.apply(this, a);
        };
    }
    //SetTimeOut的用法，推迟多少秒
    function delay(timeout) {
        var __method = this, args = slice.call(arguments, 1);
        timeout = timeout * 1000;
        return window.setTimeout(function () {
            return __method.apply(__method, args);
        }, timeout);
    }
    //强制延迟0.01秒才执行原函数
    function defer() {
        var args = update([0.01], arguments);
        return this.delay.apply(this, args);
    }
    //AOP的实现
    function wrap(wrapper) {
        var __method = this;
        return function () {
            var a = update([__method.bind(this)], arguments);
            return wrapper.apply(this, a);
        };
    }

    function methodize() {
        if (this._methodized) return this._methodized;
        var __method = this;
        return this._methodized = function () {
            var a = update([this], arguments);
            return __method.apply(null, a);
        };
    }

    return {
        argumentNames: argumentNames,
        bind: bind,
        bindAsEventListener: bindAsEventListener,
        curry: curry,
        delay: delay,
        defer: defer,
        wrap: wrap,
        methodize: methodize
    };
})());
/*********************Function扩展结束******************************************/

/*********************Array扩展开始******************************************/

/*********************Array扩展结束******************************************/

/*********************this 共用的对象最小单元通用独立方法开始*********************/

//首字母大写
function _StringCapitalize() {
    return this.charAt(0).toUpperCase();
}

//判断字符串是否以指定字符开头
function _StringStartWith(startStr, ignorecase) {
    var startString = this.substr(0, startStr.length);
    return ignorecase ? startString.toLocaleLowerCase() == startStr.toLocaleLowerCase() : startString == startStr;
}

//判断字符串是否以指定字符结尾
function _StringEndWith(endStr, ignorecase) {
    var endString = this.substring(this.length - endStr.length);
    return ignorecase ? endString.toLocaleLowerCase() == endStr.toLocaleLowerCase() : endString == endStr;

}

//去除字符两边的标签
function _StringtrimTags() {
    return this.replace(/<\w+(\s+("[^"]*"|'[^']*'|[^>])+)?>|<\/\w+>/gi, '');
}

//去除字符两边的空隔
function _Stringtrim() {
    if (arguments.length !== 0) throw Error.parameterCount();
    return this.replace(/^\s+|\s+$/g, '');
}

//是否包含了指定字符串
function _IncludeString(pattern) {
    return this.indexOf(pattern) > -1;
}

//格式化日期时间：format：yyyy-MM-dd
function _DateFormat(format) {
    var o = {
        "M+": this.getMonth() + 1, //month   
        "d+": this.getDate(),    //day   
        "h+": this.getHours(),   //hour   
        "H+": this.getHours(),   //hour   
        "m+": this.getMinutes(), //minute   
        "s+": this.getSeconds(), //second   
        "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter   
        "S": this.getMilliseconds() //millisecond   
    };
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
    (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o) if (new RegExp("(" + k + ")").test(format))
        format = format.replace(RegExp.$1,
      RegExp.$1.length == 1 ? o[k] :
        ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}

//保留指定中文长度，默认25中文字符长度，truncation：默认为...
function _Truncate(length, truncation) {
    length = length || 25;
    truncation = Object.toIsUndefined(truncation) ? '...' : truncation;
    return this.length > length ?
      this.slice(0, length) + truncation : String(this);
}

//加1操作，对数字类型的字符串
function _Succ() {
    return this.slice(0, this.length - 1) +
      String.fromCharCode(this.charCodeAt(this.length - 1) + 1);
}

//复制N次字符串
function _CopyTimes(count) {
    return count < 1 ? '' : new Array(count + 1).join(this);
}
/*********************this 对象最小单元通用独立方法结束*********************/


/*********************最小单元通用独立方法开始 也可被页面直接使用，供prototype或类使用*********************************/

//类似C#StringFormat的格式化，这里更强大，支持JSON键值方式
//例子 var a=StringFormat("Result is {0},{1}",22,33);
//var b=StringFormat("Result is {Name},{Age}",{Name:"Jhon",Age:14});
function _StringFormat(str, object) {
    var array = Array.prototype.slice.call(arguments, 1);
    return str.replace(/\\?\{([^{}]+)\}/gm, function (match, name) {
        if (match.charAt(0) == '\\')
            return match.slice(1);
        var index = Number(name);
        if (index >= 0)
            return array[index];
        if (object && object[name] != void 0)
            return object[name];
        return '';

    });
}

//获取Url传递的参数值
function _QueryString(Parametername) {
    var reg = new RegExp("(^|&)" + Parametername + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

//判断是否为Json对象
function _IsJSON(object) {
    var str = object;
    if (str.blank()) return false;
    str = str.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, '@');
    str = str.replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']');
    str = str.replace(/(?:^|:|,)(?:\s*\[)+/g, '');
    return (/^[\],:{}\s]*$/).test(str);
}


//生成随机guid数
function _GetGuid() {
    var S4 = function () {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    };
    return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
}

//转换为脚本原型
function _EvalScripts(object) {
    return object.extractScripts().map(function (script) { return eval(script); });
}

//进行HTML编码，即代码转为显示字符
function _EscapeHTML(object) {
    return object.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

//Html反编码，即转为编程代码
function _UnescapeHTML(object) {
    return object._StringtrimTags.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
}
//编码为中文符号：<转为〈
function _EscapeWeizhichar(object) {
    return object.replace(/=/g, '＝').replace(/</g, '＜').replace(/>/g, '＞');;
}
/*四舍五入 将数字转换成指定保留位数 v要保留的位数*/
function _ThisToDecimal(v) {
    return _ToDecimal(this, v);
}

/*四舍五入 将数字转换成指定保留位数 num要转换的数,v要保留的位数*/
function _ToDecimal(num, v) {
    var vv = Math.pow(10, v);
    return Math.round(num * vv) / vv;
}

//检查输入的字符数长度。
function _CheckStringLength(strTemp) {
    var i, sum;
    sum = 0;
    for (i = 0; i < strTemp.length; i++) {
        if ((strTemp.charCodeAt(i) >= 0) && (strTemp.charCodeAt(i) <= 255))
            sum = sum + 1;
        else
            sum = sum + 2; //汉字占有两个字符
    }
    return sum;
}


//Json转换为String
function _JsonToString(object) {
    return JSON.stringify(object);
}


//格式化日期"yyyy-MM-dd hh:mm:ss"
function _DateObjectFormat(dateObject, format) {
    var o = {
        "M+": dateObject.getMonth() + 1, //month   
        "d+": dateObject.getDate(),    //day   
        "h+": dateObject.getHours(),   //hour   
        "m+": dateObject.getMinutes(), //minute   
        "s+": dateObject.getSeconds(), //second   
        "q+": Math.floor((dateObject.getMonth() + 3) / 3),  //quarter   
        "S": dateObject.getMilliseconds() //millisecond   
    };
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
    (dateObject.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o) if (new RegExp("(" + k + ")").test(format))
        format = format.replace(RegExp.$1,
      RegExp.$1.length == 1 ? o[k] :
        ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}

//Json转数组
function _JsonToArr(jsonObject) {
    var arr = [];
    for (var property in jsonObject) {
        var arrItem = { name: property, value: jsonObject[property] };
        arr.push(arrItem);
    }
    return arr;
}
//将name value对象的数组转Json
function _ArrToJson(arrObject) {
    var n = arrObject.length;
    var jsonString = "{";

    for (var i = 0; i < n; i++) {
        jsonString += ":\"";
        jsonString += arrObject[i].name;
        jsonString += ":\"";

        jsonString += ":\"";
        jsonString += arrObject[i].value;
        jsonString += ":\"";

        if (i != n - 1) jsonString += ",";
    }
    var jsonString = "}";
    return Object.toJSON(jsonString);
}

//获取一个随机数
function _GetRandomNum(Min, Max) {
    var Range = Max - Min;
    var Rand = Math.random();
    return (Min + Math.round(Rand * Range));
}

///获取一个时间戳
function _GetTimeRandomNum() {
    var randomCode = new Date().valueOf();
    return randomCode;
}

//reload方式刷新
function _refreshPage() {
    window.location.reload();
}

function _getIEVersionNumber() {
    if (/msie/.test(navigator.userAgent.toLowerCase())) {
        var ua = navigator.userAgent.toLowerCase();
        return IEVersion = ua.match(/msie ([\d.]+)/)[1];
    }
    return "";
}



/* 
* 获得时间差,时间格式为 年-月-日 小时:分钟:秒 或者 年/月/日 小时：分钟：秒 
* 其中，年月日为全格式，例如 ： 2010-10-12 01:00:00 
* 返回精度为：秒，分，小时，天
*diffType：day，minute，hour，second
*var result = GetDateDiff("2010-02-26 16:00:00", "2011-07-02 21:48:40", "day"); 
*/
function _GetDateDiff(startTime, endTime, diffType) {
    //将xxxx-xx-xx的时间格式，转换为 xxxx/xx/xx的格式 
    startTime = startTime.replace(/\-/g, "/");
    endTime = endTime.replace(/\-/g, "/");
    //将计算间隔类性字符转换为小写
    diffType = diffType.toLowerCase();
    var sTime = new Date(startTime);      //开始时间
    var eTime = new Date(endTime);  //结束时间
    //作为除数的数字
    var divNum = 1;
    switch (diffType) {
        case "second":
            divNum = 1000;
            break;
        case "minute":
            divNum = 1000 * 60;
            break;
        case "hour":
            divNum = 1000 * 3600;
            break;
        case "day":
            divNum = 1000 * 3600 * 24;
            break;
        default:
            break;
    }
    var subdif = parseFloat((eTime.getTime() - sTime.getTime()) / parseInt(divNum));
    return _ToDecimal(subdif, 1);
}
/*********************最小单元通用独立方法结束******************************************/

/*********************Aajx操作******************************************/
//获取json数据ajax请求 methodName:方法名,
//methodName可为null, 为null时默认请求地址方法，如 handler的 ProcessRequest
//async是否异步：默认false
//data Json参数如{a:"aValue",b:"bValue"}
//data 数组参数形式[{name:"a",value"aValue"},{name:"b",value"bValue"}]
//type:请求类别默认post
//dataType:预期服务器返回的数据类型[string,xml,html,script,json(默认),text]
function _ajaxJson(url, method, data, async, type, callback, dataType) {
   
    var json = {};
    var isAsync = async || false;
    var theData = [];
    var item = { name: "method", value: method };

    if (!Object.toIsArray(data)) {
        //Json参数形式
        theData = data;
        if (method) {
            var arr = Object.toJsonToArr(data);
            theData = arr;
            theData.push(item);
        }
    } else {
        //数组参数形式
        theData = data;
        if (method) theData.push(item);

    }

    $.ajax({
        type: type || "POST",
        async: isAsync,
        url: url,
        data: theData,
        dataType: dataType || 'json',
        success: function (d) {
            if (callback && typeof (callback) != "function") {
                throw TypeError("the callback parameter not is a function");
            }
            else {
                if (callback) {
                    callback(d);
                }
                json = d;
            }
        },
        beforeSend: function (d) {
           Object.toShowLoading();
        },
        complete:function(d)
        {
            //请求成功或失败时均调用
            setTimeout(function () { Object.toCloseLoading(); },200);
        },
        error: function (d) {
        
            throw new Error("服务器返回数据出错");
        }
    });
    return json;
}

//ajax下载文件
//url Handdler地址
//data参数：支持数组格式或Json格式
//data Json参数如{a:"aValue",b:"bValue"}
//data 数组参数形式[{name:"a",value"aValue"},{name:"b",value"bValue"}]
function _ajaxDownloadFile(url, method, data) {
    var theData = [];
    var item = { name: "method", value: method };
    if (!Object.toIsArray(data)) {
        //Json参数形式,需转数组
        var arr = Object.toJsonToArr(data);
        theData = arr;
        theData.push(item);

    } else {
        //数组参数形式
        theData = data;
        if (method) theData.push(item);

    }
    var div_frame = $("#div_ifrme_template");
    div_frame && div_frame.remove();
    var div = $("<div>").attr("id", "div_ifrme_template");
    var iframeName = "framePost";
    var form_export = $("<form>").attr("action", url).attr("target", iframeName).attr("method", "POST");
    //构造参数
    for (var i in theData) {
        form_export.append($("<input>").attr("name", theData[i].name).val(theData[i].value));
    }
    var ifrme = $("<iframe>").attr("name", iframeName).css({ display: 'none' });
    div.append(ifrme);
    div.append(form_export).css({ display: 'none' });
    $("body").append(div);
    form_export[0].submit();
    ifrme[0].contentWindow.onload = function () {
        if (ifrme[0].contentWindow.document.body.innerHTML.length > 0) {
            alert("下载失败，服务器文件已丢失...");
        }
    };
}
/*********************Aajx操作结束******************************************/

////////////////////// 窗口开始////////////////////////////

//打开一个居中的模式对话框
//返回弹出窗口传递回的值 objectParm对象参数
function showtoModalDialog(url, dlgWidth, dlgHeight, objectParm) {
    var dlgLeft = (window.screen.width - dlgWidth) / 2;
    var dlgTop = (window.screen.height - dlgHeight) / 2;
    var widthTmp = dlgWidth;
    var form = "resizable:yes;scroll:no;status:no;dialogHeight:" + dlgHeight + "px;dialogWidth:" + widthTmp + "px;dialogLeft:" + dlgLeft + ";dialogTop:" + dlgTop;

    // 加上时间戳
    var randomCode = new Date().valueOf();
    if (url.indexOf("?") >= 0) {
        url = url + "&" + randomCode;
    } else {
        url = url + "?" + randomCode;
    }
    objectParm = objectParm || '';
    return window.showModalDialog(url, objectParm, form);
}

/**
* 给URL最后面加上时间戳,参数 paramObject.a=a paramObject.b=bbb;
*/
function buildUrl(url, paramObject) {
    if (paramObject) {
        var queryString = "";
        var attrs = paramObject.attributes;
        for (var attr in paramObject) {
            var name = attr;
            var value = paramObject[attr];

            if (queryString.length > 0) { queryString += "&"; }
            queryString += name + "=" + encodeURI(value);
        }
        if (queryString.length > 0) {
            if (url.indexOf("?") >= 0) {
                url = url + "&" + queryString;
            } else {
                url = url + "?" + queryString;
            }
        }
    }
    return url;
}
//判断Jquery是否绑定了点击事件：示例： Object.toIsHadBindClickEvent($("#myli"));
function _isHadBindClickEvent(jqueryObject) {
    var objEvt = $._data(jqueryObject[0], "events");
    if (objEvt && objEvt["click"]) {
        return true;
    }
    return false;
}
//加载遮罩层
function _showLoading(message) {
    var msg = message || "正在处理，请稍等......";
    var paddingtop = parseInt(window.document.documentElement.clientHeight / 2);
    var opacity = "opacity:0.4;"; //IE 7 8 9
    if (/msie/.test(navigator.userAgent.toLowerCase())) {
        var ua = navigator.userAgent.toLowerCase();
        var IEVersion = ua.match(/msie ([\d.]+)/)[1];
        if (parseInt(IEVersion) < 10) {
            opacity = "filter: alpha(opacity =40);";
        }

    }
    //opacity = "filter: alpha(opacity =70);";
    var loadingHtml = "<div id=\"LoadingDiv\" style='text-align:center; border:solid 2px #D4F0FC; font-weight: bold; float: left; width: 100%;  height:100%;line-height: 100%;  position: absolute;  top: 1px; left: 1px; z-index: 1000;" + opacity + "\" style=\"text-align: center; background-color:#F6F6F6;  font-size: 14px; color: Red; padding-top:" + paddingtop + "px;'><div><img alt=\"\" src=\""+ui+"/Workflow/Resources/Images/mask_loading.gif\" /></div><div>" + msg + "<span style='cursor:pointer' onclick=\"_closeLoading();\">关闭</span></div></div>";
    if ($("body")) {
        if ($("#LoadingDiv")[0]) {
            $("#LoadingDiv").show();
        }
        else {
            $(document.body).append(loadingHtml);
            $("#LoadingDiv").show();
        }
    }
}

//关闭遮罩层
function _closeLoading() {
    if ($("#LoadingDiv")[0]) {
        $("#LoadingDiv").remove();
        $("#LoadingDiv").hide();
    }
}
/////////////////////////////////////////////////// 窗口结束///////////////////////////////////

/////////////////////////////////////////////////// 弹出消息框开始///////////////////////////////////
/*
弹出框以及系统消息框（EasyUI样式）
*/
function showMsg(title, msg, isAlert) {
    if (isAlert !== undefined && isAlert) {
        $.messager.alert(title, msg);
    } else {
        $.messager.show({
            title: title,
            msg: msg,
            showType: 'show'
        });
    }
}

/*
显示确认框（EasyUI样式）
*/
function showConfirm(title, msg, callback) {
    $.messager.confirm(title, msg, function (r) {
        if (r) {
            if (jQuery.isFunction(callback))
                callback.call();
        }
    });
}

/*
显示进度框（EasyUI样式）
*/
function showProcess(isShow, title, msg) {
    if (!isShow) {
        $.messager.progress('close');
        return;
    }
    $.messager.progress({
        title: title,
        msg: msg
    });
}
/////////////////////////////////////////////////// 弹出消息框结束///////////////////////////////////


///////////////////////////////////////////////////Xml操作///////////////////////////////////
//创建Xml文档对象
//是否给xmlText加一个Root根节点,默认否
//$(xmlDoc).find("Root>Item").each(function () {
//$(this).attr("Text")取属性
//$(this).text() 取内容
//});
function _createXmlDoc(xmlText, isNeedAddRoot) {
    var xmlDoc = null;
    var addRoot = isNeedAddRoot || false;
    if (addRoot)
        xmlText = "<Root>" + xmlText + "</Root>";
    try //Internet Explorer
    {
        xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
        xmlDoc.async = "false";
        xmlDoc.loadXML(xmlText);

    }
    catch (e) {
        try //Firefox, Mozilla, Opera, etc.
        {
            parser = new DOMParser();
            xmlDoc = parser.parseFromString(xmlText, "text/xml");
        }
        catch (e) { }
    }
    return xmlDoc;
}


///////////////////////////////////////////////////Xml操作结束///////////////////////////////////