$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
var requestStart = $('#date_show_one').val() + ' 00:00:00';
var requestEnd = $('#date_show_two').val() + ' 23:59:59';
setTimeout(function () {
    chart_one_init();
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);
$('#area_select').address({
    offsetLeft: '0',
    level: 3,
    onClose: function () {
    }
});
layui.use(['laydate', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
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
              {field: 'id', title: '业务类型',  sort: true},
                 {field: 'user_name', title: '出发地',width:350}
                , {field: 'mobile', title: '目的地',width:350}
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
function chart_one_init(){
    $('#charts_container_one').highcharts({
        chart: {
        type: 'line'
    },
         legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 1300,
        y: 0,
        floating: true,
        borderWidth: 1,
        backgroundColor: 'transparent',
        labelFormatter: function () {
            return this.name
        }
    },
    title: {
        text: '运力趋势统计'
    },
    subtitle: {
        text: '省省官方后台数据库'
    },
    xAxis: {
        categories: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
         gridLineColor: '#eee',
        gridLineWidth: 1
    },
    yAxis: {
        title: {
            text: '数量 (件)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                // 开启数据标签
                enabled: true
            },
            // 关闭鼠标跟踪，对应的提示框、点击事件会失效
            enableMouseTracking: true
        }
    },
    series: [{
        name: '东京',
        data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    }, {
        name: '伦敦',
        data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    }, {
        name: '实际接单',
        data: [6.9, 8.2, 4.7, 12.5, 1.9, 11.2, 12.0, 6.6, 9.2, 7.3, 16.6, 14.8]
    }]
    })
}