$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
var requestStart = $('#date_show_one').val() + ' 00:00:00';
var requestEnd = $('#date_show_two').val() + ' 23:59:59';
setTimeout(function () {
    $('.user-menu-about > a').addClass("selected-active")
    $('.user-menu-about > a >i').addClass("select-active")
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 10);

layui.use(['laydate', 'layer', 'form', 'table'], function () {
    dataInit();
    var laydate = layui.laydate;
    var table = layui.table;
    var layer = layui.layer;
    laydate.render({
        elem: '#date_show_one',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
        format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
        }
    });
    laydate.render({
        elem: '#date_show_three',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_three').val())
            var endTime = common.timeTransform($('#date_show_four').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_four',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#date_show_four').val() == ''||val=='') {
                $('#date_show_four').next('.date-tips').show();
            } else {
                $('#date_show_four').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_three').val())
            var endTime = common.timeTransform($('#date_show_four').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_five',
        theme: '#009688',
        max: String(common.getNowFormatDate()[0]),
        calendar: true,
         format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#date_show_five').val() == '') {
                $('#date_show_five').next('.date-tips').show();
            } else {
                $('#date_show_five').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_five').val())
            var endTime = common.timeTransform($('#date_show_six').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_six',
        theme: '#009688',
        max: String(common.getNowFormatDate()[0]),
        calendar: true,
         format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#date_show_six').val() == '') {
                $('#date_show_six').next('.date-tips').show();
            } else {
                $('#date_show_six').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_five').val())
            var endTime = common.timeTransform($('#date_show_six').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
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
            $("[data-field='usual_city']").css({'display': 'none'})
            $('.main-content-right').addClass('animated fadeIn');
            $("[data-field='user_type']").children().each(function () {
                if ($(this).text() == 0) {
                    $(this).html('<span style="color: #f40;">未录入</span>')
                } else if ($(this).text() == 1) {
                    $(this).html('货主')
                } else if ($(this).text() == 2) {
                    $(this).html('司机')
                } else if ($(this).text() == 3) {
                    $(this).html('物流公司')
                }
            })
            $("td[data-field='goods_count']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '次')
                }
            })
            $("td[data-field='order_count']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '次')
                }
            })
            $("td[data-field='order_finished_count']").children().each(function () {
                if ($(this).text() != '') {
                    var str = $(this).text();
                    $(this).html(str + '单')
                }
            })
              $("td[data-field='user_name']").children().each(function () {
                if ($(this).text() == '') {
                    $(this).html('未录入').css({'color':'red'})
                }
            })
            common.clearSelect()
        }
        , cols: [[
            {field: 'user_id', title: '用户ID', sort: true},
            {field: 'user_name', title: '用户名'}
            , {field: 'mobile', title: '手机号'}
            , {field: 'user_type', title: '注册角色'}
            , {field: 'role_auth', title: '认证'}
            , {field: 'goods_count', title: '发货'}
            , {field: 'order_count', title: '接单'}
            , {field: 'order_finished_count', title: '完成订单'}
            , {field: 'download_channel', title: '下载渠道'}
            , {field: 'from_channel', title: '注册渠道'}
            , {field: 'last_login_time', title: '最后登陆'}
            , {field: 'create_time', title: '注册时间'}
            , {field: 'usual_city', title: '常驻地'}
        ]]
        , id: 'testReload'
        , page: true
    });
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    var beginTime = $.trim($('#date_show_three').val());
    var finishTime = $.trim($('#date_show_four').val());
    var infinteTime = $.trim($('#date_show_five').val());
    var overTIme = $.trim($('#date_show_six').val());
    if ($('#phone_number').val() != '' && $('#phone_number').val().length != 11) {
          layer.tips('请检查号码格式', '#phone_number', {
            tips: [1, '#009688'],
            time: 3000
        });
        return false;
    }
    if ($('#reference_mobile').val() != '' && $('#reference_mobile').val().length != 11) {
      layer.tips('请检查号码格式', '#reference_mobile', {
            tips: [1, '#009688'],
            time: 3000
        });
        return false;
    }

    if (beginTime !== '' && finishTime == '') {
        layer.tips('请输入结束日期', '#date_show_four', {
            tips: [1, '#009688'],
            time: 4000
        });
        return false;
    }
    if (beginTime == '' && finishTime != '') {
        layer.tips('请输入开始日期', '#date_show_three', {
            tips: [1, '#009688'],
            time: 4000
        });
        return false;
    }
    if (beginTime != '') {
        beginTime = common.timeTransform(beginTime + ' 00:00:00')
    } else {
        beginTime = beginTime
    }
    if (finishTime != '') {
        finishTime = common.timeTransform(finishTime + " 23:59:59")
    } else {
        finishTime = finishTime
    }
    if (infinteTime != '') {
        infinteTime = common.timeTransform(infinteTime + ' 00:00:00')
    } else {
        infinteTime = infinteTime
    }
    if (overTIme != '') {
        overTIme = common.timeTransform(overTIme + ' 23:59:59')
    } else {
        overTIme = overTIme
    }
    if (infinteTime !== '' && overTIme == '') {
         layer.tips('请选择注册日期的结束日期', '#date_show_six', {
            tips: [1, '#009688'],
            time: 3000
        });
        return false
    }
    if (infinteTime == '' && overTIme != '') {
        layer.tips('请选择注册日期的开始日期', '#date_show_five', {
            tips: [1, '#009688'],
            time: 3000
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
        region_id: $.trim($('#area_select').val()) == '' ? common.role_area_show($('#super_manager_area_select_one')) : $.trim($('#area_select').val()),
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
        data.from_channel + '&is_referenced=' + data.is_referenced + '&home_station_province=' + data.home_station_province + '&home_station_city=' + data.home_station_city + '&home_station_county=' + data.home_station_county + '&region_id=' + data.region_id + '&role_type=' + data.role_type + '&role_auth=' + data.role_auth + '&is_actived=' + data.is_actived + '&is_used=' + data.is_used + '&is_car_sticker=' + data.is_car_sticker + '&last_login_start_time=' + data.last_login_start_time + '&last_login_end_time=' + data.last_login_end_time + '&register_start_time=' + data.register_start_time + '&register_end_time=' + data.register_end_time;
    layui.use(['layer', 'table'], function () {
        var table = layui.table;
        var layer = layui.layer;
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

                $("td[data-field='goods_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '次')
                    }
                })
                $("td[data-field='order_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '次')
                    }
                })
                $("td[data-field='order_finished_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '单')
                    }
                })
            }
            , cols: [[
                {field: 'user_id', title: '用户ID', sort: true},
                {field: 'user_name', title: '用户名'}
                , {field: 'mobile', title: '手机号'}
                , {field: 'user_type', title: '注册角色'}
                , {field: 'role_auth', title: '认证'}
                , {field: 'goods_count', title: '发货'}
                , {field: 'order_count', title: '接单'}
                , {field: 'order_finished_count', title: '完成订单'}
                , {field: 'download_channel', title: '下载渠道'}
                , {field: 'from_channel', title: '注册渠道'}
                , {field: 'last_login_time', title: '最后登陆'}
                , {field: 'create_time', title: '注册时间'}
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
        region_id: $('#region_id').val() == '' ? common.role_area_show($('#super_manager_area_select_zero')) : $('#region_id').val(),
        is_auth: $("#is_auth").val()
    };
    var url = '/user/statistic/'
    http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
        if (res.status == 100000) {
            layer.closeAll('loading')
            var len = res.data.xAxis.length;
            var X_data = res.data.xAxis;
            if (len > 0 && len < 20) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 1, X_data[1])
            } else if (len > 0 && len >= 20 && len < 40) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 3, X_data[1])
            } else if (len > 0 && len >= 40 && len < 90) {
                $('.chart-tips').css({'display': 'none'})
                chartInit(res.data.xAxis, res.data.series, 5, X_data[1])
            }
        }
    })
}

