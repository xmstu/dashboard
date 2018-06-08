$('.layui-table-cell').css({'height': 'auto!important'});
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);
layui.use(['laydate', 'form', 'table'], function () {
    dataInit();
    var laydate = layui.laydate;
    var table = layui.table;
    laydate.render({
        elem: '#date_show_one',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[4]),
        done: function (val, index) {

        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
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
        loading: true,
        cols: [[
            {field: 'id', title: '货源ID'},
            {field: 'priority', title: '优先级'},
            {field: 'goods_type', title: '类型'},
            {field: 'weight', title: '货物规格'},
            {field: 'stipple', title: '所属网点'},
            {field: 'run_line', title: '出发地-目的地'},
            {field: 'vehicle_order', title: '车型要求'},
            {field: 'carriage', title: '运费'},
            {field: 'shipper_phone', title: '货主手机'},
            {field: 'communicate_count', title: '通话数'},
            {field: 'time_show', title: '时间'},
            {
                field: 'operate', title: '操作', templet: function (d) {
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
                        {field: 'id', title: 'ID', sort: true, fixed: 'left'}
                        , {field: 'username', title: '司机姓名'}
                        , {field: 'sex', title: '手机号码'}
                        , {field: 'city', title: '所在地'}
                        , {field: 'sign', title: '常驻地'}
                        , {field: 'experience', title: '车长'}
                        , {field: 'score', title: '车型'}
                        , {field: 'classify', title: '司机评分'}
                        , {field: 'wealth', title: '诚信会员', sort: true}
                        , {field: 'test', title: '接单数', sort: true}
                        , {field: 'test123', title: '完成数', sort: true}
                        , {field: 'test1234', title: '取消数', sort: true}
                    ]]
                });
                layer.open({
                    type: 1,
                    area: ['1600px', '520px'],
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

$('#search_btn').click(function (e) {
    e.preventDefault();
    layer.msg('success')
});

function dataInit() {
    var start_time = $.trim($('#date_show_one').val());
    var end_time = $.trim($('#date_show_two').val());
    var goods_types = $.trim($('#goods_types').val());
    var region_id = $.trim($('#city_area').val());
    if (start_time != '') {
        start_time = common.timeTransform(start_time + ' 00:00:00')
    }
    if (end_time != '') {
        end_time = common.timeTransform(end_time + ' 23:59:59')
    }
    var url = '/city/resource/';
    var data = {
        start_time: start_time,
        end_time: end_time,
        region_id: region_id,
        goods_type: goods_types
    };
    http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
        var arr = Object.keys(res.data);
        var str = '';
        var elemArr = [];
          for (var i = 0; i < arr.length; i++) {
            str += '<li class="charts-container" id="charts_container_' + i + '"></li>';
        }
        $('.part-1-bottom ul').append(str);
        var dataStyle = {
            normal: {
                label: {show: false},
                labelLine: {show: false}
            }
        };
        var placeHolderStyle = {
            normal: {
                color: 'rgba(0,0,0,0)',
                label: {show: false},
                labelLine: {show: false}
            },
            emphasis: {
                color: 'rgba(0,0,0,0)'
            }
        };
        $.each(res.data, function (index, val) {
            console.log(val[1])
            if (arr.length >= 0) {
                arr.length--;
            }
            var dom = document.getElementById('charts_container_' + arr.length + '');
            var myChart = echarts.init(dom, e_macarons);
            option = {
                title: {
                    text: index,
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
                        '待接单', '已接单', '已取消', '已接单车辆', '待接单车辆数'
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
                        data: val[0]
                    },
                    {
                        name: '2',
                        type: 'pie',
                        clockWise: false,
                        radius: [80, 100],
                        itemStyle: dataStyle,
                        data: val[1]
                    }
                ]
            };
            if (option && typeof option === "object") {
                myChart.setOption(option, true);
            }
        })
    })
}