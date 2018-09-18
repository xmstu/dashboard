/**
 * Created by Creazy_Run on 2018/5/30.
 */
var setAbout = {
    init: function () {
        /*侧边栏样式*/
          $('.menu-transaction').addClass('menu-active');
          $('.menu-transaction').next('.second-menu-list').css({'display': 'block'});
          $('.menu-transaction').next('.second-menu-list').find('.lurk-goods').addClass('selected-active');
        /*给表单设置默认值，时间转换秒是前端做的*/
        $('.layui-table-cell').css({'height': 'auto!important'});
        $('#date_show_one').val(String(common.getNowFormatDate()[2]));
        $('#date_show_two').val(String(common.getNowFormatDate()[3]));
        $('#start_date_one').val(String(common.getNowFormatDate()[2]));
        $('#end_time_one').val(String(common.getNowFormatDate()[3]));
        setTimeout(function () {
            common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
        }, 10);
        $('.layui-form-item').width('184');
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
    },
    layui: function () {
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
                elem: '#create_start_time',
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#create_start_time').val();
                    var endTime = $('#create_end_time').val();
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
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#create_start_time').val();
                    var endTime = $('#create_end_time').val();
                    if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false
                    }
                    if ($('#create_end_time').val() == '') {
                        $('#create_end_time').next('.date-tips').show();
                    } else {
                        $('#create_end_time').next('.date-tips').hide()
                    }

                }
            });
            laydate.render({
                elem: '#record_start_time',
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#record_start_time').val();
                    var endTime = $('#record_end_time').val();
                    if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false
                    }
                    if ($('#record_start_time').val() == '') {
                        $('#record_start_time').next('.date-tips').show();
                    } else {
                        $('#record_start_time').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#record_end_time',
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#record_start_time').val();
                    var endTime = $('#record_end_time').val();
                    if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false
                    }
                    if ($('#record_end_time').val() == '') {
                        $('#record_end_time').next('.date-tips').show();
                    } else {
                        $('#record_end_time').next('.date-tips').hide()
                    }
                }
            });
        });
    },
    tableSet: function (url) {
        layui.use('table', function () {
            var table = layui.table;
            table.render({
                elem: '#LAY_table_goods',
                even: true
                , url: url,
                response: {
                    statusName: 'status',
                    statusCode: 100000
                },
                cols: [[
                    {field: 'goods_standard', title: '货物规格'},
                    {field: 'goods_type', title: '货物类型'},
                    {field: 'address', title: '出发地-目的地', width: 300},
                    {field: 'vehicle', title: '车型要求'},
                    {field: 'price', title: '运费'},
                    {field:'query_time',title:'查价时间'},
                    {field:'stay_time',title:'查价时长'},
                    {field: 'mobile', title: '用户信息'},
                    {field: 'goods_counts', title: '发货数'},
                    {field: 'orders_counts', title: '完成数'},
                    {field: 'register_time', title: '注册时间'}
                ]],
                done: function (res, curr, count) {
                    $("td[data-field='mobile']").children().each(function () {
                        var str = $(this).text();
                        if (str != '') {
                            str = str.split('\n');
                            if (str[0] == '') {
                                $(this).html(str[0])
                            } else if (str[0] != '' && str[1] == '' && str[2] != '') {
                                $(this).html(str[0] + '<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ')</span>')
                            } else if (str[0] != '' && str[1] != '' && str[2] == '') {
                                $(this).html(str[0] + '<br>' + str[1])
                            }
                            else if (str[0] != '' && str[1] != '' && str[2] != '') {
                                $(this).html(str[0] + '<br>' + str[1] + '<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ')</span>')
                            }
                        }
                    });
                    $("td[data-field='goods_type']").children().each(function () {
                        var str = $(this).text();
                        if (str != '') {
                            str = str.split('\n');
                            console.log(str.length);
                            if (str.length > 1) {
                                $(this).html(str[0] + str[1])
                            } else {
                                $(this).html(str[0])
                            }
                        }
                    });
                    $("td[data-field='address']").children().each(function (val) {
                        if ($(this).text() != '') {
                            var result = $(this).text().split('\n');
                            $(this).html(result[0] + '<br>' + result[1] + '<br>' + result[2])
                        }
                    })
                }
                , id: 'goods_reload'
                , page: true
            });
        })
    },
    chartRender: function () {
        var _this = this;
        var start_time = $('#date_show_one').val();
        var end_time = $('#date_show_two').val();
        var periods = $('.periods>li').find('button.active').val();
        if (start_time != '') {
            start_time = common.timeTransform(start_time + ' 00:00:00')
        }
        if (end_time != '') {
            end_time = common.timeTransform(end_time + ' 23:59:59')
        }
        var data = {
            region_id: $.trim($('#region_id_show').val()) == '' ? common.role_area_show($('#super_manager_area_select_zero')) : $.trim($('#region_id_show').val()),
            start_time: start_time,
            end_time: end_time,
            periods: periods,
            haul_dist: $('#haul_dist').val(),
            business: $('#business').val(),
            goods_price_type: $('#goods_price_type').val()
        };
        var url = '/potential/trend/';
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                if (res.status == 100000) {
                    var len = res.data.xAxis.length;
                    var X_data = res.data.xAxis;
                    if (len > 0 && len < 20) {
                        _this.chartInit(res.data.xAxis, res.data.series, 1, X_data[1])
                    } else if (len > 0 && len >= 20 && len < 40) {
                        _this.chartInit(res.data.xAxis, res.data.series, 3, X_data[1])
                    } else if (len > 0 && len >= 40 && len < 90) {
                        _this.chartInit(res.data.xAxis, res.data.series, 5, X_data[1])
                    }
                    layer.closeAll('loading')
                }
            })
        })

    },
    tableRender: function () {
        var _this = this;
        var url = '/potential/list/';
        _this.tableSet(url)
    },
    chartInit: function (xAxis, series, interval, x_value1) {
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
                text: '潜在货源趋势曲线图'
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
                min: 0,
                allowDecimals: false,
                plotLines: [
                    {
                        color: '#ddd',
                        dashStyle: 'dash',
                        value: x_value1,
                        width: 1
                    }
                ],
                title: {
                    text: '潜在货源 (单)',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value}单',
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
                            return this.point.y + '单';
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
                name: '潜在货源',
                type: 'line',
                tooltip: {
                    valueSuffix: '单'
                },
                data: series
            }]
        });
    },
    area_select: function () {
        var auth_role = $('#user-info').attr('data-role');
        if (!!auth_role && auth_role == 1) {
            $('#super_manager_area').css({'display': 'block'});
            $('#super_manager_area_select_zero').address({
                level: 3,
                offsetLeft: '-124px',
            });
        } else {
            $('#super_manager_area').css({'display': 'none'});
            $('#city_manager_one').css({'display': 'block'});
        }
    }

};
setAbout.init();
setAbout.layui();
setAbout.area_select();
setAbout.chartRender();
setAbout.tableRender();
$('#goods_search_box').click(function (e) {
    e.preventDefault();
    var register_start_time = $('#create_start_time').val();
    var register_end_time = $('#create_end_time').val();
    var record_start_time = $('#record_start_time').val();
    var record_end_time = $('#record_end_time').val();
    if (register_start_time != '') {
        register_start_time = common.timeTransform(register_start_time + ' 00:00:00')
    }
    if (register_end_time != '') {
        register_end_time = common.timeTransform(register_end_time + ' 23:59:59')
    }
    if (record_start_time != '') {
        record_start_time = common.timeTransform(record_start_time + ' 00:00:00')
    }
    if (record_end_time != '') {
        record_end_time = common.timeTransform(record_end_time + ' 23:59:59')
    }
    var data = {
        from_province_id: $('#from_region_id').attr('provinceid') == undefined ? '' : $('#from_region_id').attr('provinceid'),
        from_city_id: $('#from_region_id').attr('cityid') == undefined ? '' : $('#from_region_id').attr('cityid'),
        from_county_id: $('#from_region_id').attr('districtsid') == undefined ? '' : $('#from_region_id').attr('districtsid'),
        to_province_id: $('#to_region_id').attr('provinceid') == undefined ? '' : $('#to_region_id').attr('provinceid'),
        to_city_id: $('#to_region_id').attr('cityid') == undefined ? '' : $('#to_region_id').attr('cityid'),
        to_county_id: $('#to_region_id').attr('districtsid') == undefined ? '' : $('#to_region_id').attr('districtsid'),
        goods_price_type: $('#goods_type_first').val(),
        business: $('#business_type').val(),
        haul_dist: $('#haul_dist_table').val(),
        vehicle_name: $('#vehicle_name').val(),
        special_tag: $('#special_tag').val(),
        register_start_time: register_start_time,
        register_end_time: register_end_time,
        record_start_time: record_start_time,
        record_end_time: record_end_time
    };
    console.log($('#haul_dist_table').val());
    console.log('test:'+data.haul_dist)
    var url = '/potential/list/?from_province_id=' + data.from_province_id + '&from_city_id=' + data.from_city_id + '&from_county_id=' + data.from_county_id + '&to_province_id=' + data.to_province_id + '&to_city_id=' + data.to_city_id + '&to_county_id=' + data.to_county_id + '&goods_price_type=' + data.goods_price_type + '&business=' + data.business + '&haul_dist=' + data.haul_dist + '&vehicle_name=' + data.vehicle_name + '&special_tag=' + data.special_tag + '&register_start_time=' + data.register_start_time + '&register_end_time=' + data.register_end_time + '&record_start_time=' + data.record_start_time + '&record_end_time=' + data.record_end_time;
    setAbout.tableSet(url)
});
$('#search_btn').click(function (e) {
    e.preventDefault();
    setAbout.chartRender();
});