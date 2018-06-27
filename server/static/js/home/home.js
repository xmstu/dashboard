$('.layui-table-cell').css({'height': 'auto!important'});
$('.part-2 .layui-form-item').css({'width': "260px"})
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
setTimeout(function () {
    tableInit('/city/latest_orders/');
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 50);
layui.use(['laydate', 'form', 'table'], function () {
    dataInit();
    layer.load();
    var laydate = layui.laydate;
    var table = layui.table;
    laydate.render({
        elem: '#date_show_one',
        theme: '#009688',
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
        theme: '#009688',
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
        is_called: $.trim($('#is_called').val()),
        vehicle_length: $.trim($('#vehicle_length').val()),
        node_id: $.trim($('#node_id').val()),
        spec_tag: $.trim($('#spec_tag').val()),
        is_addition: $.trim($('#is_addition').val())
    };
    var url = '/city/latest_orders/?goods_type=' + data.goods_type + '&is_called=' + data.is_called + '&vehicle_length=' + data.vehicle_length + '&node_id=' +
        data.node_id + '&spec_tag=' + data.spec_tag + '&is_addition=' + data.is_addition;
    tableInit(url);
});

function dataInit() {

    layui.use('layer', function () {
        var layer = layui.layer;
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

            for (var i = 0; i < arr.length; i++) {
                str += '<li class="charts-lists"><div class="charts-container" id="charts_container_' + i + '"></div><div class="data-list-container' + i + '"></li>';
                $('.data-list-container0').append($('.tip-list-show0'))
                console.log($('.tip-list-show0'))
            }
            $('.part-1-bottom ul').empty();
            $('.part-1-bottom ul').append(str);
            var dataStyle = {
                normal: {
                    label: {show: false},
                    labelLine: {show: false}
                }
            };
            var result = "";
            //$('.data-list-container').append(result)
            $.each(res.data, function (index, val) {
                if (val[1][2].value < 0) {
                    val[1][2].value = 0
                }
                if (arr.length >= 0) {
                    arr.length--;
                }
                var result = '<span class=" tip-show-set tip-list-show' + arr.length + '">' + val[0][0].name + ':' + val[0][0].value + '单</span>';
                result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][1].name + ':' + val[0][1].value + '单</span>';
                result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][2].name + ':' + val[0][2].value + '单</span>';
                result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][0].name + ':' + val[1][0].value + '辆</span>';
                result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][1].name + ':' + val[1][1].value + '辆</span>';
                result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][2].name + ':' + val[1][2].value + '辆</span>';
                var all_count = '<p class="all_count">货源总数：<span>' + (val[0][0].value + val[0][1].value + val[0][2].value) + '单</span></p>'
                var all_count_1 = '<p class="all_count_1">车辆总数：<span>' + (val[1][0].value + val[1][1].value) + '辆</span></p>'
                if ($('#goods_types').val() == 1 || $('#goods_types').val() == 2) {
                    $('.data-list-container' + arr.length).html('');
                    $('.data-list-container' + arr.length).append(all_count + all_count_1 + result)
                } else if ($('#goods_types').val() == 3) {
                    var result_ano = '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][0].name + ':' + val[0][0].value + '单</span>';
                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][1].name + ':' + val[0][1].value + '单</span>';
                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][2].name + ':' + val[0][2].value + '单</span>';
                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][3].name + ':' + val[0][3].value + '单</span>';
                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][4].name + ':' + val[0][4].value + '单</span>';
                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][0].name + ':' + val[1][0].value + '辆</span>';
                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][1].name + ':' + val[1][1].value + '辆</span>';
                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][2].name + ':' + val[1][2].value + '辆</span>';
                    var all_count_ano = '<p class="all_count">货源总数：<span>' + (val[0][0].value + val[0][1].value + val[0][2].value + val[0][3].value + val[0][4].value) + '单</span></p>'
                    var all_count_ano_1 = '<p class="all_count_1">车辆总数：<span>' + (val[1][0].value + val[1][1].value) + '辆</span></p>'
                    $('.data-list-container' + arr.length).html('');
                    $('.data-list-container' + arr.length).append(all_count_ano + all_count_ano_1 + result_ano)

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
                        formatter: "{a} <br/>{b} : {c} ({d}%)",
                        extraCssText: 'width:auto;height:60px;background:rgba(0,0,0,.4);'
                    },
                    legend: {
                        orient: 'vertical',
                        x: 'left',
                        y: 'top',
                        data: [
                            '待接单', '已接单', '已取消', '待联系', '已联系', '已接单车辆', '待接单车辆数'
                        ]
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            mark: {show: true}
                        }
                    },
                    color: ['skyblue', '#7dd4f8', '#60b2d3', '#2973a7', '#497080', '#5fd779', '#56b35d'],
                    series: [
                        {
                            name: '货源数',
                            type: 'pie',
                            clockWise: false,
                            radius: [90, 105],
                            itemStyle: dataStyle,
                            data: val[0]
                        },
                        {
                            name: '车辆数',
                            type: 'pie',
                            clockWise: false,
                            radius: [75, 90],
                            itemStyle: dataStyle,
                            data: val[1]
                        }
                    ]
                };
                if (option && typeof option === "object") {
                    myChart.setOption(option, true);
                }
            })
            layer.closeAll('loading')
        })
    })
}

