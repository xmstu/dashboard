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
        theme: '#009688',
        calendar: true,
         format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#date_show_one').val() == '') {
                $('#date_show_one').next('.date-tips').show();
            } else {
                $('#date_show_one').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            if (common.timeTransform(startTime) > common.timeTransform(endTime)) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false
            }
            if ($('#date_show_two').val() == '') {
                $('#date_show_two').next('.date-tips').show();
            } else {
                $('#date_show_two').next('.date-tips').hide()
            }
        }
    });
    laydate.render({
        elem: '#start_date_one',
        theme: '#009688',
        calendar: true,
         max: String(common.getNowFormatDate()[0]),
       format:'yyyy/MM/dd',
        done: function (val, index) {
            var startTime = $('#start_date_one').val();
            var endTime = $('#end_time_one').val();
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
         max: String(common.getNowFormatDate()[0]),
         format:'yyyy/MM/dd',
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
});
var setAbout = {
    that: this,
    tableRender: function (url) {
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
                text: '接口还没做',
                cols: [[
                    {field: 'id', title: '订单ID', width: 60},
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
    }
};
//setAbout.tableRender();