Highcharts.setOptions({
    colors: [ /*'#9FE6B8', '#FFDB5C','#ff9f7f',*/  '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
});

function chartInit(xAxis, series, interval, x_value1) {
    $('#charts_container_one').highcharts({
        tooltip: {
            shared: true,
            crosshairs: [{
                width: 1,
                color: '#ccc'
            }, {
                width: 1,
                color: '#ccc'
            }]
        },
        chart: {
            zoomType: 'xy'
        },

        title: {
            text: '用户变化趋势曲线图'
        },
        subtitle: {
            text: null
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
            min:0,
            allowDecimals:false,
            plotLines: [
                {
                    color: '#ddd',
                    dashStyle: 'dash',
                    value: x_value1,
                    width: 1
                }
            ],
            title: {
                text: '人数 (人)',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value}人',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        return this.point.y + '人';
                    }
                }
            },
            series: {
                states: {
                    hover: {
                        enabled: true
                    }
                }
            }
            , marker: {
                radius: 3.5,
                lineWidth: 1,
                //  lineColor: '#666666',
                symbol: 'circle',

                states: {
                    hover: {
                        enabled: true,
                        radius: 3.5
                    }
                }
            },
        },
        series: [{
            name: '人数',
            type: 'line',
            tooltip: {
                valueSuffix: '人'
            },
            data: series
        }]
    });
}

function area_select() {
    var auth_role = $('#user-info').attr('data-role')
    if (!!auth_role && auth_role == 1) {
        $('#super_manager_area').css({'display': 'block'})
        $('#super_manager_area_select_zero').address({
            level: 3,
            offsetLeft: '-124px',
        });
        $('#super_manager_area_one').css({'display': 'block'})
        $('#super_manager_area_select_one').address({
            level: 3,
            offsetLeft: '-124px',
        });
    } else {
        $('#super_manager_area').css({'display': 'none'})
        $('#super_manager_area_two').css({'display': 'none'})
        $('#city_manager_one').css({'display': 'block'})
        $('#city_manager_two').css({'display': 'block'})

    }
}

area_select()
if ($('#region_id').val() == '') {
}
