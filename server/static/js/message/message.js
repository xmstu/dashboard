var set = {
    init: function () {
        var _this = this;
        layui.use(['layer', 'laydate', 'element', 'laypage'], function () {
            var layer = layui.layer;
            var laydate = layui.laydate;
            var laypage = layui.laypage;
            var element = layui.element;
            var url = '/message/user/';
            var data = {
                'account': $('#user-info').attr('data-account'),
                'user_name': $('#user-info').attr('data-user-name'),
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
                    str += '<div data-value="' + data[i].id + '" class="layui-colla-title collapse-' + i + '">' + data[i].title;
                    str += '<p class="layui-colla-title-child"><span>' + data[i].date + '</span><i class="read-status orange">' + _this.setAbout(data[i].is_read) + '</i></p></div>';
                    if (i == 0) {
                        str += '<div class="layui-colla-content  layui-show">' + data[i].content + '</div></div>';
                    } else {
                        str += '<div class="layui-colla-content ">' + data[i].content + '</div></div>';
                    }
                }
                $('.layui-collapse').html(_this.resetData(str));
                element.init();//告诉layui对js模板重新渲染

                element.on('collapse(message_list)', function (data_set) {
                    if (data_set.show == true) {
                        var url_set = '/message/user/' + $(this).attr('data-value') + '/?account=' + $('#user-info').attr('data-account');
                        var _that = $(this);
                        _this.isRead(url_set, _that)
                    }
                });
                /*-----第一条消息默认是展开的所以要单独设置已读状态，写在这里是因为等layui渲染完毕之后再获取dom-----*/
                var first_msg = $('.collapse-0');
                console.log(first_msg);
                var value = first_msg.attr('data-value');
                // var url_set = '/message/user/' + value + '/?account=' + $('#user-info').attr('data-account');
                if (first_msg.find('.read-status').html() == '未读') {
                    first_msg.find('.read-status').html('已读')
                }
                /*------------------------------------------------------------------------------------*/
                laypage.render({
                    elem: $('#pagination')
                    , count: count
                    , layout: ['count', 'prev', 'page', 'next', 'refresh', 'skip']
                    , jump: function (obj) {
                    }
                })
            }, function (xhttp) {
                layer.closeAll('loading')
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
        /*js反转义,有很多慢慢加*/
        str = str.replace(/&lt;/g, '<');
        str = str.replace(/&gt;/g, '>');
        str = str.replace(/&nbsp;/g, '');
        str = str.replace(/\n/g, '');
        return str
    },
    isRead: function (url, element) {
        http.ajax.get_no_loading(true, false, url, {}, http.ajax.CONTENT_TYPE_2, function (res) {
            if (element.find('.read-status').text() == '未读' && res.status == 100000) {
                element.find('.read-status').html('已读')

            }
            layer.closeAll('loading')
        })
    }
};
set.init();