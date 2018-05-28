layui.use(['laydate', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    laydate.render({
        elem: '#date_show_one',
        value: String(common.getNowFormatDate()[0]),
        theme: '#1E9FFF',
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            console.log(val)
        }
    });
    laydate.render({
        elem: '#date_show_two',
        value: String(common.getNowFormatDate()[1]),
        theme: '#1E9FFF',
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            console.log(val)
        }
    })
    laydate.render({
        elem: '#date_show_three',
        value: String(common.getNowFormatDate()[0]),
        theme: '#1E9FFF',
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            console.log(val)
        }
    });
    laydate.render({
        elem: '#date_show_four',
        value: String(common.getNowFormatDate()[1]),
        theme: '#1E9FFF',
        calendar: true,
        ready: function () {

        },
        done: function (val, index) {
            console.log(val)
        }
    });
    table.render({
        elem: '#LAY_table_user'
        ,url: '../static/js/user-statics/test.json'
        ,cols: [[
             {field:'user_name', title: '用户名', width:130}
            ,{field:'phone_number', title: '手机号', width:180}
            ,{field:'roles', title: '注册角色', width:140}
            ,{field:'profession', title: '认证', width:280}
            ,{field:'usual_city', title: '常驻地', width:280}
            ,{field:'shipments', title: '发货',width:90}
            ,{field:'order_receiving', title: '接单',  width:90}
            ,{field:'accomplish_orders', title: '完成订单',  width:90}
            ,{field:'download_ways', title: '下载渠道',  width:135}
            ,{field:'register_channel', title: '注册渠道',  width:80}
            ,{field:'last_login', title: '最后登陆', width:135}
            ,{field:'register_time', title: '注册时间',  width:135}
        ]]
        ,id: 'testReload'
        ,page: true
        ,height: 315
    });

    var $ = layui.$, active = {
        reload: function(){
            var demoReload = $('#demoReload');

            //执行重载
            table.reload('testReload', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                ,where: {
                    key: {
                        id: demoReload.val()
                    }
                }
            });
        }
    };

    $('.dataTable .layui-btn').on('click', function(){
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
$('#charts_container_one').highcharts({
    tooltip: {
        shared:false,
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
        text: '测试图表'
    },
    subtitle: {
        text: '数据来源：省省官方后台数据库'
    },
    legend:{
        labelFormatter:function () {
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