$('.layui-table-cell').css({'height': 'auto!important'});
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
setTimeout(function () {
    tableInit('/city/latest_orders/');
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 50);
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
            var startTime = common.timeTransform($('#date_show_one').val())
            var endTime = common.timeTransform($('#date_show_two').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！')
                return false
            }
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        done: function (val, index) {
            var startTime = common.timeTransform($('#date_show_one').val())
            var endTime = common.timeTransform($('#date_show_two').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
});

/*-----------------------------------------------------------------------------*/

$('#search_btn').click(function (e) {
    e.preventDefault();
    dataInit();
    console.log($('#city_area').val())
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    var data = {
        goods_type: $.trim($('#goods_type').val()),
        priority: $.trim($('#priority').val()),
        is_called: $.trim($('#is_called').val()),
        vehicle_length: $.trim($('#vehicle_length').val()),
        node_id: $.trim($('#node_id').val()),
        spec_tag: $.trim($('#spec_tag').val()),
        is_addition: $.trim($('#is_addition').val())
    };
    var url = '/city/latest_orders/?goods_type=' + data.goods_type + '&priority=' + data.priority + '&is_called=' + data.is_called + '&vehicle_length=' + data.vehicle_length + '&node_id=' +
        data.node_id + '&spec_tag=' + data.spec_tag + '&is_addition=' + data.is_addition;
    tableInit(url);
});

function dataInit() {
    var start_time = $.trim($('#date_show_one').val());
    var end_time = $.trim($('#date_show_two').val());
    if (common.timeTransform(start_time) > common.timeTransform(end_time)) {
        layer.msg('提示：开始时间大于了结束时间！');
        return false
    }
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
        $('.part-1-bottom ul').empty();
        $('.part-1-bottom ul').append(str);
        var dataStyle = {
            normal: {
                label: {show: false},
                labelLine: {show: false}
            }
        };
        var dashStyle_2 = {
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
                    trigger: 'item',
                    show: true,
                    formatter: "{a} <br/>{b} : {c} ({d})",
                    extraCssText: 'width:160px;height:60px;background:rgba(0,0,0,.4);'
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
                color: ['#2EC7C9', '#AA4643', '#5AB1EF', '#3D96AE', '#DB843D', '#A47D7C'],
                // colors: ['#2EC7C9', '#AA4643', '#B6A2DE', '#5AB1EF', '#3D96AE', '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92'],
                series: [
                    {
                        name: '货源数',
                        type: 'pie',
                        clockWise: false,
                        radius: [100, 120],
                        itemStyle: dataStyle,
                        data: val[0]
                    },
                    {
                        name: '车辆数',
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

function tableInit(url) {
    layui.use('table', function () {
        var table = layui.table;
        table.render({
            elem: '#LAY_table_goods',
            even: true
            , url: url,
            response: {
                statusName: 'status',
                statusCode: 100000
            },
            loading: true,
            cols: [[
                {field: 'goods_id', title: '货源ID', width: 82},
                {field: 'priority', title: '优先级', width: 82},
                {field: 'goods_type', title: '类型', width: 100},
                {field: 'content', title: '货物规格', width: 120},
                {field: 'supplier_node', title: '所属网点'},
                {field: 'vehicle', title: '车型要求', width: 116},
                {field: 'price', title: '运费', width: 180},
                {field: 'mobile', title: '货主手机', width: 110},
                {field: 'call_count', title: '通话数', width: 82},
                {field: 'goods_time', title: '时间', width: 200},
                {field: 'address', title: '出发地-目的地', width: 250},
                {
                    field: 'operate', title: '操作', width: 107, templet: function (d) {
                        return '<button id="' + d.phone_number + '" class="layui-btn layui-btn-small nearby" style="padding: 0 8px;"><i class="iconfont icon-qicheqianlian-" style="margin-right: 2px"></i>附近的车</button>'
                    }
                }
            ]],
            done: function (res, curr, count) {
                $('[data-field]>div').css({'padding': '0 6px'});
                $('.nearby').on('click', function () {
                    table.render({
                        elem: '#demo'
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
                        area: ['1400px', '520px'],
                        skin: 'layui-layer-molv',
                        closeBtn: 1,
                        content: $('#popup')
                    })
                });
                $("td[data-field='price']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        str = str.split('\n');
                        $(this).html(str[0] + '<br>' + str[1])
                    }
                });
                $("td[data-field='vehicle']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        str = str.split('\n');
                        $(this).html(str[0] + '<br>' + str[1])
                    }
                });
                $("td[data-field='goods_time']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        str = str.split('\n');
                        $(this).html(str[0] + '<br>' + str[1])
                    }
                });
                $("td[data-field='address']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        str = str.split('\n');
                        $(this).html(str[0] + '<br>' + str[1])
                    }
                })
                $("td[data-field='call_count']").children().each(function () {
                    if ($(this).text() != '') {
                        var str = $(this).text();
                        $(this).html(str + '次')
                    }
                })
            }
            , id: 'testReload'
            , page: true
        });
    })

}