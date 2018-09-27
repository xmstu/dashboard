var set = {
    init: function () {
        layui.use(['layer', 'laydate'], function () {
            var layer = layui.layer;
            var laydate = layui.laydate;
            laydate.render({
                elem: '#delivery_start_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#delivery_start_time').val();
                    var endTime = $('#delivery_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#delivery_start_time').val());
                    var endTime = common.timeTransform($('#delivery_end_time').val());
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#delivery_start_time').val() == '') {
                        $('#delivery_start_time').next('.date-tips').show();
                    } else {
                        $('#delivery_start_time').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#delivery_end_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#delivery_start_time').val();
                    var endTime = $('#delivery_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#delivery_start_time').val())
                    var endTime = common.timeTransform($('#delivery_end_time').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#delivery_end_time').val() == '' || val == '') {
                        $('#delivery_end_time').next('.date-tips').show();
                    } else {
                        $('#delivery_end_time').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#register_start_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#register_start_time').val();
                    var endTime = $('#register_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#register_start_time').val())
                    var endTime = common.timeTransform($('#register_end_time').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#register_start_time').val() == '' || val == '') {
                        $('#register_start_time').next('.date-tips').show();
                    } else {
                        $('#register_start_time').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#register_end_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#register_start_time').val();
                    var endTime = $('#register_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#date_show_one').val())
                    var endTime = common.timeTransform($('#date_show_two').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#register_end_time').val() == '' || val == '') {
                        $('#register_end_time').next('.date-tips').show();
                    } else {
                        $('#register_end_time').next('.date-tips').hide()
                    }
                }
            });
        });
        $('.menu-map').addClass('menu-active');
        $('.menu-active .icon-xia').addClass('icon-rotate')
        $('.menu-map').next('.second-menu-list').css({'display': 'block'});
        $('.menu-map').next('.second-menu-list').find('.goodsMap-second-menu').addClass('selected-active')
    },
    mapRender: function (heatMapData, maxCount,center) {
        var zoom;
        var role = $('#user-info').attr('data-role-type');
        if (role == 1) {
            zoom = 6
        } else {
            zoom = 11
        }
        center?center=center:center=[116.418261, 39.921984];
        var map = new AMap.Map("container", {
            resizeEnable: true,
            center: center,
            zoom: zoom
        });
        if (!isSupportCanvas()) {
            layer.msg('热力图仅对支持canvas的浏览器适用,您所使用的浏览器不能使用热力图功能,请换个浏览器试试~', {
                time: 1500
            })
        }
        var heatmap;
        map.plugin(["AMap.Heatmap"], function () {
            //初始化heatmap对象
            heatmap = new AMap.Heatmap(map, {
                radius: 10, //给定半径
                opacity: [0, 1]
                , gradient: {
                    0.5: 'blue',
                    0.65: 'rgb(117,211,248)',
                    0.7: 'rgb(0, 255, 0)',
                    0.9: '#ffea00',
                    1.0: 'red'
                }
            });
            //设置数据集：该数据为北京部分“公园”数据
            heatmap.setDataSet({
                data: heatMapData,
                max:2
            });
            $('#heatMapHide').click(function () {
                heatmap.hide();
            });
            $('#heatMapShow').click(function () {
                heatmap.show();
            });
        });

        //判断浏览区是否支持canvas
        function isSupportCanvas() {
            var elem = document.createElement('canvas');
            return !!(elem.getContext && elem.getContext('2d'));
        }
    },
    operate: function () {
        var _this = this;
        var url = '/map/goods_map/';
        var data = {
            goods_price_type: $('#goods_price_type').val(),
            haul_dist: $('#haul_dist').val(),
            vehicle_length: $('#vehicle_length').val(),
            goods_status: $('#goods_status').val(),
            special_tag: $('#special_tag').val(),
            delivery_start_time: $('#delivery_start_time').val(),
            delivery_end_time: $('#delivery_end_time').val(),
            register_start_time: $('#register_start_time').val(),
            register_end_time: $('#register_end_time').val()
        };
        if (data.delivery_start_time != '') {
            data.delivery_start_time = common.timeTransform($('#delivery_start_time').val() + ' 00:00:00');
        }
        if (data.delivery_end_time != '') {
            data.delivery_end_time = common.timeTransform($('#delivery_end_time').val() + ' 23:59:59');
        }
        if (data.register_start_time != '') {
            data.register_start_time = common.timeTransform($('#register_start_time').val() + ' 00:00:00');
        }
        if (data.register_end_time != '') {
            data.register_end_time = common.timeTransform($('#register_end_time').val() + ' 23:59:59');
        }
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                if (res.data == '') {
                    layer.msg('该条件无数据！', {icon: 5});
                } else {
                    var heatMapData = res.data;
                    var maxCount = res.max_lat_lng.max_count;
                    var center=[];
                    center.push(res.max_lat_lng.lng)
                    center.push(res.max_lat_lng.max_lat);
                    _this.mapRender(heatMapData, maxCount,center)
                }
            }, function (xhttp) {
                layer.closeAll('loading')
            })
        })
    }
};
set.operate();
set.init();
set.mapRender();
$('#search_btn').click(function (e) {
    e.preventDefault();
    set.operate();
});