function tableInit(url) {
    layui.use(['layer', 'table', 'form'], function () {
        var table = layui.table;
        var form = layui.form;
        var layer = layui.layer;
        layer.load();
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
                {field: 'goods_id', title: '货源ID', width: 70},
                {field: 'goods_type', title: '类型', width: 60},
                {field: 'content', title: '货物规格', width: 120},
                {field: 'address', title: '出发地-目的地',width:310},
                {field: 'vehicle', title: '车型要求', width: 86},
                {field: 'price', title: '运费', width: 180},
                {field: 'mobile', title: '货主手机', width: 96},
                {field: 'call_count', title: '通话数', width: 60},
                {field: 'goods_time', title: '时间', width: 146},
                {field: 'supplier_node', title: '所属网点'},
                {
                    field: 'operate', title: '操作', width: 107, templet: function (d) {
                        return '<button value="' + d.goods_id + '" id="nearly_' + d.goods_id + '" class="layui-btn layui-btn-small nearby" style="padding: 0 8px;"><i class="iconfont icon-qicheqianlian-" style="margin-right: 2px"></i>附近的车</button>'
                    }
                }
            ]],
            done: function (res, curr, count) {
                layer.closeAll('loading')

                $('[data-field]>div').css({'padding': '0 6px'});
                $('.nearby').on('click', function () {
                    var val = $(this).val();
                    var url = '/city/nearby_cars/' + val;
                    form.on('select(interest)', function (res) {
                        var value = res.value;
                        var url_reset = '/city/nearby_cars/' + val + '?goods_type' + value;
                        tableReset(url_reset)
                    });
                    tableReset(url);
                    layer.open({
                        type: 1,
                        title: '附近的车',
                        area: ['1400px', '600px'],
                        skin: 'layui-layer-molv',
                        closeBtn: 1,
                        content: $('#popup')
                    })
                });
                $("td[data-field='price']").children().each(function () {
                    if ($(this).text() != '') {
                        layer.closeAll('loading')
                        var str = $(this).text();
                        str = str.split('\n');
                        $(this).html(str[0] + '<br>' + str[1])
                    }
                });
                $("td[data-field='mobile']").children().each(function () {
                    if ($(this).text().length > 14) {
                        var str = $(this).text();
                        str = str.split('\n');
                        $(this).html(str[0] + '<br>' + str[1])
                    }
                });
                $("td[data-field='vehicle']").children().each(function () {
                    if ($(this).text() != '') {
                        layer.closeAll('loading')
                        var str = $(this).text();
                        str = str.split('\n');
                        if (str[1] == '' || str[1] == undefined) {
                            $(this).html(str[0])
                        } else {
                            $(this).html(str[0] + '<br>' + str[1])
                        }
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

function tableReset(url) {
    layui.use(['table', 'form'], function () {
        var table = layui.table;
        var rate = layui.rate;
        table.render({
            elem: '#demo'
            , url: url //数据接口
            , page: false, //开启分页
            response: {
                statusName: 'status',
                statusCode: 100000
            },
            loading: true
            , cols: [[ //表头
                  {field: 'name', title: '司机姓名', width: 86}
                , {field: 'mobile', title: '手机号码', width: 110}
                , {field: 'usual_region', title: '匹配原则', width: 204}
                , {field: 'vehicle_length', title: '车长', width: 166}
                , {field: 'vehicle_type', title: '车型', width: 110}
                , {field: 'credit_level', title: '司机评分', width: 104}
                , {field: 'is_trust_member', title: '诚信会员', width: 84}
                , {field: 'order_count', title: '接单数', sort: true, width: 90}
                , {field: 'order_finished', title: '完成数', sort: true, width: 96}
                , {field: 'order_cancel', title: '取消数', sort: true, width: 86}
                , {field: 'current_region', title: '所在地', width: 206}
            ]]
            , done: function (res) {
                $("td[data-field='is_trust_member']").children().each(function () {
                    if ($(this).text() != '') {
                        layer.closeAll('loading')
                        var str = $(this).text();
                        if (str == 1) {
                            $(this).text('是')
                        } else if (str == 0) {
                            $(this).text('否')
                        }
                    }
                });
                $("td[data-field='usual_region']").children().each(function () {
                    $(this).html('最新定位')
                });
                $("td[data-field='credit_level']").children().each(function () {
                    var value_level = $(this).text();
                    if (value_level == 1) {
                        $(this).html('<p><i class="iconfont icon-iconfontxingxing"></i></p>')
                    }
                    if (value_level == 2) {
                        $(this).html('<p><i class="iconfont icon-iconfontxingxing"></i></p>')
                    }
                    if (value_level == 5) {
                        $(this).html('<p style="color: #009f95;"><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i></p>')
                    }
                });
            }
        });
    })
}