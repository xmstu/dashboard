var set = {
    init: function () {
        layui.use(['layer', 'laydate', 'element'], function () {
            var layer = layui.layer;
            var laydate = layui.laydate;
            var element = layui.element;
            element.on('collapse(message_list)', function (data) {
                layer.msg('展开状态：' + data.show);
            });
            $(window).load(function () {
                $('.main-content-right').addClass('animated fadeIn')
            });
        })
    }
};
set.init();