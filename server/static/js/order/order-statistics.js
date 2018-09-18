/**
 * Created by Creazy_Run on 2018/5/30.
 */
$('.layui-table-cell').css({'height': 'auto!important'});
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
$('#start_date_one').val(String(common.getNowFormatDate()[2]));
$('#end_time_one').val(String(common.getNowFormatDate()[3]));
setTimeout(function () {
    $('.menu-transaction').addClass('menu-active');
    $('.menu-transaction').next('.second-menu-list').css({'display': 'block'});
    $('.menu-transaction').next('.second-menu-list').find('.order-second-menu').addClass('selected-active');
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 10);

function init() {
    $('.part-2 .layui-input-inline').width(102);
    $('.part-2 .layui-inline').addClass('mr4');
    $('.layui-form-item').width(184);
    $('.part-1-top .layui-form-item').css({width: 182});
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
    /*二级*/
    $('.menu-transaction').addClass('menu-active');
    $('.menu-transaction').next('.second-menu-list').css({'display': 'block'});
    $('.menu-transaction').next('.second-menu-list').find('li:nth-of-type(2)').find('a').addClass('selected-active')
}

layui.use(['laydate', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    laydate.render({
        elem: '#date_show_one',
        theme: '#009688',
        calendar: true,
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#date_show_one').val() == '') {
                $('#date_show_one').next('.date-tips').show();
            } else {
                $('#date_show_one').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#date_show_two').val() == '') {
                $('#date_show_two').next('.date-tips').show();
            } else {
                $('#date_show_two').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#start_date_one',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
        format: 'yyyy/MM/dd',
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
        format: 'yyyy/MM/dd',
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
        elem: '#create_start_time',
        theme: '#009688',
        max: String(common.getNowFormatDate()[0]),
        calendar: true,
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#create_start_time').val();
            var endTime = $('#create_end_time').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
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
        max: String(common.getNowFormatDate()[0]),
        calendar: true,
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#create_start_time').val();
            var endTime = $('#create_end_time').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#create_end_time').val() == '') {
                $('#create_end_time').next('.date-tips').show();
            } else {
                $('#create_end_time').next('.date-tips').hide()
            }
            if (val != '') {
                $('#create_end_time').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#load_start_time',
        theme: '#009688',
        max: String(common.getNowFormatDate()[0]),
        calendar: true,
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#load_start_time').val();
            var endTime = $('#load_end_time').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#load_start_time').val() == '') {
                $('#load_start_time').next('.date-tips').show();
            } else {
                $('#load_start_time').next('.date-tips').hide()
            }
            if (val != '') {
                $('#load_start_time').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#load_end_time',
        theme: '#009688',
        max: String(common.getNowFormatDate()[0]),
        calendar: true,
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#load_start_time').val();
            var endTime = $('#load_end_time').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#load_end_time').val() == '') {
                $('#load_end_time').next('.date-tips').show();
            } else {
                $('#load_end_time').next('.date-tips').hide()
            }
            if (val != '') {
                $('#load_end_time').next('.date-tips').hide()
            }
        }
    });
});
Highcharts.setOptions({
    colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
});
var setAbout = {
    that: this,
    chartRender: function (xAxis, complete_series, pending_series, cancel_series, interval, unit, title) {
        $('#charts_container_one').highcharts({
            chart: {
                type: 'area'
            },
            title: {
                text: title
            },
            subtitle: {
                text: null
            },
            xAxis: {
                tickInterval: interval,
                categories: xAxis,
                tickmarkPlacement: 'on',
                title: {
                    enabled: true
                }
            },
            yAxis: {
                title: {
                    text: title
                },
                labels: {
                    formatter: function () {
                        return this.value + unit;
                    }
                }
            },
            tooltip: {
                split: true,
                valueSuffix: unit,
                backgroundColor: '#FFF'
            },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#eee',
                    lineWidth: 1,
                    marker: {
                        radius: 2.5,
                        lineWidth: 1,
                        lineColor: '#666666',
                        fillColor: '#fff',
                        symbol: 'circle',
                        states: {
                            hover: {
                                enabled: true,
                                radius: 3
                            }
                        }
                    },
                    dataLabels: {
                        enabled: false
                    }
                }
            },
            series: [{
                name: '已完成',
                data: complete_series
            }, {
                name: '进行中',
                data: pending_series
            }, {
                name: '已取消',
                data: cancel_series
            }]

        });
    },
    chartShow: function (dataArr, title) {
        $('#charts_container_two').highcharts({
            chart: {
                renderTo: 'chart',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: title
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
                        style: {
                            font: '12px Trebuchet MS, Verdana, sans-serif'
                        }
                    }
                }
            },
            legend: {
                backgroundColor: '#FFFFFF',
                x: 0,
                y: -30
            },
            credits: {
                enabled: false
            },
            series: [{
                type: 'pie',
                name: 'Browser share',
                data: dataArr
            }]
        });
        chart = $('#charts_container_two').highcharts();
    },
    chartInit: function () {
        var that = this;
        var requestStart = common.timeTransform($('#start_date_one').val() + ' 00:00:00');
        var requestEnd = common.timeTransform($('#end_time_one').val() + ' 23:59:59');
        var url = '/order/cancel_reason/';
        var data = {
            start_time: requestStart,
            end_time: requestEnd,
            goods_type: $('#cancel_reason_types').val(),
            goods_price_type: $('#goods_price_type1').val(),
            cancel_type: $('#cancel_reason_roles').val(),
            region_id: $('#cancel_reason_area').val() == '' ? common.role_area_show($('#super_manager_area_select_one')) : $.trim($('#cancel_reason_area').val())
        };
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var cancel_list = res.data.cancel_list;
                var cancel_list_dict = res.data.cancel_list_dict;
                var len = cancel_list_dict.length;
                var str = '';
                if (cancel_list.length == 0) {
                    str += '<span class="table-no-data">there is no data</span>';
                    $('.cancel-reason-types').html('').append(str);
                    $('#charts_container_two').height('90px');
                    console.log($('.highcharts-container').height());
                    that.chartShow(cancel_list, '图表无法显示，因该条件下无数据')
                } else if (cancel_list.length > 0) {
                    $('#charts_container_two').height('400px');
                    that.chartShow(cancel_list, '取消原因统计表');
                    $('.cancel-reason-types').html('');
                    for (var i = 0; i < len; i++) {
                        str += '<tr>';
                        str += '<td>' + i + '</td>';
                        str += '<td class="cancel-reason-name-"' + i + '>' + cancel_list_dict[i].canceled_reason_text + '</td>';
                        str += '<td class="table-order-count cancel-reason-count-"' + i + '><span>' + cancel_list_dict[i].reason_count + '单</span></td>';
                        str += '<th class="cancel-reason-percentage-"' + i + '><span class="badge">' + cancel_list_dict[i].percentage + '</span></th>';
                        str += '<tr>'
                        $('.cancel-reason-types').html('').append(str)
                    }
                    var string = '<tr class="cancel_reason_total"><td>取消总数：<span>' + res.data.sum_count + '单</span></td></tr>';
                    $('.cancel-reason-types').append(string)
                }
            })
        })

    },
    chartRequest: function () {
        var that = this;
        var requestStart = common.timeTransform($('#date_show_one').val() + ' 00:00:00');
        var requestEnd = common.timeTransform($('#date_show_two').val() + ' 23:59:59');
        var url = '/order/statistics/';
        var data = {
            start_time: requestStart,
            end_time: requestEnd,
            periods: $('.periods>li').find('button.active').val(),
            goods_price_type: $('#goods_price_type').val(),
            goods_type: $('#goods_type_show').val(),
            dimension: $('#dimension').val(),
            region_id: $.trim($('#region_id_show').val()) == '' ? common.role_area_show($('#super_manager_area_select_zero')) : $.trim($('#region_id_show').val()),
            comment_type: $('#comment_type').val(),
            pay_method: $('#pay_method').val(),
            SXB: $("#CHART_SXB").val()
        };
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var cancel_list_date = res.data.xAxis;
                var len = cancel_list_date.length;
                var complete_series = res.data.complete_series;
                var cancel_series = res.data.cancel_series;
                var pending_series = res.data.pending_series;
                var value = data.dimension;
                if (value == 1) {
                    if (len > 0 && len < 20) {
                        that.chartRender(cancel_list_date, complete_series, pending_series, cancel_series, 1, '单', '订单汇总')
                    } else if (len >= 20 && len < 50) {
                        that.chartRender(cancel_list_date, complete_series, pending_series, cancel_series, 3, '单', '订单汇总')
                    } else if (len >= 50) {
                        that.chartRender(cancel_list_date, complete_series, pending_series, cancel_series, 5, '单', '订单汇总')
                    }
                } else if (value == 2) {
                    if (len > 0 && len < 20) {
                        that.chartRender(cancel_list_date, complete_series, pending_series, cancel_series, 1, '元', '金额汇总')
                    } else if (len >= 20 && len < 50) {
                        that.chartRender(cancel_list_date, complete_series, pending_series, cancel_series, 3, '元', '金额汇总')
                    } else if (len >= 50) {
                        that.chartRender(cancel_list_date, complete_series, pending_series, cancel_series, 5, '元', '金额汇总')
                    }
                }

            })
        })
    },
    tableRender: function (url) {
        layui.use(['layer', 'table'], function () {
            var layer = layui.layer;
            var table = layui.table;
            layer.load();
            table.render({
                elem: '#LAY_table_goods',
                even: true
                , url: url,
                response: {
                    statusName: 'status',
                    statusCode: 100000
                },
                cols: [[
                    {field: 'order_id', title: '订单ID', width: 60},
                    {field: 'goods_standard', title: '货物规格', width: 70},
                    {field: 'goods_type', title: '类型', width: 80},
                    {field: 'address', title: '出发地-目的地', width: 260},
                    {field: 'vehicle', title: '车型要求', width: 76},
                    {field: 'freight', title: '运费', width: 80},
                    {field: 'cargo_owner', title: '货主', width: 96},
                    {field: 'driver', title: '司机', width: 94},
                    {field: 'latency_time', title: '接单时间', width: 90},
                    {field: 'order_status', title: '状态', width: 80},
                    {field: 'time_field', title: '时间', width: 180},
                    {field: 'evaluation', title: '互评', width: 92},
                    {field: 'comment', title: '互评内容'}
                ]],
                done: function (res, curr, count) {
                    $('[data-field]>div').css({'padding': '0 6px'});
                    layer.closeAll('loading');
                    $('.main-content-right').addClass('animated fadeIn');
                    $("td[data-field='goods_standard']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            $(this).html(result[0] + '<br>' + result[1] + '</span>')
                        }
                    });
                    $("td[data-field='goods_time']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            $(this).html('<i class="iconfont icon-fabu mr-4"  title="发布时间" style="font-weight: 500;color: deepskyblue;"></i><span style="">' + result[0] + '</span><br><i style="font-weight: 500;color: deepskyblue;" class="mr-4 iconfont icon-huowu1" title="装货时间"></i><span>' + result[1])
                        }
                    });
                    $("td[data-field='time_field']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            $(this).html('<i class="zhuanghuo">接单</i>：' + result[1] + '<br><i class="fahuo">完成</i>：<span style="">' + result[0] + '</span>')
                        }
                    });
                    $("td[data-field='order_status']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            $(this).html(result[1] + '<br>' + result[0])
                        }
                    });
                    $("td[data-field='evaluation']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            $(this).html('<span style="">司机:' + result[0] + '</span><br><span style="">货主:' + result[1] + '</span>')
                        }
                    });
                    $("td[data-field='comment']").children().each(function (val) {
                        if ($(this).text().length >= 2) {
                            var result = $(this).text().split('\n');
                            $(this).html('<span style="">司机:' + result[0] + '</span><br><span style="">货主:' + result[1] + '</span>')
                        } else if ($(this).text().length < 2) {
                            $(this).html('<span style="">司机:该司机未对货主进行评价</span><br><span style="">货主:该货主未对司机进行评价</span>')
                        }
                    });
                    $("td[data-field='driver']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            if (result[0] != '' && result[1] != '') {
                                $(this).html('<span>' + result[0] + '</span ><br><span>' + result[1] + '</span>')
                            }
                            if (result[0] != '' && result[1] != '' && result[2] != '') {
                                $(this).html('<span>' + result[0] + '</span ><br><span>' + result[1] + '</span><br><span style="color: red">(' + result[2] + ')</span>')
                            }
                            if (result[0] != '' && result[1] == '' && result[2] != '') {
                                $(this).html('<span>' + result[0] + '</span ><br><span style="color: #f40;">' + result[2] + '</span>')
                            }
                        }
                    })
                    $("td[data-field='cargo_owner']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            if (result[0] != '' && result[1] != '') {
                                $(this).html('<span>' + result[0] + '</span ><br><span>' + result[1] + '</span>')
                            }
                            if (result[0] != '' && result[1] != '' && result[2] != '') {
                                $(this).html('<span>' + result[0] + '</span ><br><span>' + result[1] + '</span><br><span style="color: red">(' + result[2] + ')</span>')
                            }
                            if (result[0] != '' && result[1] == '' && result[2] != '') {
                                $(this).html('<span>' + result[0] + '</span ><br><span style="color: #f40;">' + result[2] + '</span>')
                            }
                        }
                    });
                    $("td[data-field='vehicle']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            if (result[0] !== '') {
                                $(this).html(result[0])
                            }
                            if (result[1] != '' && result[1] != undefined) {
                                $(this).html(result[0] + '<br>' + result[1])
                            }
                            if (result[2] != '' && result[2] != undefined) {
                                $(this).html(result[0] + '<br>' + result[1])
                            }
                        }
                    });

                    $("td[data-field='address']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            $(this).html(result[0] + '<br>' + result[1] + '<br>' + result[2])
                        }
                    });
                    common.clearSelect()
                }
                , id: 'order_reload'
                , page: true
            });
        })
    }
};

