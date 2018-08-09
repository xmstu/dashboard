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
            $(window).load(function () {
                $('.main-content-right').addClass('animated fadeIn')
            });
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var count = res.count;
                var data = res.data;
                var str = '';
                for (var i = 0; i < count; i++) {
                     str += '<div class="layui-colla-item">';
                        str += '<div data-value="' + data[i].id + '" class="layui-colla-title">' + data[i].title;
                        str += '<p class="layui-colla-title-child"><span>' + data[i].date + '</span><i class="read-status orange">' + _that.setAbout(data[i].is_read) + '</i></p></div>';
                    if (i == 0) {
                        str += '<div class="layui-colla-content  layui-show">' + data[i].content + '</div></div>';
                    } else {
                        str += '<div class="layui-colla-content ">' + data[i].content + '</div></div>';
                    }
                }
                $('.layui-collapse').html(_that.resetData(str));
                element.init();//告诉layui对js模板重新渲染
                element.on('collapse(message_list)', function (data) {
                    if (data.show == true) {
                        var url = '/message/user/' + $(this).attr('data-value') + '/?account=' + $('#user-info').attr('data-account');
                        var data = {};
                        var _that = $(this);
                        http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function () {
                            if (_that.find('.read-status').text() == '未读' && res.status == 100000) {
                                _that.find('.read-status').html('已读')
                            }
                        })
                    }
                });
                laypage.render({
                    elem: $('#pagination')
                    , count: count
                    , layout: ['count', 'prev', 'page', 'next', 'refresh', 'skip']
                    , jump: function (obj) {
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
    },
    resetData: function (str) {
        /*js反转义*/
        str = str.replace(/&lt;/g, '<');
        str = str.replace(/&gt;/g, '>');
        return str
    }
};
set.init();