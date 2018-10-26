var setAbout = {
    survival_url: "/active_retain/list/",
    active_url: '/active_retain/statistic/',
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
            var current_parent_id = 'users'//当前页面上一级ID，指目录名
            var child_id = "active-retain";//当前页面ID，指文件名,注意'-'与'_'的区别
            // 为啥要这样搞？总之锅laitx不背，laitx负责改得更容易操作而已哈哈 可以考虑自动获取url文件名，就不需要管这块儿了。
            $('.menu-' + current_parent_id).addClass('menu-active');
            $('.menu-active .icon-xia').addClass('icon-rotate')
            $('.menu-' + current_parent_id).next('.second-menu-list').css({'display': 'block'});
            $('.menu-' + current_parent_id).next('.second-menu-list').find('.' + child_id + '-second-menu').addClass('selected-active')
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
    //表格数据
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
                totalRow: true,
                cols: [[
                    {field: 'active_retain_date', title: '时间', unresize: true, totalRowText: '合计行'},
                    {field: 'first_day_count', title: '一天',totalRow: true},
                    {field: 'second_day_count', title: '两天',totalRow: true},
                    {field: 'third_day_count', title: '三天',totalRow: true},
                    {field: 'fourth_day_count', title: '四天',totalRow: true},
                    {field: 'fifth_day_count', title: '五天',totalRow: true},
                    {field: 'sixth_day_count', title: '六天',totalRow: true},
                    {field: 'seventh_day_count', title: '七天',totalRow: true},
                    {field: 'eighth_day_count', title: '八天',totalRow: true}
                ]],
                done: function (res, curr, count) {

                }
                , id: 'active_retain_date'
                , page: true
            });
        })
    },
    chartRender: function () {
        var _this = this;
        var start_time = $('#active_start').val();
        var end_time = $('#active_end').val();
        var periods = $('.active_periods>li').find('button.active').val();
        var user_type = $('#active_user-type').val();
        var active_if = $('#active_if').val();
        var region_id = $('#user_region_id').val() == '' ? common.role_area_show($('#user_super_manager_area_select')) : $('#user_region_id').val();
        if (start_time != '') {
            start_time = common.timeTransform(start_time + ' 00:00:00')
        }
        if (end_time != '') {
            end_time = common.timeTransform(end_time + ' 23:59:59')
        }
        var data = {
            start_time: start_time,
            end_time: end_time,
            periods: periods,
            user_type: user_type,
            special_tag: active_if,
            region_id: region_id
        };
        console.log(data);
        var url = '/active_retain/statistic/';
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                console.log(res);
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
        var url = setAbout.survival_url;
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
                            return this.point.y > 0 ? this.point.y + '人' : '';
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
            $('#user_super_manager_area').css({'display': 'block'});
            $('#user_super_manager_area_select').address({
                level: 3,
                offsetLeft: '-124px'
            });
            $('#survival_super_manager_area').css({'display': 'block'});
            $('#survival_super_manager_area_select').address({
                level: 3,
                offsetLeft: '-124px'
            });
        } else {
            $('#user_super_manager_area').css({'display': 'none'});
            $('#user_area').css({'display': 'block'});

            $('#survival_super_manager_area').css({'display': 'none'});
            $('#survival_area').css({'display': 'block'});
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
    var data = {
        start_date:$('#survival_start').val(),
        end_date:$('#survival_end').val(),
        user_type:$('#survival_user-type').val(),
        user_behavior:$('#survival_action').val(),
        region_id:$('#survival_region_id').val() == '' ? common.role_area_show($('#survival_super_manager_area_select')) : $('#survival_region_id').val()
    };
    if (data.start_date != '') {
        data.start_date = common.timeTransform(data.start_date + ' 00:00:00')
    }
    if (data.end_date != '') {
        data.end_date = common.timeTransform(data.end_date + ' 23:59:59')
    }
    console.log(data);
    var url = setAbout.survival_url +
        '?start_date=' + data.start_date +
        '&end_date=' + data.end_date +
        '&user_type=' + data.user_type +
        '&user_behavior=' + data.user_behavior +
        '&region_id=' + data.region_id;
    setAbout.tableSet(url)
});
$('#search_btn').click(function (e) {
    e.preventDefault();
    setAbout.chartRender();
})