$('#goods_search_box').on('click', function (e) {
    e.preventDefault();
    layui.use(['layer', 'table'], function () {
        var create_start_time = $('#create_start_time').val();
        var create_end_time = $('#create_end_time').val();
        var load_start_time = $('#load_start_time').val();
        var load_end_time = $('#load_end_time').val();
        if (create_start_time != '') {
            create_start_time = common.timeTransform(create_start_time + ' 00:00:00')
        }
        if (create_end_time != '') {
            create_end_time = common.timeTransform(create_end_time + ' 23:59:59')
        }
        if (load_start_time != '') {
            load_start_time = common.timeTransform(load_start_time + ' 00:00:00')
        }
        if (load_end_time != '') {
            load_end_time = common.timeTransform(load_end_time + ' 23:59:59')
        }
        if (load_start_time != '' && load_end_time == '') {
            load_end_time = common.currentTime();
        }
        if (load_start_time == '' && load_end_time != '') {
            layer.tips('请输入开始日期！', '#load_start_time', {
                tips: [1, '#009688'],
                time: 3000
            });
            return false;
        }
        var data = {
            order_id: $.trim($('#order_id').val()),
            consignor_mobile: $.trim($('#consignor_mobile').val()),
            driver_mobile: $.trim($('#driver_mobile').val()),
            order_price_type: $.trim($('#order_price_type').val()),
            order_type: $.trim($('#order_type').val()),
            order_status: $.trim($('#order_status').val()),
            vehicle_length: $.trim($('#vehicle_length').val()),
            vehicle_type: $.trim($('#vehicle_type').val()),
            node_id: $.trim($('#node_id').val()) == '' ? common.role_area_show($('#super_manager_area_select_two')) : $.trim($('#node_id').val()),//10
            spec_tag: $.trim($('#spec_tag').val()),
            pay_status: $.trim($('#pay_status').val()),
            is_change_price: $.trim($('#is_change_price').val()),
            comment_type: $.trim($('#comment_type_one').val()),
            from_province_id: $('#from_region_id').attr('provinceid') == undefined ? '' : $('#from_region_id').attr('provinceid'),
            from_city_id: $('#from_region_id').attr('cityid') == undefined ? '' : $('#from_region_id').attr('cityid'),
            from_county_id: $('#from_region_id').attr('districtsid') == undefined ? '' : $('#from_region_id').attr('districtsid'),
            to_province_id: $('#to_region_id').attr('provinceid') == undefined ? '' : $('#to_region_id').attr('provinceid'),
            to_city_id: $('#to_region_id').attr('cityid') == undefined ? '' : $('#to_region_id').attr('cityid'),
            to_county_id: $('#to_region_id').attr('districtsid') == undefined ? '' : $('#to_region_id').attr('districtsid'),
            SXB: $('#TABLE_SXB').val(),
            start_order_time: create_start_time,
            end_order_time: create_end_time,
            start_complete_time: load_start_time,
            end_complete_time: load_end_time
        };
        var url = '/order/list/?order_id=' + data.order_id + '&consignor_mobile=' + data.consignor_mobile + '&driver_mobile=' + data.driver_mobile + '&from_province_id=' + data.from_province_id + '&from_city_id=' + data.from_city_id + '&from_county_id=' + data.from_county_id + '&to_province_id=' + data.to_province_id + '&to_city_id=' + data.to_city_id + '&to_county_id=' + data.to_county_id + '&order_price_type=' +
            data.order_price_type + '&order_type=' +
            data.order_type + '&order_status=' + data.order_status + '&vehicle_length=' + data.vehicle_length + '&vehicle_type=' + data.vehicle_type + '&spec_tag=' + data.spec_tag + '&node_id=' + data.node_id + '&is_change_price=' + data.is_change_price + '&pay_status=' + data.pay_status + '&comment_type=' + data.comment_type + '&SXB=' + data.SXB + '&start_order_time=' + data.start_order_time + '&end_order_time=' + data.end_order_time + '&start_complete_time=' + data.start_complete_time + '&end_complete_time=' + data.end_complete_time;
        setAbout.tableRender(url)
    });
});

