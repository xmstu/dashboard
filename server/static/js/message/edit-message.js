var ue = UE.getEditor('editor');
 $(window).load(function(){
 $('.main-content-right').addClass('animated fadeIn')
 });
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
    init();
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
            title:'信息预览',
            closeBtn: 0,
            shadeClose: true,
            area: ['800px', '400px'],
            skin: '#009688',
            content: $('#popup')
        });
    })

}

$('.submit-edit').click(function () {
    var url = '/message/system/';
    var content = UE.getEditor('editor').getContent();
    var title = $('#message_title').val()
    if(title==''){
         layer.tips('请输入标题！', '#message_title', {
            tips: [1, '#009688'],
            time: 3000
        });
        return false;
    }
     if(content==''){
         layer.tips('请输入内容！', '#editor', {
            tips: [3, '#009688'],
            time: 3000
        });
        return false;
    }
    var data = {
        "title": $('#message_title').val(),
        "content": String(content),
        "msg_type": $('[name=publish]:checked').attr('data-value'),
        "push_role": $('[name=publish-role]:checked').attr('data-value')
    };
     data=JSON.stringify(data);
    http.ajax.post(true,false,url,data,http.ajax.CONTENT_TYPE_2,function(res){
        if(res.status==100000){
            layer.msg('发布成功')
            window.location.reload();
        }else {
            layer.msg("发布失败")
        }
    })
});