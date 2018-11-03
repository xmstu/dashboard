/**
 * 货源统计
 * Created by Creazy_Run on 2018/5/30.
 */
/*设置一些默认日期*/
$('.layui-table-cell').css({'height': 'auto!important'});
$('.layui-form-item').css({'width':'184px'})
$('.chart-area-two-body .layui-form-item').css({'width':'184'})
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[0]));
$('#start_date_one').val(String(common.getNowFormatDate()[2]));
$('#end_time_one').val(String(common.getNowFormatDate()[0]));
$('#start_date_two').val(String(common.getNowFormatDate()[2]));
$('#end_time_two').val(String(common.getNowFormatDate()[0]));
$('#start_date_three').val(String(common.getNowFormatDate()[2]));
$('#end_time_three').val(String(common.getNowFormatDate()[0]));
setTimeout(function () {
    /*设置左边二级菜单样式*/
    $('.menu-transcation').addClass('menu-active');
    $('.menu-active .icon-xia').addClass('icon-rotate')
    $('.menu-transcation').next('.second-menu-list').css({'display': 'block'});
    $('.menu-transcation').next('.second-menu-list').find('.goods-second-menu').addClass('selected-active')
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
    common.dateInterval_Ano($('#start_date_three').val(), $('#end_time_three').val())
}, 10);
/*设置jquery.address地区选择插件*/
function init() {
    $('#from_region_id').address({
        offsetLeft: '0',
        level: 3,
        onClose: function () {

        }
    });
    $('#to_region_id').address({
        offsetLeft: '0',
        level: 3,
        onClose: function () {

        }
    });
    $('.menu-transaction').addClass('menu-active');
    $('.menu-transaction').next('.second-menu-list').css({'display':'block'});
    $('.menu-transaction').next('.second-menu-list').find('.goods-second-menu').addClass('selected-active')
    Highcharts.getOptions().colors = Highcharts.map(Highcharts.getOptions().colors, function (color) {
        return {
            radialGradient: {cx: 0.5, cy: 0.3, r: 0.7},
            stops: [
                [0, color],
                [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
            ]
        };
    });
}
/*运用layui设置日历，表单和数据表格*/
layui.use(['laydate', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    laydate.render({
        elem: '#date_show_one',
        theme: '#1E9FFF',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {

        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#1E9FFF',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
        format:'yyyy/MM/dd',
        done: function (val, index) {

        }
    });
    laydate.render({
        elem: '#create_start_time',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
        format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#create_start_time').val() == '') {
                $('#create_start_time').next('.date-tips').show();
            } else {
                $('#create_start_time').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#create_end_time',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#create_end_time').val() == '') {
                $('#create_end_time').next('.date-tips').show();
            } else {
                $('#create_end_time').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#register_start_time',
        theme: '#009688',
        calendar: true,
        format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#register_start_time').val() == '') {
                $('#register_start_time').next('.date-tips').show();
            } else {
                $('#register_start_time').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#register_end_time',
        theme: '#009688',
        calendar: true,
         format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#register_end_time').val() == '') {
                $('#register_end_time').next('.date-tips').show();
            } else {
                $('#register_end_time').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#start_date_one',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
        format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#start_date_one').val();
            var endTime = $('#end_time_one').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#start_date_one').val() == '') {
                $('#start_date_one').next('.date-tips').show();
            } else {
                $('#start_date_one').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#end_time_one',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#start_date_one').val();
            var endTime = $('#end_time_one').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#end_time_one').val() == '') {
                $('#end_time_one').next('.date-tips').show();
            } else {
                $('#end_time_one').next('.date-tips').hide()
            }

        }
    });
    laydate.render({
        elem: '#start_date_two',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
        format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#start_date_two').val() == '') {
                $('#start_date_two').next('.date-tips').show();
            } else {
                $('#start_date_two').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#end_time_two',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#end_time_two').val() == '') {
                $('#end_time_two').next('.date-tips').show();
            } else {
                $('#end_time_two').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#start_date_three',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#start_date_three').val();
            var endTime = $('#end_time_three').val();
            common.dateInterval_Ano(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#end_time_one').val() == '') {
                $('#end_time_one').next('.date-tips').show();
            } else {
                $('#end_time_one').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#end_time_three',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#start_date_three').val();
            var endTime = $('#end_time_three').val();
            common.dateInterval_Ano(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#end_time_one').val() == '') {
                $('#end_time_one').next('.date-tips').show();
            } else {
                $('#end_time_one').next('.date-tips').hide()
            }
        }
    });
    /*layui的数据表格*/
    table.render({
        elem: '#LAY_table_goods',
        even: true
        , url: '/goods/list/',
        response: {
            statusName: 'status',
            statusCode: 100000
        },
        cols: [[
            {field: 'id', title: '货源ID'},
            {field: 'goods_standard', title: '货物规格'},
            {field: 'goods_type', title: '类型'},
            {field: 'address', title: '出发地-目的地', width: 280},
            {field: 'vehicle', title: '车型要求'},
            {field: 'price', title: '运费',width:110},
            {field: 'mobile', title: '货主手机'},
            {field: 'goods_status', title: '状态'},
            {field: 'call_count', title: '通话数'},
            {field: 'latency_time', title: '初次触达'},
            {field: 'goods_time', title: '时间', width: 170},
            {field: 'node_id', title: '所属网点'}
        ]],
        done: function (res, curr, count) {
             layer.closeAll('loading');
            $('.main-content-right').addClass('animated fadeIn');
            $('[data-field]>div').css({'padding': '0 6px'});
            $('.nearby').on('click', function () {
                layer.open({
                    type: 1,
                    area: ['1450px', '420px'],
                    skin: 'layui-layer-molv',
                    closeBtn: 1,
                    content: $('#popup')

                })
            });
            $("td[data-field='goods_standard']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html('<span style="font-weight: 500">' + result[0] + '</span><br><span>' + result[1] + '</span>')
                }
            })
            $("td[data-field='goods_time']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html('<i class="fahuo">发布</i>：<span style="">' + result[0] + '</span><br><i class="zhuanghuo">装货</i>：' + result[1])
                }
            })
            $("td[data-field='price']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html('<span>' + result[0] + '</span ></br>' + result[1] + '</span>')
                }
            })
              $("td[data-field='mobile']").children().each(function () {

                    var str = $(this).text();
                    if (str != '') {
                        str = str.split('\n');
                        if(str[0]==''){
                             $(this).html(str[0])
                        }else if(str[0]!=''&&str[1] == ''&&str[2] != '') {
                            $(this).html(str[0] +'<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ')</span>')
                        }else if(str[0]!=''&&str[1] != ''&&str[2] == '') {
                            $(this).html(str[0] +'<br>'+str[1])
                        }
                        else if(str[0] != '' && str[1] != '' && str[2] != '') {
                            $(this).html(str[0] + '<br>' + str[1] + '<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ')</span>')
                        }
                    }
                });
            $("td[data-field='address']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html(result[0] + '<br>' + result[1] + '<br>' + result[2])
                }
            })
          $("td[data-field='goods_type']").children().each(function () {
                    if ($(this).text() == '跨城定价') {
                        $(this).html('<span style="color: #01AAED;">跨城定价</span>')
                    }
                     if ($(this).text() == '跨城议价') {
                        $(this).html('<span style="color: #f40;">跨城议价</span>')
                    }
                    if ($(this).text() == '同城') {
                        $(this).html('<span style="color: green;">同城</span>')
                    }
                    if ($(this).text() == '零担') {
                        $(this).html('<span style="color: #393D49;">零担</span>')
                    }
                })
        }
        , id: 'goods_reload'
        , page: true
    });
    var $ = layui.$, active = {
        reload: function () {
            var demoReload = $('#demoReload');
            table.reload('goods_reload', {
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
    $('#goods_search_box').on('click', function (e) {
        e.preventDefault()
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
/*下面的是货源漏斗图，暂时先不做*/
var chart = Highcharts.chart('charts_container_one', {
    chart: {
        type: 'funnel',
        marginRight: 100
    },
    title: {
        text: '货源统计漏斗',
        x: -50
    },
    plotOptions: {
        series: {
            dataLabels: {
                enabled: true,
                crop: false,
                overflow: 'none',
                format: '<b>{point.name}</b> ({point.y:,.0f})',
                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
                softConnector: true
            },
            neckWidth: '0%',
            neckHeight: '0%'
        }
    },
    legend: {
        enabled: false
    },
    series: [{
        name: '用户',
        data: [
            ['潜在货源', 5654],
            ['实际货源', 4064],
            ['接单货源', 1987]
        ]
    }]
});
/*--------------下面是数据调用---------------*/
var dataSet = {
    charts_two_init: function () {
        var url = '/goods/goods_distribution_trend/';
        var requestStartTime = common.timeTransform($('#start_date_one').val() + ' 00:00:00');
        var requestEndTime = common.timeTransform($('#end_time_one').val() + ' 23:59:59');
        var data = {
            start_time: requestStartTime,
            end_time: requestEndTime,
            periods: $('.periods>li').find('button.active').val(),
            goods_type: $('#goods_type_one').val(),
            region_id: $('#region_id').val()==''?common.role_area_show($('#super_manager_area_select_zero')):$.trim($('#region_id').val()),
            goods_price_type:$('#goods_price_type').val(),
            payment_method:$('#pay_methods_statistics').val()
        }
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var data = res.data
                var len = res.data.xAxis.length;
                if (len > 0 && len < 20) {
                    Chart_twice(data.xAxis, data.wait_order_series, data.recv_order_series, data.cancel_order_series, data.goods_user_count_series, 1)
                } else if (len >= 20 && len < 50) {
                    Chart_twice(data.xAxis, data.wait_order_series, data.recv_order_series, data.cancel_order_series, data.goods_user_count_series, 3)
                } else if (len >= 50) {
                    Chart_twice(data.xAxis, data.wait_order_series, data.recv_order_series, data.cancel_order_series, data.goods_user_count_series, 5)
                }
            },function(){
                layer.closeAll('loading');
            })
        })
    },
    chart_third_init: function () {
        var url = '/jobs/jobs_pie/';
        var requestStartTime = common.timeTransform($('#start_date_three').val() + ' 00:00:00');
        var requestEndTime = common.timeTransform($('#end_time_three').val() + ' 23:59:59');
        var data = {
            search_name: $('#search_name').val(),
        };
        layui.use('layer', function () {
            var layer = layui.layer;
            /*左边表格部分*/
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var all_reason = res.data.job_list;
                if (res.data.job_list == '' && res.data.job_list_dict == '') {
                    var str = '<p style="color: #ccc; text-align: center; font-size: 24px;width: 400%;line-height: 40px;" >there is no data</p>';
                    Chart_third(all_reason, '该条件下无数据，图表无法展示');
                    $('#charts_container_four').css('height', '90px');
                    $('.cancel-reason-types').html(str)
                } else if (res.data.job_list != '' || res.data.job_list_dict != '') {
                    $('#charts_container_four').css('height', '400px');
                    Chart_third(all_reason, '职位数量统计');
                    var cancel_list_dict = res.data.job_list_dict;
                    var len = cancel_list_dict.length;
                    $('.cancel-reason-types').html('');
                    for (var i = 0; i < len; i++) {
                        var str = '';
                        str += '<tr>';
                        str += '<td>' + i + '</td>';
                        str += '<td class=" cancel-reason-name-"' + i + '>' + cancel_list_dict[i].region_name + '</td>';
                        str += '<td class="table-order-count cancel-reason-count-"' + i + '><span>' + cancel_list_dict[i].count + '个</span></td>';
                        str += '<th class=" cancel-reason-percentage-"' + i + '><span class="badge">' + cancel_list_dict[i].percentage + '</span></th>';
                        str += '<tr>';
                        $('.cancel-reason-types').append(str)
                    }
                     var string = '<tr class="cancel_reason_total"><td>职位总数：<span>'+res.data.sum_count+'个</span></td></tr>';
                    $('.cancel-reason-types').append(string)
                }
            },function(){
                layer.closeAll('loading')
            })
        })
    }
}
function Chart_twice(xAxis, wait_order_series, recv_order_series, cancel_order_series, goods_user_count_series, interval) {
Highcharts.setOptions({
    colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
});
    $('#charts_container_two').highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: '货源分布及发货人数趋势图'
        },
        subtitle: {
            text: null
        },
        xAxis: [{
            tickInterval: interval,
            categories: xAxis,
            crosshair: true,
            gridLineColor: '#eee',
            gridLineWidth: 1

        }],
        yAxis: [{
            labels: {
                format: '{value}人',
            },
            title: {
                text: '发货人数',
            }
        }, {
            title: {
                text: '订单统计',

            },
            labels: {
                format: '{value} 单',
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        lotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        plotOptions: {
            column: {
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        return this.point.y > 0 ? this.point.y + '单' : null;
                    }
                }
            },
            line: {
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        return this.point.y > 0 ? this.point.y + '人' : '';
                    }
                },
                tooltip: {valueSuffix: '%'},
                //曲线点类型："circle", "square", "diamond", "triangle","triangle-down"，默认是"circle"
                marker: {
                    radius: 5, symbol: 'circle'
                },
            }
        },
        series: [{
            name: '待接单',
            type: 'column',
            yAxis: 1,
            data: wait_order_series,
            tooltip: {
                valueSuffix: ' 单'
            }
        },
            {
                name: '已接单',
                type: 'column',
                yAxis: 1,
                data: recv_order_series,
                tooltip: {
                    valueSuffix: ' 单'
                }
            }, {
                name: '已取消',
                type: 'column',
                yAxis: 1,
                data: cancel_order_series,
                tooltip: {
                    valueSuffix: ' 单'
                }
            }, {
                name: '发货人数',
                type: 'line',
                data: goods_user_count_series,
                tooltip: {
                    valueSuffix: '人'
                }

            }]
    });

}

