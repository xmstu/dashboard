$('.login-page').addClass('animated zoomIn')
$(document).keypress(function (e) {
    if (e.which == 13) {
        $('input[type="button"]').click();
    }
});
$('body').particleground({
    dotColor: '#f5f5f5',
    lineColor: '#f5f5f5',
    particleRadius: 7.5,
    'Dot size': 5
});
$('input[name="pwd"]').focus(function () {
    $(this).attr('type', 'password');
});
$('input[type="text"]').focus(function () {
    $(this).prev().animate({'opacity': '1'}, 200);
});
$('input[type="text"],input[type="password"]').blur(function () {
    $(this).prev().animate({'opacity': '.5'}, 200);
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
layui.use(['layer', 'form'], function () {
    var layer = layui.layer;
    var form = layui.form;
});
$('button[type="button"]').click(function () {
    checkUser()
});
// ----------------------------------------------------------------------
$(document).keyup(function (event) {
    switch (event.keyCode) {
        case 13:
         checkUser();
         return;
    }
});
function checkUser(){
    var login = $('input[name="username"]').val();
    var pwd = $('input[name="password"]').val();
    var role = $('[name=role]:checked').val() ? parseInt($('[name=role]:checked').val()) : 1;
    if (login == '') {
        layer.msg('对不起,您输入的账号不能为空!');
    } else if (pwd == '') {
        layer.msg('对不起,您输入密码不能为空!');
    } else {
        var url = '/login/';
        var data = {
            user_name: login,
            password: hex_md5(pwd),
            role: role
        };
        data = JSON.stringify(data);
        http.ajax.post(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
            if (res.msg == '电话号码有误') {
                layer.msg('号码有误，请核对您的号码！')
            } else if (res.status == '100000') {
                window.location.href = '/home/'
            } else {
                layer.msg('服务器错误')
            }
            return false;
        })
    }
}