/**
 * Created by Creazy_Run on 2018/5/30.
 */
/**
 * Created by Creazy_Run on 2018/5/30.
 */
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
$('#date_show_three').val();
$('#date_show_four').val();
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
        ready: function () {

        },
        done: function (val, index) {
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
        }
    });
    table.render({
        elem: '#LAY_table_goods',
        even: true
        , url: '../static/js/user-statics/test.json',
        /*  response: {
              statusName: 'status',
              statusCode: 100000
          },*/
        cols: [[
            {field: 'goods_id', title: '货源ID', width: 80},
            {field: 'user_name', title: '货物规格', width: 140}
            , {field: 'mobile', title: '类型', width: 120}
            , {field: 'user_type', title: '所属网点', width: 140}
            , {field: 'role_auth', title: '出发地-目的地', width: 220}
            , {field: 'usual_city', title: '车型要求', width: 150}
            , {field: 'goods_count', title: '运费', width: 180}
            , {field: 'order_count', title: '货主手机', width: 120}
            , {field: 'order_completed', title: '状态', width: 90}
            , {field: 'download_channel', title: '通话数', width: 50}
            , {field: 'download_channel', title: '时间', width: 230}
            , {
                field: 'from_channel', title: '操作', width: 130, templet: function (d) {
                    return '<button id="' + d.phone_number + '" class="layui-btn nearby">附近的车</button>'
                }
            }
        ]],
        done: function (res, curr, count) {
            $('[data-field]>div').css({'padding': '0 6px'})
            $('.nearby').on('click', function () {
                layer.open({
                    type: 1,
                    area: ['1400px', '400px'],
                    skin: 'layui-layer-molv',
                    closeBtn: 1,
                    content: $('#popup')
                })
            });
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
    colors:['#4572A7', '#AA4643', '#89A54E', '#80699B', '#3D96AE', '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92']
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
})