function Chart_third(dataArr, chartsTitle) {
    Highcharts.setOptions({
    colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
});
    $('#charts_container_four').highcharts({
        chart: {
            renderTo: 'chart'
        },
        title: {
            text: chartsTitle
        },
        plotArea: {
            shadow: true,
            borderWidth: true,
            backgroundColor: true
        },
        tooltip: {
            formatter: function () {
                return '<b>' + this.point.name + '</b>: ' + Highcharts.numberFormat(this.percentage, 1) + '% (' +
                    Highcharts.numberFormat(this.y, 0, ',') + ' 个)';
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        if (this.percentage > 4) return this.point.name;
                    },
                    color: 'black',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black',
                        font: '12px Trebuchet MS, Verdana, sans-serif'
                    }
                }
            }
        },
        legend: {
            //backgroundColor: '#FFFFFF',
            x: 0,
            y: -30
        },
        credits: {
            enabled: true
        },
        series: [{
            type: 'pie',
            name: '地区职位数量对比',
            data: dataArr
        }]
    });
}

$('#goods_search_box').on('click', function (e) {
    e.preventDefault();
    var create_start_time = $('#create_start_time').val();
    var create_end_time = $('#create_end_time').val();
    var register_start_time = $('#register_start_time').val();
    var register_end_time = $('#register_end_time').val();
    if (create_start_time != '') {
        create_start_time = common.timeTransform(create_start_time + ' 00:00:00')
    }
    if (create_end_time != '') {
        create_end_time = common.timeTransform(create_end_time + ' 23:59:59')
    }
    if (register_start_time != '') {
        register_start_time = common.timeTransform(register_start_time + ' 00:00:00')
    }
    if (register_end_time != '') {
        register_end_time = common.timeTransform(register_end_time + ' 23:59:59')
    }
    var data = {
        goods_id: $.trim($('#goods_id').val()),
        mobile: $.trim($('#mobile').val()),
        from_region_id: $.trim($('#reference_mobile').val()),
        to_region_id: $.trim($('#to_region_id').val()),
        goods_type: $.trim($('#goods_type').val()),
        goods_price_type:$.trim($('#goods_price_type3').val()),
        goods_status: $.trim($('#goods_status').val()),
        is_called: $.trim($('#is_called').val()),
        vehicle_length: $.trim($('#vehicle_length').val()),
        vehicle_type: $.trim($('#vehicle_type').val()),
        node_id: $.trim($('#node_id').val())==''?common.role_area_show($('#super_manager_area_select_two')):$.trim($('#node_id').val()),//10
        new_goods_type: $.trim($('#new_goods_type').val()),
        urgent_goods: $.trim($('#urgent_goods').val()),
        is_addition: $.trim($('#is_addition').val()),
        from_province_id: $('#from_region_id').attr('provinceid') == undefined ? '' : $('#from_region_id').attr('provinceid'),
        from_city_id: $('#from_region_id').attr('cityid') == undefined ? '' : $('#from_region_id').attr('cityid'),
        from_county_id: $('#from_region_id').attr('districtsid') == undefined ? '' : $('#from_region_id').attr('districtsid'),
        to_province_id: $('#to_region_id').attr('provinceid') == undefined ? '' : $('#to_region_id').attr('provinceid'),
        to_city_id: $('#to_region_id').attr('cityid') == undefined ? '' : $('#to_region_id').attr('cityid'),
        to_county_id: $('#to_region_id').attr('districtsid') == undefined ? '' : $('#to_region_id').attr('districtsid'),
        payment_method:$('#pay_methods').val(),
        create_start_time: create_start_time,
        create_end_time: create_end_time,
        register_start_time: register_start_time,
        register_end_time: register_end_time,//23
        page: 1,
        limit: 10
    }
    var url = '/goods/list/?goods_id=' + data.goods_id + '&mobile=' + data.mobile + '&from_province_id=' + data.from_province_id + '&from_city_id=' + data.from_city_id + '&from_county_id=' + data.from_county_id + '&to_province_id=' + data.to_province_id + '&to_city_id=' + data.to_city_id + '&to_county_id=' + data.to_county_id + '&goods_price_type=' +
        data.goods_price_type + '&goods_type=' +
        data.goods_type + '&goods_status=' + data.goods_status + '&is_called=' + data.is_called + '&vehicle_length=' + data.vehicle_length + '&vehicle_type=' + data.vehicle_type + '&node_id=' + data.node_id + '&new_goods_type=' + data.new_goods_type + '&urgent_goods=' + data.urgent_goods + '&is_addition=' + data.is_addition + '&payment_method=' + data.payment_method  + '&create_start_time=' + data.create_start_time + '&create_end_time=' + data.create_end_time + '&register_start_time=' + data.register_start_time + '&register_end_time=' + data.register_end_time;
    layui.use(['table', 'layer'], function () {
        var table = layui.table;
        var layer = layui.layer;
        layer.load()
        table.render({
            elem: '#LAY_table_goods',
            even: true
            , url: url,
            response: {
                statusName: 'status',
                statusCode: 100000
            },
            cols: [[
                {field: 'id', title: '货源ID', width: 60},
                {field: 'goods_standard', title: '货物规格', width: 86},
                {field: 'goods_type', title: '类型', width: 76},
                {field: 'address', title: '出发地-目的地', width: 300},
                {field: 'vehicle', title: '车型要求', width: 114},
                {field: 'price', title: '运费', width: 116},
                {field: 'mobile', title: '货主手机', width: 100},
                {field: 'goods_status', title: '状态', width: 86},
                {field: 'call_count', title: '通话数', width: 60},
                {field: 'latency_time', title: '初次触达', width: 80},
                {field: 'goods_time', title: '时间', width: 190},
                {field: 'node_id', title: '所属网点'}
            ]],
            done: function (res, curr, count) {
                layer.closeAll('loading');
                console.log(res);
                $('[data-field]>div').css({'padding': '0 6px'});
                $('.nearby').on('click', function () {
                    layer.open({
                        type: 1,
                        area: ['1620px', '520px'],
                        skin: 'layui-layer-molv',
                        closeBtn: 1,
                        content: $('#popup')
                    })
                });
                $("td[data-field='goods_time']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html('<i class="fahuo">发布</i>：<span style="">' + result[0] + '</span><br><i class="zhuanghuo">装货</i>：' + result[1])
                    }
                })
                $("td[data-field='price']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html('<span>' + result[0] + '<br>' + result[1] + '</span >');
                    }
                })
                $("td[data-field='mobile']").children().each(function () {
                    var str = $(this).text();
                    if (str != '') {
                        str = str.split('\n');
                        if(str[0]==''){
                             $(this).html(str[0])
                        }else if(str[0]!=''&&str[1] == ''&&str[2] != '') {
                            $(this).html(str[0] +'<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ')</span>')
                        }
                        else if(str[0] != '' && str[1] != '' && str[2] != '') {
                            $(this).html(str[0] + '<br>' + str[1] + '<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ')</span>')
                        }
                    }
                });
                $("td[data-field='address']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html(result[0] + '<br>' + result[1] + '<br>' + result[2])
                    }
                })
                  $("td[data-field='goods_type']").children().each(function () {
                    if ($(this).text() == '跨城定价') {
                        $(this).html('<span style="color: #01AAED;">跨城定价</span>')
                    }
                     if ($(this).text() == '跨城议价') {
                        $(this).html('<span style="color: #f40;">跨城议价</span>')
                    }
                    if ($(this).text() == '同城') {
                        $(this).html('<span style="color: green;">同城</span>')
                    }
                    if ($(this).text() == '零担') {
                        $(this).html('<span style="color: #393D49;">零担</span>')
                    }
                })
            }
            , id: 'goods_reload'
            , page: true
        });
    })
});
$('#searchBox').on('click', function (e) {
    e.preventDefault();
    dataSet.charts_two_init()
})
$('#searchBox_3').on('click', function (e) {
    e.preventDefault();
    dataSet.chart_third_init()
})
function area_select() {
    var auth_role = $('#user-info').attr('data-role-type')
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
         $('#super_manager_area_two').css({'display': 'block'})
        $('#super_manager_area_select_two').address({
            level: 3,
             offsetLeft: '-124px',
        });
    } else {
        $('#super_manager_area').css({'display': 'none'})
        $('#super_manager_area_one').css({'display': 'none'})
        $('#super_manager_area_two').css({'display': 'none'})
        $('#city_manager_one').css({'display': 'block'})
        $('#city_manager_two').css({'display': 'block'})
    $('#city_manager_three').css({'display': 'block'})
    }
}
area_select()
dataSet.charts_two_init();
dataSet.chart_third_init();
