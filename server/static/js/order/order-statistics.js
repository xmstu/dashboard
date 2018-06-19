/**
 * Created by Creazy_Run on 2018/5/30.
 */
$('.layui-table-cell').css({'height': 'auto!important'});
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
$('#start_date_one').val(String(common.getNowFormatDate()[2]));
$('#end_time_one').val(String(common.getNowFormatDate()[3]));
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);

function init() {
    $('.layui-form-item').width('250px');
    $('#from_region_id').address({
        offsetLeft: '0',
        level: 3,
        onClose: function () {

        }
    });
    $('#to_region_id').address({
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
        elem: '#start_date_one',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[4]),
        ready: function () {

        },
        done: function (val, index) {
            var startTime = $('#start_date_one').val();
            var endTime = $('#end_time_one').val();
            alert(12)
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#start_date_one').val() == '') {
                $('#start_date_one').next('.date-tips').show();
            } else {
                $('#start_date_one').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#end_time_one',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        ready: function () {

        },
        done: function (val, index) {
            var startTime = $('#start_date_one').val();
            var endTime = $('#end_time_one').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#end_time_one').val() == '') {
                $('#end_time_one').next('.date-tips').show();
            } else {
                $('#end_time_one').next('.date-tips').hide()
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
            , {field: 'address', title: '出发地-目的地', width: 250}
            , {field: 'vehicle', title: '车型要求', width: 144}
            , {field: 'price', title: '运费', width: 210}
            , {field: 'mobile', title: '货主手机', width: 120}
            , {field: 'goods_status', title: '状态', width: 109}
            , {field: 'call_count', title: '通话数', width: 60}
            , {field: 'goods_time', title: '时间', width: 180}
            , {
                field: 'from_channel', title: '操作', width: 112, templet: function (d) {
                    return '<button value="' + d.id + '" id="' + d.id + '" class="layui-btn layui-btn-small nearby" style="padding: 0 8px;"><i class="iconfont icon-qicheqianlian-" style="margin-right: 2px"></i>附近的车</button>'
                }
            }
        ]],
        done: function (res, curr, count) {
            $('[data-field]>div').css({'padding': '0 6px'});
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
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html('<i class="iconfont icon-huowu1 mr-4" style="font-weight: 500;color: deepskyblue;"></i><span style="font-weight: 500;color: deepskyblue;">' + result[0] + '</span><br><i style="font-weight: 500;color: deepskyblue;" class="mr-4 iconfont icon-zhongliangweight9"></i><span style="font-weight: 500;color: deepskyblue;">' + result[1] + '</span>')
                }
            });
            $("td[data-field='goods_time']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html('<i class="iconfont icon-fabu mr-4"  title="发布时间" style="font-weight: 500;color: deepskyblue;"></i><span style="">' + result[0] + '</span><br><i style="font-weight: 500;color: deepskyblue;" class="mr-4 iconfont icon-huowu1" title="装货时间"></i><span>' + result[1])
                }
            });
            $("td[data-field='price']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html('<span>' + result[0] + '</span ></br>' + result[1] + '</span>')
                }
            });
            $("td[data-field='vehicle']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    if (result[0] !== '') {
                        $(this).html('<i class="iconfont icon-yifahuo mr-4"></i>' + result[0])
                    } else if (result[1] != '' || result[1] != undefined) {
                        $(this).html('<i class="iconfont icon-yifahuo mr-4"></i>' + result[0] + '<br><i class="iconfont icon-yifahuo mr-4"></i>' + result[1])
                    } else if (result[2] != '' || result[2] != undefined) {
                        $(this).html('<i class="iconfont icon-yifahuo mr-4"></i>' + result[0] + '<br><i class="iconfont icon-yifahuo mr-4"></i>' + result[1] + '<br><i class="iconfont icon-yifahuo mr-4"></i>' + result[2])
                    }
                }
            });
            $("td[data-field='mobile']").children().each(function (val) {
                if ($(this).text().length > 12) {
                    var result = $(this).text().split('\n');
                    $(this).html('<span>' + result[0] + '</span ><br><span style="color: #f40;">(' + result[1] + ')</span>')
                }
            });
            $("td[data-field='address']").children().each(function (val) {
                if ($(this).text() != '') {
                    var result = $(this).text().split('\n');
                    $(this).html('<i class="iconfont icon-qidian mr-4"></i>' + result[0] + '<br><i class="iconfont icon-zhongdian mr-4"></i>' + result[1] + '<br><i class="iconfont icon-luxian"></i>' + result[2])
                }
            })
        }
        , id: 'goods_reload'
        , page: true
    });
    var $ = layui.$, active = {
        reload: function () {
            var demoReload = $('#demoReload');

            //执行重载
            table.reload('goods_reload', {
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
    $('#goods_search_box').on('click', function (e) {
        e.preventDefault();
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
Highcharts.setOptions({
    colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C','#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
});
$('#charts_container_one').highcharts({
     chart: {
        type: 'area'
    },
    title: {
        text: '订单统计'
    },
    subtitle: {
        text: null
    },
    xAxis: {
        categories: ['1750', '1800', '1850', '1900', '1950', '1999', '2050'],
        tickmarkPlacement: 'on',
        title: {
            enabled: false
        }
    },
    yAxis: {
        title: {
            text: '订单汇总'
        },
        labels: {
            formatter: function () {
                return this.value+'单';
            }
        }
    },
    tooltip: {
        split: true,
        valueSuffix: '单',
        backgroundColor:'#FFF',

    },
    plotOptions: {
        area: {
            stacking: 'normal',
            lineColor: '#666666',
            lineWidth: 1,
            marker: {
                radius:3.5,
                lineWidth: 1,
                fillColor:'#fff',
                lineColor: '#666666',
                symbol: 'circle',
                states:{
                    hover:{
                        enabled:true,
                        radius:3.5
                    }
                }
            }
        }
    },
    series: [{
        name: '已完成',
        data: [502, 635, 809, 947, 1402, 3634, 5268]
    }, {
        name: '进行中',
        data: [106, 107, 111, 133, 221, 767, 1766]
    }, {
        name: '已取消',
        data: [163, 203, 276, 408, 547, 729, 628]
    }]
});
$('#charts_container_two').highcharts({
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

$('#goods_search_box').on('click', function (e) {
    e.preventDefault();
    var create_start_time = $('#create_start_time').val();
    var create_end_time = $('#create_end_time').val();
    var load_start_time = $('#load_start_time').val();
    var load_end_time = $('#load_end_time').val();
    if (create_start_time != '') {
        create_start_time = common.timeTransform(create_start_time)
    }
    if (create_end_time != '') {
        create_end_time = common.timeTransform(create_end_time)
    }
    if (load_start_time != '') {
        load_start_time = common.timeTransform(load_start_time)
    }
    if (load_end_time != '') {
        load_end_time = common.timeTransform(load_end_time)
    }
    var data = {
        goods_id: $.trim($('#goods_id').val()),
        mobile: $.trim($('#mobile').val()),
        from_region_id: $.trim($('#reference_mobile').val()),
        to_region_id: $.trim($('#to_region_id').val()),
        goods_type: $.trim($('#goods_type').val()),
        goods_status: $.trim($('#goods_status').val()),
        is_called: $.trim($('#is_called').val()),
        vehicle_length: $.trim($('#vehicle_length').val()),
        vehicle_type: $.trim($('#vehicle_type').val()),
        node_id: $.trim($('#node_id').val()),//10
        new_goods_type: $.trim($('#new_goods_type').val()),
        urgent_goods: $.trim($('#urgent_goods').val()),
        is_addition: $.trim($('#is_addition').val()),
        from_province_id: $('#from_region_id').attr('provinceid') == undefined ? '' : $('#from_region_id').attr('provinceid'),
        from_city_id: $('#from_region_id').attr('cityid') == undefined ? '' : $('#from_region_id').attr('cityid'),
        from_dist_id: $('#from_region_id').attr('districtsid') == undefined ? '' : $('#from_region_id').attr('districtsid'),
        to_province_id: $('#to_region_id').attr('provinceid') == undefined ? '' : $('#to_region_id').attr('provinceid'),
        to_city_id: $('#to_region_id').attr('cityid') == undefined ? '' : $('#to_region_id').attr('cityid'),
        to_dist_id: $('#to_region_id').attr('districtsid') == undefined ? '' : $('#to_region_id').attr('districtsid'),
        create_start_time: create_start_time,
        create_end_time: create_end_time,
        load_start_time: load_start_time,
        load_end_time: load_end_time,//23
        page: 1,
        limit: 10
    }
    var url = '/goods/list/?goods_id=' + data.goods_id + '&mobile=' + data.mobile + '&from_province_id=' + data.from_province_id + '&from_city_id=' + data.from_city_id + '&from_dist_id=' + data.from_dist_id + '&to_province_id=' + data.to_province_id + '&to_city_id=' + data.to_city_id + '&to_dist_id=' + data.to_dist_id +
        data.goods_type + '&goods_status=' + data.goods_status + '&is_called=' + data.is_called + '&vehicle_length=' + data.vehicle_length + '&vehicle_type=' + data.vehicle_type + '&node_id=' + data.node_id + '&new_goods_type=' + data.new_goods_type + '&urgent_goods=' + data.urgent_goods + '&is_addition=' + data.is_addition + '&create_start_time=' + data.create_start_time + '&create_end_time=' + data.create_end_time + '&load_start_time=' + data.load_start_time + '&load_end_time=' + data.load_end_time;

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
            cols: [[
                {field: 'id', title: '货源ID', width: 60},
                {field: 'goods_standard', title: '货物规格', width: 140}
                , {field: 'goods_type', title: '类型', width: 120}
                , {field: 'node_id', title: '所属网点', width: 140}
                , {field: 'address', title: '出发地-目的地', width: 250}
                , {field: 'vehicle', title: '车型要求', width: 144}
                , {field: 'price', title: '运费', width: 210}
                , {field: 'mobile', title: '货主手机', width: 120}
                , {field: 'goods_status', title: '状态', width: 109}
                , {field: 'call_count', title: '通话数', width: 60}
                , {field: 'goods_time', title: '时间', width: 180}
                , {
                    field: 'from_channel', title: '操作', width: 112, templet: function (d) {
                        return '<button value="' + d.id + '" id="' + d.id + '" class="layui-btn layui-btn-small nearby" style="padding: 0 8px;"><i class="iconfont icon-qicheqianlian-" style="margin-right: 2px"></i>附近的车</button>'
                    }
                }
            ]],
            done: function (res, curr, count) {
                $('[data-field]>div').css({'padding': '0 6px'});
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
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html('<i class="iconfont icon-huowu1 mr-4" style="font-weight: 500;color: deepskyblue;"></i><span style="font-weight: 500;color: deepskyblue;">' + result[0] + '</span><br><i style="font-weight: 500;color: deepskyblue;" class="mr-4 iconfont icon-zhongliangweight9"></i><span style="font-weight: 500;color: deepskyblue;">' + result[1] + '</span>')
                    }
                })
                $("td[data-field='goods_time']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html('<i class="iconfont icon-fabu mr-4"  title="发布时间" style="font-weight: 500;color: deepskyblue;"></i><span style="">' + result[0] + '</span><br><i style="font-weight: 500;color: deepskyblue;" class="mr-4 iconfont icon-huowu1" title="装货时间"></i><span>' + result[1])
                    }
                })
                $("td[data-field='price']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html('<span>' + result[0] + '</span >')
                    }
                })
                $("td[data-field='mobile']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html('<span>' + result[0] + '</span ><br><span style="color: #f40;">(' + result[1] + ')</span>')
                    }
                })
                $("td[data-field='vehicle']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        if (result[0] !== '') {
                            $(this).html('<i class="iconfont icon-yifahuo mr-4"></i>' + result[0])
                        } else if (result[1] != '' || result[1] != undefined) {
                            $(this).html('<i class="iconfont icon-yifahuo mr-4"></i>' + result[0] + '<br><i class="iconfont icon-yifahuo mr-4"></i>' + result[1])
                        } else if (result[2] != '' || result[2] != undefined) {
                            $(this).html('<i class="iconfont icon-yifahuo mr-4"></i>' + result[0] + '<br><i class="iconfont icon-yifahuo mr-4"></i>' + result[1] + '<br><i class="iconfont icon-yifahuo mr-4"></i>' + result[2])
                        }

                    }
                })

                $("td[data-field='address']").children().each(function (val) {
                    if ($(this).text() != '') {
                        var result = $(this).text().split('\n');
                        $(this).html('<i class="iconfont icon-qidian mr-4"></i>' + result[0] + '<br><i class="iconfont icon-zhongdian mr-4"></i>' + result[1] + '<br><i class="iconfont icon-luxian"></i>' + result[2])
                    }
                })
            }
            , id: 'goods_reload'
            , page: true
        });
    })
});
