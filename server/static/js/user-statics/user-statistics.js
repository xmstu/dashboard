$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
$('#date_show_three').val();
$('#date_show_four').val();
$('#date_show_five').val();
$('#date_show_six').val();
var dataAll;
var startTime = $('#date_show_one').val();
var endTime = $('#date_show_two').val();
var beginTime = $('#date_show_three').val();
var finishTime = $('#date_show_four').val();
var infinteTime = $('#date_show_five').val();
var overTIme = $('#date_show_six').val();
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);

function init() {
    var data = ''
    var url = '/user/list/'
    $.ajax({
        url: url
        , type: "get"
        , async: false
        , dataType: "json"
        , success: function (result) {
            dataAll = result
        }
    });
}

layui.use(['laydate', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    laydate.render({
        elem: '#date_show_one',
        theme: '#1E9FFF',
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            startTime = val;
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
            endTime = val;
        }
    });
    laydate.render({
        elem: '#date_show_three',
        theme: '#1E9FFF',
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            beginTime = val + ' 00:00:00'
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
            finishTime = val + ' 23:59:59';
        }
    });
    laydate.render({
        elem: '#date_show_five',
        theme: '#1E9FFF',
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            infinteTime = val + ' 00:00:00'
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
            overTIme = val + ' 23:59:59'
        }
    });
    table.render({
        elem: '#LAY_table_user'
        , url: '/user/list/',
        response: {
            statusName: 'status',
            statusCode: 100000
        }
        , cols: [[
            {field: 'id', title: '用户ID', width: 80},
            {field: 'user_name', title: '用户名', width: 100}
            , {field: 'mobile', title: '手机号', width: 130}
            , {field: 'user_type', title: '注册角色', width: 80}
            , {field: 'role_auth', title: '认证', width: 180}
            , {field: 'usual_city', title: '常驻地', width: 280}
            , {field: 'goods_count', title: '发货', width: 90}
            , {field: 'order_count', title: '接单', width: 90}
            , {field: 'order_completed', title: '完成订单', width: 90}
            , {field: 'download_channel', title: '下载渠道', width: 130}
            , {field: 'from_channel', title: '注册渠道', width: 80}
            , {field: 'last_login_time', title: '最后登陆', width: 130}
            , {field: 'create_time', title: '注册时间', width: 130}
        ]]
        , id: 'testReload'
        , page: true
    });

    var $ = layui.$, active = {
        reload: function () {
            var demoReload = $('#demoReload');

            //执行重载
            table.reload('testReload', {
                page: {
                    curr: 1 //重新从第 1 页开始
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
$('#charts_container_one').highcharts({
    tooltip: {
        shared: false,
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
        colors: ['#058DC7', '#fff', '#ED561B', '#DDDF00', '#24CBE5', '#64E572',
            '#FF9655', '#FFF263', '#6AF9C4'],
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
        labelFormatter: function () {
            return this.name
        }
    },
    xAxis: {
        categories: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
    },
    yAxis: {
        title: {
            text: '气温 (°C)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: true          // 开启数据标签
            },
            enableMouseTracking: true // 关闭鼠标跟踪，对应的提示框、点击事件会失效
        }
    },
    series: [{
        name: '东京',
        data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
    }]
});
$('#search_btn').click(function (e) {
    e.preventDefault();
    layer.msg('success')
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
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
    var data = {
        user_name: $.trim($('#user_name').val()),
        mobile: $.trim($('#phone_number').val()),
        reference_mobile: $.trim($('#reference_mobile').val()),
        download_ch: $.trim($('#download_ch').val()),
        from_channel: $.trim($('#register').val()),
        is_referenced: $.trim($('#is_referenced').val()),
        home_station_id: $.trim($('#home_station_id').val()),
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
     var url = '/user/list/?user_name='+data.user_name+'&mobile='+data.mobile+'&reference_mobile='+data.reference_mobile+'&download_ch='+data.download_ch+'&from_channel=' +
         data.from_channel+'&is_referenced='+data.is_referenced+'&home_station_id='+data.home_station_id+'&role_type='+data.role_type+'&role_auth='+data.role_auth+'&is_actived='+data.is_actived+'&is_used='+data.is_used+'&is_car_sticker='+data.is_car_sticker+'&last_login_start_time='+data.last_login_start_time+ '&last_login_end_time='+data.last_login_end_time+'&register_start_time='+data.register_start_time+'&register_end_time='+data.register_end_time;

    layui.use('table', function () {
        var table = layui.table;
        table.render({
              url:url
            , elem: '#LAY_table_user'
            , response: {
                statusName: 'status',
                statusCode: 100000
            }
            , cols: [[
                {field: 'id', title: '用户ID', width: 80},
                {field: 'user_name', title: '用户名', width: 100}
                , {field: 'mobile', title: '手机号', width: 130}
                , {field: 'user_type', title: '注册角色', width: 80}
                , {field: 'role_auth', title: '认证', width: 180}
                , {field: 'usual_city', title: '常驻地', width: 280}
                , {field: 'goods_count', title: '发货', width: 90}
                , {field: 'order_count', title: '接单', width: 90}
                , {field: 'order_completed', title: '完成订单', width: 90}
                , {field: 'download_channel', title: '下载渠道', width: 130}
                , {field: 'from_channel', title: '注册渠道', width: 80}
                , {field: 'last_login_time', title: '最后登陆', width: 130}
                , {field: 'create_time', title: '注册时间', width: 130}
            ]]
            , id: 'testReload'
            , page: true
        });
    })
})
