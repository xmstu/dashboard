$('.layui-table-cell').css({'height': 'auto!important'});
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
$('#date_show_three').val();
$('#date_show_four').val();
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);


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
    table.render({
        elem: '#LAY_table_goods',
        even: true
        , url: '/city/latest_orders',
        response: {
            statusName: 'status',
            statusCode: 100000
        },
        loading:true,
        cols: [[
            {field: 'id', title: '货源ID', width: 60},
            {field: 'priority', title: '优先级', width: 80},
            {field: 'goods_type', title: '类型', width: 140},
            {field: 'weight', title: '货物规格', width: 120},
            {field: 'stipple', title: '所属网点', width: 140},
            {field: 'run_line', title: '出发地-目的地', width: 220},
            {field: 'vehicle_order', title: '车型要求', width: 144},
            {field: 'carriage', title: '运费', width: 180},
            {field: 'shipper_phone', title: '货主手机', width: 120},
            {field: 'communicate_count', title: '通话数', width: 60},
            {field: 'time_show', title: '时间', width: 230},
            {
                field: 'operate', title: '操作', width: 112, templet: function (d) {
                    return '<button id="' + d.phone_number + '" class="layui-btn layui-btn-small nearby" style="padding: 0 8px;"><i class="iconfont icon-qicheqianlian-" style="margin-right: 2px"></i>附近的车</button>'
                }
            }
        ]],
        done: function (res, curr, count) {
            $('[data-field]>div').css({'padding': '0 6px'});
            $('.nearby').on('click', function () {
                table.render({
                    elem: '#demo'
                    , height: 315
                    , url: '/demo/table/user/' //数据接口
                    , page: true //开启分页
                    , cols: [[ //表头
                        {field: 'id', title: 'ID', width: 80, sort: true, fixed: 'left'}
                        , {field: 'username', title: '司机姓名', width: 150}
                        , {field: 'sex', title: '手机号码', width: 130}
                        , {field: 'city', title: '所在地', width: 255}
                        , {field: 'sign', title: '常驻地', width: 177}
                        , {field: 'experience', title: '车长', width: 120}
                        , {field: 'score', title: '车型', width: 160}
                        , {field: 'classify', title: '司机评分', width: 120}
                        , {field: 'wealth', title: '诚信会员', width: 150, sort: true}
                        , {field: 'test', title: '接单数', width: 80, sort: true}
                        , {field: 'test123', title: '完成数', width: 80, sort: true}
                        , {field: 'test1234', title: '取消数', width: 80, sort: true}
                    ]]
                });
                layer.open({
                    type: 1,
                    area: ['1620px', '520px'],
                    skin: 'layui-layer-molv',
                    closeBtn: 1,
                    content: $('#popup')
                })
            });
            $("td[data-field='goods_id']").children().each(function (val) {
                var value = $(this).parent().parent('tr').attr('data-index');
                if ($(this).text() == '') {
                    //下面的一定要用html
                    //$(this).html(res.data[value].user_name+'</br>'+res.data[value].goods_count)
                }
            })
        }
        , id: 'testReload'
        , page: true
    });
});

/*-----------------------------------------------------------------------------*/
var dom = document.getElementById("charts_container_1");
var myChart = echarts.init(dom, e_macarons);
var dataStyle = {
    normal: {
        label: {show: false},
        labelLine: {show: false}
    }
};
option = {
    title: {
        text: '4.2m',
        subtext: null,
        x: 'center',
        y: 'center',
        itemGap: 20,
        textStyle: {
            color: 'skyblue',
            fontFamily: '微软雅黑',
            fontSize: 18,
            fontWeight: 'bolder'
        }
    },
    tooltip: {
        show: true,
        formatter: "{a} <br/>{b} : {c} ({d})"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        y: 'top',
        data: [
            '代接单', '已接单', '已取消', '待接单车辆数', '已接单车辆数'
        ]
    },
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    series: [
        {
            name: '1',
            type: 'pie',
            clockWise: false,
            radius: [100, 120],
            itemStyle: dataStyle,
            data: [
                {
                    value: 68,
                    name: '代接单'
                },
                {
                    value: 32,
                    name: '已接单'
                },
                {
                    value: 29,
                    name: '已取消'
                }
            ]
        },
        {
            name: '2',
            type: 'pie',
            clockWise: false,
            radius: [80, 100],
            itemStyle: dataStyle,
            data: [
                {
                    value: 71,
                    name: '待接单车辆数'
                },
                {
                    value: 91,
                    name: '已接单车辆数'
                }
            ]
        }
    ]
};
if (option && typeof option === "object") {
    myChart.setOption(option, true);
}
