
var setAbout = {
    init: function () {
        /*给表单设置默认值，时间转换秒是前端做的*/
        $('.layui-table-cell').css({'height': 'auto!important'});
        $('#active_start').val(String(common.getNowFormatDate()[2]));
        $('#active_end').val(String(common.getNowFormatDate()[0]));
        $('#survival_start').val(String(common.getNowFormatDate()[2]));
        $('#survival_end').val(String(common.getNowFormatDate()[3]));
        setTimeout(function () {
            common.dateInterval($('#active_start').val(), $('#active_start').val());
             /*设置左边二级菜单样式*/
                var current_parent_id='users'//当前页面上一级ID，指目录名
                var child_id="active-retain";//当前页面ID，指文件名,注意'-'与'_'的区别
            // 为啥要这样搞？总之锅laitx不背，laitx负责改得更容易操作而已哈哈 可以考虑自动获取url文件名，就不需要管这块儿了。
                $('.menu-'+current_parent_id).addClass('menu-active');
                $('.menu-active .icon-xia').addClass('icon-rotate')
                $('.menu-'+current_parent_id).next('.second-menu-list').css({'display': 'block'});
                $('.menu-'+current_parent_id).next('.second-menu-list').find('.'+child_id+'-second-menu').addClass('selected-active')
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
                elem: '#active_start',
                theme: '#009688',
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#active_start').val();
                    var endTime = $('#active_end').val();
                    common.dateInterval(endTime, startTime);
                    if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false
                    }
                    if ($('#active_start').val() == '') {
                        $('#active_start').next('.date-tips').show();
                    } else {
                        $('#active_start').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#active_end',
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#active_start').val();
                    var endTime = $('#active_end').val();
                    common.dateInterval(endTime, startTime);
                    if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false
                    }
                    if ($('#active_end').val() == '') {
                        $('#active_end').next('.date-tips').show();
                    } else {
                        $('#active_end').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#survival_start',
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#survival_start').val();
                    var endTime = $('#survival_end').val();
                    if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false
                    }
                    if ($('#survival_start').val() == '') {
                        $('#survival_start').next('.date-tips').show();
                    } else {
                        $('#survival_start').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#survival_end',
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#survival_start').val();
                    var endTime = $('#survival_end').val();
                    if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false
                    }
                    if ($('#survival_end').val() == '') {
                        $('#survival_end').next('.date-tips').show();
                    } else {
                        $('#survival_end').next('.date-tips').hide()
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
                elem: '#active_survival_table',
                even: true
                , url: url,
                response: {
                    statusName: 'status',
                    statusCode: 100000
                },
                cols: [[
                    {field: 'goods_standard', title: '时间'},
                    {field: 'goods_type', title: '用户数'},
                    {field: 'address', title: '一天', width: 250},
                    {field: 'vehicle', title: '两天'},
                    {field: 'price', title: '三天'},
                    {field:'query_time',title:'四天'},
                    {field:'stay_time',title:'五天'},
                    {field: 'mobile', title: '六天'},
                    {field: 'goods_counts', title: '七天'},
                    {field: 'orders_counts', title: '八天'}
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
        var start_time = $('#active_start').val();
        var end_time = $('#active_end').val();
        var periods = $('.active_periods>li').find('button.active').val();
        if (start_time != '') {
            start_time = common.timeTransform(start_time + ' 00:00:00')
        }
        if (end_time != '') {
            end_time = common.timeTransform(end_time + ' 23:59:59')
        }
        var data = {
            region_id: '',
            start_time: start_time,
            end_time: end_time,
            periods: periods,
            haul_dist:'',
            business: '',
            goods_price_type: ''
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
        $('#active_charts').highcharts({
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
                text: '活跃用户趋势折线图'
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
                    text: '',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value}天',
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
                            return this.point.y>0? this.point.y + '人':'';
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
                name: '活跃用户',
                type: 'line',
                tooltip: {
                    valueSuffix: '人'
                },
                data: series
            }]
        });
    },
    area_select: function () {
        var auth_role = $('#user-info').attr('data-role-type');
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
    var url = '/potential/list/?from_province_id=' + data.from_province_id + '&from_city_id=' + data.from_city_id + '&from_county_id=' + data.from_county_id + '&to_province_id=' + data.to_province_id + '&to_city_id=' + data.to_city_id + '&to_county_id=' + data.to_county_id + '&goods_price_type=' + data.goods_price_type + '&business=' + data.business + '&haul_dist=' + data.haul_dist + '&vehicle_name=' + data.vehicle_name + '&special_tag=' + data.special_tag + '&register_start_time=' + data.register_start_time + '&register_end_time=' + data.register_end_time + '&record_start_time=' + data.record_start_time + '&record_end_time=' + data.record_end_time;
    setAbout.tableSet(url)
});
$('#search_btn').click(function (e) {
    e.preventDefault();
    setAbout.chartRender();
});