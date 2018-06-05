/**
 * Created by Creazy_Run on 2018/5/30.
 */
/**
 * Created by Creazy_Run on 2018/5/30.
 */
$('.layui-table-cell').css({'height': 'auto!important'});
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);

function init() {
    $('#start_address_name').address({
        offsetLeft: '0',
        level: 3,
        onClose: function () {

        }
    });
    $('#over_address_name').address({
        offsetLeft: '0',
        level: 3,
        onClose: function () {

        }
    });
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

        }
    });
    laydate.render({
        elem: '#date_show_three',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[4]),
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
        elem: '#LAY_table_goods',
        even: true
        , url: '/goods/list/',
          response: {
              statusName: 'status',
              statusCode: 100000
          },
        cols: [[
            {field: 'id', title: '货源ID', width: 60},
            {field: 'goods_standard', title: '货物规格', width: 140}
            , {field: 'goods_type', title: '类型', width: 120}
            , {field: 'node_id', title: '所属网点', width: 140}
            , {field: 'from_to_dist', title: '出发地-目的地', width: 220}
            , {field: 'vehicle_type', title: '车型要求', width: 144}
            , {field: 'price_recommend', title: '运费', width: 180}
            , {field: 'mobile', title: '货主手机', width: 120}
            , {field: 'STATUS', title: '状态', width: 90}
            , {field: 'call_count', title: '通话数', width: 60}
            , {field: 'loading_time', title: '时间', width: 230}
            , {
                field: 'from_channel', title: '操作', width: 112, templet: function (d) {
                    return '<button id="' + d.phone_number + '" class="layui-btn layui-btn-small nearby" style="padding: 0 8px;"><i class="iconfont icon-qicheqianlian-" style="margin-right: 2px"></i>附近的车</button>'
                }
            }
        ]],
        done: function (res, curr, count) {
            $('[data-field]>div').css({'padding': '0 6px'});
            console.log(res)
            $('.nearby').on('click', function () {
                layer.open({
                    type: 1,
                    area: ['1620px', '520px'],
                    skin: 'layui-layer-molv',
                    closeBtn: 1,
                    content: $('#popup')
                })
            });
            $("td[data-field='goods_standard']").children().each(function (val) {
                var value = $(this).parent().parent('tr').attr('data-index');
                if($(this).text()!=''){
                  var result = $(this).text().split(',');
                   $(this).html('名称：<span style="font-weight: 500;color: deepskyblue;">'+result[0]+'</span><br>重量：<span style="font-weight: 500;color: deepskyblue;">'+result[1]+'</span><br>体积：<span style="font-weight: 500;color: deepskyblue;">'+result[2]+'</span>')
                }
            })
              $("td[data-field='STATUS']").children().each(function (val) {
                if($(this).text()==2){
                    $(this).text('待接单')
                }else if($(this).text()==3){
$(this).html('<span style="color: #40AFFE">已接单</span>')
                }else if($(this).text()==4){
$(this).html('<span style="color: #1E1E1E">已过期</span>')
                }else if($(this).text()==-1){
                $(this).html('<span style="color: #1E1E1E;font-weight: bold;">已取消</span>')
                }
            })
             $("td[data-field='from_to_dist']").children().each(function (val) {
                if($(this).text()!=''){
                  var result = $(this).text().split(',');
                  // $(this).html('<p><i class="iconfont icon-qidian"></i></p>')
                    console.log(result)
                }else {
                    $(this).text('未记录')
                }
            })
        }
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
    //监听工具条
    table.on('tool(demo)', function (obj) {
        var data = obj.data;
        if (obj.event === 'detail') {
            layer.msg('ID：' + data.id + ' 的查看操作');
        } else if (obj.event === 'del') {
            layer.confirm('真的删除行么', function (index) {
                obj.del();
                layer.close(index);
            });
        } else if (obj.event === 'edit') {
            layer.alert('编辑行：<br>' + JSON.stringify(data))
        }
    });

    var $ = layui.$, active = {
        getCheckData: function () { //获取选中数据
            var checkStatus = table.checkStatus('idTest')
                , data = checkStatus.data;
            layer.alert(JSON.stringify(data));
        }
        , getCheckLength: function () { //获取选中数目
            var checkStatus = table.checkStatus('idTest')
                , data = checkStatus.data;
            layer.msg('选中了：' + data.length + ' 个');
        }
        , isAll: function () { //验证是否全选
            var checkStatus = table.checkStatus('idTest');
            layer.msg(checkStatus.isAll ? '全选' : '未全选')
        }
    };

    $('.demoTable .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });

});
Highcharts.setOptions({
    colors: ['#2EC7C9', '#AA4643', '#B6A2DE', '#5AB1EF', '#3D96AE', '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92']
});
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
$('#charts_container_two').highcharts({
    chart: {
        zoomType: 'xy'
    },
    title: {
        text: '货源分布及发货人数趋势图'
    },
    subtitle: {
        text: '数据来源: 省省官方数据库'
    },
    xAxis: [{
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        crosshair: true,
        gridLineColor: '#eee',
        gridLineWidth: 1

    }],
    yAxis: [{ // Primary yAxis
        labels: {
            format: '{value}人',
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        },
        title: {
            text: '人数',
            style: {
                color: Highcharts.getOptions().colors[1]
            }
        }
    }, { // Secondary yAxis
        title: {
            text: '发货数',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        labels: {
            format: '{value} 人',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        },
        opposite: true
    }],
    tooltip: {
        shared: true
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
    series: [{
        name: '潜在货源',
        type: 'column',
        yAxis: 1,
        data: [59.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
        tooltip: {
            valueSuffix: ' 人'
        }
    },
        {
            name: '实际货源',
            type: 'column',
            yAxis: 1,
            data: [49.9, 61.5, 86.4, 79.2, 64.0, 85.0, 68.6, 26.5, 108.4, 136.1, 75.6, 15.4],
            tooltip: {
                valueSuffix: ' 人'
            }
        }, {
            name: '接单人数',
            type: 'column',
            yAxis: 1,
            data: [38.9, 81.5, 76.4, 79.2, 104.0, 171.0, 126.6, 114.5, 176.4, 154.1, 56.6, 54.4],
            tooltip: {
                valueSuffix: ' 人'
            }
        }, {
            name: '发货人数',
            type: 'line',
            data: [105.0, 69.9, 99.5, 149.5, 180.2, 179.5, 159.2, 172.5, 123.3, 180.3, 130.9, 99.6],
            tooltip: {
                valueSuffix: '人'
            }
        }]
});
$('#charts_container_three').highcharts({
    chart: {
        type: 'line'
    },
    title: {
        text: '发货/接单率趋势'
    },
    subtitle: {
        text: '数据来源: 省省官方后台数据库'
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
    tooltip: {
        shared: true,
        valueSuffix: '%',
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
    xAxis: {
        categories: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
        crosshair: true,
        gridLineColor: '#eee',
        gridLineWidth: 1
    },
    yAxis: {
        title: {
            text: '百分比(%)'
        },
        labels: {
            format: '{value}%',
            style: {
                color: Highcharts.getOptions().colors[0]
            }
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: true
            },
            enableMouseTracking: true
        }
    },
    series: [{
        name: '发货率',
        data: [17.0, 16.9, 19.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 19.6]
    }, {
        name: '接单率',
        data: [13.9, 14.2, 15.7, 18.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 16.6, 14.8]
    }]
});
$('#charts_container_four').highcharts({
    chart: {
        renderTo: 'chart'
    },
    title: {
        text: '取消原因统计'
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
                color: 'white',
                style: {
                    font: '13px Trebuchet MS, Verdana, sans-serif'
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
        data: [
            ['装货时间不合适', 3617],
            ['司机让我取消订单', 3436],
            ['突发事件', 416],
            ['运输变化有变', 200],
            ['车型大小不合适', 1000],
            ['其他', 5000]
        ]
    }]
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    if (beginTime != '' && finishTime == '') {
        layer.msg('请选择新增结束日期')
        return false;
    }
    if (beginTime == '' && finishTime != '') {
        layer.msg('请选择新增开始日期')
        return false;
    }
    if (beginTime != '') {
        beginTime = common.timeTransform(beginTime)
        console.log(beginTime)
    }
    if (finishTime != '') {
        var currentFinish = finishTime;
        finishTime = common.timeTransform(finishTime)
    }
    /* var data = {
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
     , {field: 'goods_count', title: '发货', width: 70}
     , {field: 'order_count', title: '接单', width: 70}
     , {field: 'order_completed', title: '完成订单', width: 90}
     , {field: 'download_channel', title: '下载渠道', width: 130}
     , {field: 'from_channel', title: '注册渠道', width: 180}
     , {field: 'last_login_time', title: '最后登陆', width: 130}
     , {field: 'create_time', title: '注册时间', width: 130}
     ]]
     , id: 'testReload'
     , page: true
     });
     })*/
});

