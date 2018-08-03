var set = {
    init: function () {
        var _that = this;
        layui.use(['layer', 'laydate', 'element', 'laypage'], function () {
            var layer = layui.layer;
            var laydate = layui.laydate;
            var laypage = layui.laypage;
            var element = layui.element;
            var url = '/message/user/';
            var data = {
                'account': $('#user-info').attr('data-account'),
                'page': 1,
                'limit': 10
            };
            element.on('collapse(message_list)', function (data) {
                //layer.msg('展开状态：' + data.show);
            });
            $(window).load(function () {
                $('.main-content-right').addClass('animated fadeIn')
            });
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var count = res.count;
                var data = res.data;
                var str = '';
                for (var i = 0; i < count; i++) {
                    str += '<div class="layui-colla-item">';
                    str += '<div class="layui-colla-title">' + data[i].title;
                    str += '<p class="layui-colla-title-child"><span>' + data[i].date + '</span><i class="read-status orange">' + _that.setAbout(data[i].is_read) + '</i></p></div>';
                    str += '<div class="layui-colla-content">' + data[i].content + '</div></div>';
                }
                $('.layui-collapse').html('');
                $('.layui-collapse').append(str);
                element.init();//告诉layui对js模板重新渲染
                laypage.render({
                    elem: $('#pagination')
                    , count: count
                    , layout: ['count', 'prev', 'page', 'next', 'refresh', 'skip']
                    , jump: function (obj) {
                       // console.log(obj)
                    }
                })
            })
        })
    },
    dataRender: function () {
    },
    setAbout: function (num) {
        if (num == 1) {
            return '已读'
        } else if (num == 0) {
            return '未读'
        }
    }
};
set.init();