function area_select() {
    var auth_role = $('#user-info').attr('data-role')
    if (!!auth_role && auth_role == 1) {
        $('#super_manager_area').css({'display': 'block'})
        $('#super_manager_area_select_zero').address({
            level: 3,
            offsetLeft: '-124px'
        });
        $('#super_manager_area_one').css({'display': 'block'})
        $('#super_manager_area_select_one').address({
            level: 3,
            offsetLeft: '-124px'
        });
        $('#super_manager_area_two').css({'display': 'block'})
        $('#super_manager_area_select_two').address({
            level: 3,
            offsetLeft: '-124px'
        });
    } else {
        $('#super_manager_area').css({'display': 'none'});
        $('#super_manager_area_one').css({'display': 'none'});
        $('#super_manager_area_two').css({'display': 'none'});
        $('#city_manager_one').css({'display': 'block'});
        $('#city_manager_two').css({'display': 'block'});
        $('#city_manager_three').css({'display': 'block'})
    }
}

area_select()
$('#searchBox_3').on('click', function (e) {
    e.preventDefault();
    setAbout.chartInit()
});
$('#search_btn').on('click', function (e) {
    e.preventDefault();
    setAbout.chartRequest();
})
setAbout.chartInit();
setAbout.chartRequest();
setAbout.tableRender('/order/list/');