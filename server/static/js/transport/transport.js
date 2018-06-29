var dataSet = {
    init: function () {
        var that = this;
        $('#date_show_three').val(String(common.getNowFormatDate()[2]));
        $('#date_show_four').val(String(common.getNowFormatDate()[3]));
        setTimeout(function () {
            $('.layui-form-item .layui-inline ').css({'margin-right': 0});
            $('.part-2').css({'padding-top': '0px', 'border-top': 0});
            that.radar_chart_init();
            that.dateRender();
        }, 10);
        $('#area_select').address({
            offsetLeft: '0',
            level: 3,
            onClose: function () {
            }
        });
    },
    dateRender: function () {
        layui.use(['laydate', 'form', 'table'], function () {
            var laydate = layui.laydate;
            var table = layui.table;
            laydate.render({
                elem: '#date_show_three',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
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
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
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

                }
                , cols: [[
                    {field: 'id', title: '业务类型', sort: true},
                    {field: 'user_name', title: '出发地', width: 350}
                    , {field: 'mobile', title: '目的地', width: 350}
                    , {field: 'user_type', title: '里程'}
                    , {field: 'role_auth', title: '货源量'}
                    , {field: 'usual_city', title: '车辆数'}
                    , {field: 'goods_count', title: '接单量'}
                    , {field: 'order_count', title: '图表'}
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
    },
    radar_chart_init: function () {
        Highcharts.setOptions({
            colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
        });
        $('#charts_container_two').highcharts({
            chart: {
                polar: true,
                type: 'line'
            },
            title: {
                text: '运力雷达图',
                x: -80
            },
            pane: {
                size: '80%'
            },
            xAxis: {
                categories: ['小面包车', '17M', '13M', '9.6M',
                    '7.6M', '6.8M', '4.2M', '中面包车', '小货车'],
                tickmarkPlacement: 'on',
                lineWidth: 0
            },
            yAxis: {
                gridLineInterpolation: 'polygon',
                lineWidth: 0,
                min: 0
            },
            tooltip: {
                shared: true,
                pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}辆</b><br/>'
            },
            legend: {
                align: 'left',
                verticalAlign: 'top',
                y: 70,
                layout: 'vertical'
            },
            series: [{
                name: '车辆数',
                data: [50000, 39000, 42000, 31000, 26000, 14000, 19000, 60000, 35000, 17000, 10000],
                pointPlacement: 'on',
                type: 'area'
            }, {
                name: '车辆数',
                data: [60000, 59000, 52000, 41000, 66000, 24000, 29000, 70000, 45000, 27000, 20000],
                pointPlacement: 'on',
                type: 'line'
            }, {
                name: '货源量',
                data: [43000, 19000, 60000, 35000, 17000, 10000, 19000, 60000, 35000, 17000, 10000],
                pointPlacement: 'on',
                type: 'area'
            }]
        })
    }
};
dataSet.init();