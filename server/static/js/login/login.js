$(document).keypress(function (e) {
    if (e.which == 13) {
        $('input[type="button"]').click();
    }
});
$('body').particleground({
    dotColor: '#eef',
    lineColor: '#eee'
});
$('input[name="pwd"]').focus(function () {
    $(this).attr('type', 'password');
});
$('input[type="text"]').focus(function () {
    $(this).prev().animate({ 'opacity': '1' }, 200);
});
$('input[type="text"],input[type="password"]').blur(function () {
    $(this).prev().animate({ 'opacity': '.5' }, 200);
});
$('input[name="login"],input[name="pwd"]').keyup(function () {
    var Len = $(this).val().length;
    if (!$(this).val() == '' && Len >= 5) {
        $(this).next().animate({
            'opacity': '1',
            'right': '0'
        }, 200);
    } else {
        $(this).next().animate({
            'opacity': '0',
            'right': '20'
        }, 200);
    }
});
// ----------------------------------------------------
layui.use(['layer','form'], function () {
    var layer = layui.layer;
    var form = layui.form;
});
$('button[type="button"]').click(function () {
    var login = $('input[name="username"]').val();
    var pwd = $('input[name="password"]').val();
    if (login == '') {
        layer.msg('对不起,您输入的账号不能为空!');
    } else if (pwd == '') {
        layer.msg('对不起,您输入密码不能为空!');
    } else {
        layer.msg('success')
        $.ajax({
            url:'test.txt',
            type:'GET',
            dataType:'txt',
            beforeSend:function(){
                var index = layer.load(1, {
                    shade: [0.1,'#fff']
                });
            },
            success:function(res){
                layer.msg(res)
                layer.close(layer.index)
            },
            error:function(){
                layer.close(layer.index)
            }
        })
    }
})
// ----------------------------------------------------------------------