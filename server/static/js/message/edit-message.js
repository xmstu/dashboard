var ue = UE.getEditor('editor');

function setblur(e) {
    UE.getEditor('editor').blur();
    UE.dom.domUtils.preventDefault(e)
}

function insertHtml() {
    var value = prompt('插入html代码', '');
    UE.getEditor('editor').execCommand('insertHtml', value)
}

function getAllHtml() {

}

function getContent() {
    var arr = [];
    arr.push(UE.getEditor('editor').getContent());
    $('#popup').html(arr.join("\n"));
    init()
    return arr.join("\n")
}

function getPlainTxt() {
    var arr = [];
    arr.push("内容为：");
    arr.push(UE.getEditor('editor').getPlainTxt());
    $('#popup').html(arr.join("\n"));
    init()
}

function setContent(isAppendTo) {
    var arr = [];
    UE.getEditor('editor').setContent('欢迎使用ueditor', isAppendTo);
    alert(arr.join("\n"));
}
function setEnabled() {
    UE.getEditor('editor').setEnabled();
    enableBtn();
}

function getText() {
    //当你点击按钮时编辑区域已经失去了焦点，如果直接用getText将不会得到内容，所以要在选回来，然后取得内容
    var range = UE.getEditor('editor').selection.getRange();
    range.select();
    var txt = UE.getEditor('editor').selection.getText();
    $('#popup').html(txt);
    init()
    return txt;
}

function getContentTxt() {
    var arr = [];
    arr.push("编辑器的纯文本内容为：");
    arr.push(UE.getEditor('editor').getContentTxt());
     $('#popup').html(arr.join("\n"));
    init()
}

function hasContent() {
    var arr = [];
    arr.push("判断结果为：");
    arr.push(UE.getEditor('editor').hasContents());
    layer.msg(arr.join("\n"))
}

function setFocus() {
    UE.getEditor('editor').focus();
}

function disableBtn(str) {
    var div = document.getElementById('btns');
    var btns = UE.dom.domUtils.getElementsByTagName(div, "button");
    for (var i = 0, btn; btn = btns[i++];) {
        if (btn.id == str) {
            UE.dom.domUtils.removeAttributes(btn, ["disabled"]);
        } else {
            btn.setAttribute("disabled", "true");
        }
    }
}

function enableBtn() {
    var div = document.getElementById('btns');
    var btns = UE.dom.domUtils.getElementsByTagName(div, "button");
    for (var i = 0, btn; btn = btns[i++];) {
        UE.dom.domUtils.removeAttributes(btn, ["disabled"]);
    }
}

function init() {
    layui.use('layer', function () {
        var layer = layui.layer;
        layer.open({
            type: 1,
            title: false,
            closeBtn: 0,
            shadeClose: true,
            area:['1200px','400px'],
            skin: '#009688',
            content: $('#popup')
        });
    })

}
  $('.submit-edit').click(function(){
      var url = '/message/system/';
      var content = UE.getEditor('editor').getContent()
      console.log(arr);
      var data = {
           "title": "string",
            "content": content,
            "msg_type": 0,
            "push_role": 0
      };
        layer.msg('success')
   })