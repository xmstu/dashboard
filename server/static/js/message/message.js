/*
* 消息浏览
*/
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
                if (data) {
                    $.each(data, function (val, index) {
                        str += '<div class="layui-colla-item">';
                        str += '<div data-value="' + index.id + '" class="layui-colla-title collapse-' + val + '">' + index.title;
                        str += '<p class="layui-colla-title-child"><span>' + index.date + '</span><i class="read-status orange">' + _this.setAbout(index.is_read) + '</i></p></div>';
                        str += '<div class="layui-colla-content ">' + index.content + '</div></div>';
                    });
                    $('.layui-collapse').html(_this.resetData(str));
                    /*layui监听面板展开关闭，展开的时候消息已读，未展开为未读*/
                    element.on('collapse(message_list)', function (data_set) {
                        if (data_set.show == true) {
                            var url_set = '/message/user/' + $(this).attr('data-value') + '/';
                            var _that = $(this);
                            var data = JSON.stringify({user_name: $('#user-info').attr('data-user-name')});
                            _this.isRead(url_set, _that, data)
                        }
                    });
                }
                /*-----点击消息面板对应展开，写在这里是因为等layui渲染完毕之后再获取dom-----*/
                var param = common.getUrlParam('msg-item');//根据获取url参数展开对应，根据不同条件告诉后端那条消息已读
                var data_set = JSON.stringify({user_name: $('#user-info').attr('data-user-name')});
                if (param == 'all') {
                    var url = '/message/user/0/';
                    _this.isRead(url, $('.collapse-0'), data_set)
                    $('.collapse-0').next('.layui-colla-content').addClass('layui-show');
                } else {
                    var url ='/message/user/' + $('.collapse-' + param + '').attr('data-value') + '/';
                     _this.isRead(url,  $('.collapse-' + param + ''), data_set)
                    $('.collapse-' + param + '').next('.layui-colla-content').addClass('layui-show')
                }
                element.init();//告诉layui对js模板重新渲染
                /*-------------------------------------------------------------------------------------*/
                laypage.render({
                    elem: $('#pagination'),
                    count: count,
                    limit: 40,
                    layout: ['count', 'prev', 'page', 'next', 'refresh', 'skip'],
                    jump: function (obj) {
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
    isRead: function (url, element, data) {
        if (element.find('.read-status').text() == '未读') {
            http.ajax.put_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                if (res.status == 100000) {
                    element.find('.read-status').html('已读')
                }
                layer.closeAll('loading')
            })
        }
    }
};
set.init();