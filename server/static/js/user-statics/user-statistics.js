$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
var requestStart = $('#date_show_one').val() + ' 00:00:00';
var requestEnd = $('#date_show_two').val() + ' 23:59:59';
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);
$('#area_select').address({
    offsetLeft: '0',
    level: 3,
    onClose: function () {
    }
});
layui.use(['laydate', 'layer', 'form', 'table'], function () {
    dataInit();
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
    layer.load();
    laydate.render({
        elem: '#date_show_one',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[4]),
        ready: function () {

        },
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        ready: function () {

        },
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
        }
    });
    laydate.render({
        elem: '#date_show_three',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[5]),
        ready: function () {

        },
        done: function (val, index) {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#date_show_four',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        ready: function () {

        },
        done: function (val, index) {
            if ($('#date_show_four').val() == '') {
                $('#date_show_four').next('.date-tips').show();
            } else {
                $('#date_show_four').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#date_show_five',
        theme: '#1E9FFF',
        max: String(common.getNowFormatDate()[5]),
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            if ($('#date_show_five').val() == '') {
                $('#date_show_five').next('.date-tips').show();
            } else {
                $('#date_show_five').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#date_show_six',
        theme: '#1E9FFF',
        max: String(common.getNowFormatDate()[3]),
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            if ($('#date_show_four').val() == '') {
                $('#date_show_four').next('.date-tips').show();
            } else {
                $('#date_show_four').next('.date-tips').hide()
            }
        }
    });
    table.render({
        elem: '#LAY_table_user'
        , url: '/user/list/',
        even: true,
        response: {
            statusName: 'status',
            statusCode: 100000
        },
        done: function (res, curr, count) {
            $('[data-field]>div').css({'padding': '0 6px'})
            $("[data-field='user_type']").children().each(function () {
                if ($(this).text() == 0) {
                    $(this).text('未录入')
                } else if ($(this).text() == 1) {
                    $(this).text('货主')
                } else if ($(this).text() == 2) {
                    $(this).text('司机')
                } else if ($(this).text() == 3) {
                    $(this).text('物流公司')
                }
            })
            $("[data-field='usual_city']").children().each(function () {
                if ($(this).text() == '') {
                    $(this).text('未查询到该用户常驻地')
                }
            })
            $("[data-field='goods_count']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '次')
                }
            })
            $("[data-field='order_count']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '次')
                }
            })
            $("td[data-field='order_completed']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '单')
                }
            })
        }
        , cols: [[
           {field: 'id', title: '用户ID', sort: true, width: 76},
                {field: 'user_name', title: '用户名', width: 76}
                , {field: 'mobile', title: '手机号', width: 111}
                , {field: 'user_type', title: '注册角色', width: 111}
                , {field: 'role_auth', title: '认证', width: 111}
                , {field: 'goods_count', title: '发货', width: 70}
                , {field: 'order_count', title: '接单', width: 76}
                , {field: 'order_completed', title: '完成订单', width: 76}
                , {field: 'download_channel', title: '下载渠道', width: 110}
                , {field: 'from_channel', title: '注册渠道', width: 146}
                , {field: 'last_login_time', title: '最后登陆', width: 104}
                , {field: 'create_time', title: '注册时间', width: 104}
                , {field: 'usual_city', title: '常驻地'}
        ]]

        , id: 'testReload'
        , page: true
    });
    var $ = layui.$, active = {
        reload: function () {
            var demoReload = $('#demoReload');
            table.reload('testReload', {
                page: {
                    curr: 1
                }
                , where: {
                    key: {
                        id: demoReload.val()
                    }
                }
            });
        }
    };
    $('.dataTable .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    var beginTime = $.trim($('#date_show_three').val());
    var finishTime = $.trim($('#date_show_four').val());
    var infinteTime = $.trim($('#date_show_five').val());
    var overTIme = $.trim($('#date_show_six').val());
    var provinceid = $.trim($('#area_select').attr('provinceid'));
    var cityid =$.trim($('#area_select').attr('cityid'));
    var districtsid = $.trim($('#area_select').attr('districtsid'));
  /*  if (provinceid != '' && districtsid == '') {
        layer.msg('请将常驻地选择到第三级别', function () {
        });
        return false;
    }*/
    if ($('#phone_number').val() != '' && $('#phone_number').val().length != 11) {
        layer.msg('请检查用户名号码长度!', function () {

        });
        return false;
    }
    if ($('#reference_mobile').val() != '' && $('#reference_mobile').val().length != 11) {
        layer.msg('请检查推荐人号码长度!', function () {

        });
        return false;
    }

    if (beginTime !== '' && finishTime == '') {
        layer.msg('请选择最后登陆的结束日期', function () {

        });
        return false;
    }
    if (beginTime == '' && finishTime != '') {
        layer.msg('请选择最后登陆的起始日期', function () {

        });
        return false;
    }
    if (beginTime != '') {
        beginTime = common.timeTransform(beginTime)
    }
    if (finishTime != '') {
        finishTime = common.timeTransform(finishTime)
    }
    if (infinteTime != '') {
        infinteTime = common.timeTransform(infinteTime)
    }
    if (overTIme != '') {
        overTIme = common.timeTransform(overTIme)
    }
    if (infinteTime !== '' && overTIme == '') {
        layer.msg('请选择注册日期的结束日期', function () {

        });
        return false
    }
    if (infinteTime == '' && overTIme != '') {
        layer.msg('请选择注册日期的开始日期', function () {

        });
        return false;
    }

    var data = {
        user_name: $.trim($('#user_name').val()),
        mobile: $.trim($('#phone_number').val()),
        reference_mobile: $.trim($('#reference_mobile').val()),
        download_ch: $.trim($('#download_ch').val()),
        from_channel: $.trim($('#register').val()),
        is_referenced: $.trim($('#is_referenced').val()),
        home_station_province: provinceid,
        home_station_city:cityid,
        home_station_county:districtsid,
        role_type: $.trim($('#role_type').val()),
        role_auth: $.trim($('#role_auth').val()),
        is_actived: $.trim($('#is_actived').val()),
        is_used: $.trim($('#is_used').val()),
        is_car_sticker: $.trim($('#is_car_sticker').val()),
        last_login_start_time: beginTime,
        last_login_end_time: finishTime,
        register_start_time: infinteTime,
        register_end_time: overTIme,
        page: 1,
        limit: 10
    }
    var url = '/user/list/?user_name=' + data.user_name + '&mobile=' + data.mobile + '&reference_mobile=' + data.reference_mobile + '&download_ch=' + data.download_ch + '&from_channel=' +
        data.from_channel + '&is_referenced=' + data.is_referenced + '&home_station_province=' + data.home_station_province + '&home_station_city=' + data.home_station_city+ '&home_station_county=' + data.home_station_county+ '&role_type=' + data.role_type + '&role_auth=' + data.role_auth + '&is_actived=' + data.is_actived + '&is_used=' + data.is_used + '&is_car_sticker=' + data.is_car_sticker + '&last_login_start_time=' + data.last_login_start_time + '&last_login_end_time=' + data.last_login_end_time + '&register_start_time=' + data.register_start_time + '&register_end_time=' + data.register_end_time;

    layui.use('table', function () {
        var table = layui.table;
        table.render({
            url: url
            , elem: '#LAY_table_user'
            , even: true
            , response: {
                statusName: 'status',
                statusCode: 100000
            }
            , done: function () {
                $('[data-field]>div').css({'padding': '0 6px'})
                $("[data-field='user_type']").children().each(function () {
                    if ($(this).text() == 0) {
                        $(this).text('未录入')
                    } else if ($(this).text() == 1) {
                        $(this).text('货主')
                    } else if ($(this).text() == 2) {
                        $(this).text('司机')
                    } else if ($(this).text() == 3) {
                        $(this).text('物流公司')
                    }
                })
                $("[data-field='usual_city']").children().each(function () {
                    if ($(this).text() == '') {
                        $(this).text('未查询到该用户常驻地')
                    }
                })
                $("[data-field='goods_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '次')
                    }
                })
                $("[data-field='order_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '次')
                    }
                })
                $("td[data-field='order_completed']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '单')
                    }
                })
            }
            , cols: [[
                {field: 'id', title: '用户ID', sort: true, width: 76},
                {field: 'user_name', title: '用户名', width: 76}
                , {field: 'mobile', title: '手机号', width: 111}
                , {field: 'user_type', title: '注册角色', width: 111}
                , {field: 'role_auth', title: '认证', width: 111}
                , {field: 'goods_count', title: '发货', width: 70}
                , {field: 'order_count', title: '接单', width: 76}
                , {field: 'order_completed', title: '完成订单', width: 76}
                , {field: 'download_channel', title: '下载渠道', width: 110}
                , {field: 'from_channel', title: '注册渠道', width: 146}
                , {field: 'last_login_time', title: '最后登陆', width: 104}
                , {field: 'create_time', title: '注册时间', width: 104}
                , {field: 'usual_city', title: '常驻地'}
            ]]
            , id: 'testReload'
            , page: true
        });
    })
});
$('#search_btn').on('click', function (e) {
    e.preventDefault();
    dataInit()
})

