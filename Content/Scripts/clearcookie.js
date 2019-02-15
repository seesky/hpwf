function foreach()
{
  var strCookie=document.cookie;
  var arrCookie=strCookie.split("; ");
  for(var i=0;i<arrCookie.length;i++)
 {
    var arr=arrCookie[i].split("=");
    if(arr.length>0)
    DelCookie(arr[0]);
 }
}
function GetCookieVal(offset)
{
var endstr = document.cookie.indexOf (";", offset);
if (endstr == -1)
endstr = document.cookie.length;
return decodeURIComponent(document.cookie.substring(offset, endstr));
}
function DelCookie(name)
{
var exp = new Date();
exp.setTime (exp.getTime() - 1);
var cval = GetCookie (name);
document.cookie = name + "=" + cval + "; expires="+ exp.toGMTString();
}
function GetCookie(name)
{
var arg = name + "=";
var alen = arg.length;
var clen = document.cookie.length;
var i = 0;
while (i < clen)
{
var j = i + alen;
if (document.cookie.substring(i, j) == arg)
return GetCookieVal (j);
i = document.cookie.indexOf(" ", i) + 1;
if (i == 0) break;
}
return null;
}
function clearCookie(){
    var date=new Date();
    date.setTime(date.getTime()-10000);
    var keys=document.cookie.match(/[^ =;]+(?=\=)/g);
    if (keys) {
        for (var i =  keys.length; i--;)
          document.cookie=keys[i]+"=0; expire="+date.toGMTString()+"; path=/";
    }
}