function dataInit() {
    var requestStartTime = common.timeTransform($('#date_show_one').val() + ' 00:00:00');
    var requestEndTime = common.timeTransform($('#date_show_two').val() + ' 23:59:59');
    var data = {
        start_time: requestStartTime,
        end_time: requestEndTime,
        periods: $('.periods>li').find('button.active').val(),
        user_type: $('#user_type').val(),
        role_type: $('#role_type_first').val(),
        region_id: $('#region_id').val(),
        is_auth: $("#is_auth").val()
    };
    var url = '/user/statistic/'
    http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
        //console.log(res)
        if (res.status == 100000) {
            var len = res.data.xAxis.length;
            var X_data = res.data.xAxis;
            if (len > 0 && len < 20) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 1, X_data[1])
            } else if (len > 0 && len > 20 && len < 40) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 2, X_data[1])
            } else if (len > 0 && len > 40 && len < 90) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 4, X_data[1])
            } else {
                $('#charts_container_one').html('');
                $('.chart-tips').css({'display': 'block'})
                return false
            }
        }
    })
}

function chartInit(xAxis, series, interval, x_value1) {
    Highcharts.setOptions({
        colors: ['#A47D7C', '#DB843D', '#B6A2DE', '#2EC7C9', '#AA4643', '#5AB1EF', '#3D96AE', '#92A8CD', '#B5CA92']
    });
    $('#charts_container_one').highcharts({
        tooltip: {
            shared: true,
            valueSuffix: '人',
            crosshairs: [{
                width: 1,
                color: '#ccc'
            }, {
                width: 1,
                color: '#ccc'
            }],
            plotOptions: {
                spline: {
                    marker: {
                        radius: 4,
                        lineColor: '#666666',
                        lineWidth: 1
                    }
                }
            }
        },
        chart: {
            backgroundColor: '#fff',
            type: 'line'
        },

        title: {
            text: '用户变化趋势曲线图'
        },
        subtitle: {
            text: '数据来源：省省官方后台数据库'
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 1250,
            y: 0,
            floating: true,
            borderWidth: 1,
            backgroundColor: 'transparent',
            labelFormatter: function () {
                return this.name
            }
        },
        xAxis: {
            tickInterval: interval,
            categories: xAxis,
            gridLineColor: '#eee',
            gridLineWidth: 1
        },
        yAxis: {
            gridLineColor: '#eee',
            gridLineWidth: 1,
            plotLines: [
                {
                    color: '#ddd',
                    dashStyle: 'dash',
                    value: x_value1,
                    width: 1
                }
            ],
            title: {
                text: '人数 (人)'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: '人数',
            data: series
        }]
    });
}
