/**
 * Created by Creazy_Run on 2018/5/30.
 */
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
layui.use('layer', function () {
    var layer = layui.layer;
    layer.load();
    dataInit();
});
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);
layui.use(['laydate', 'layer', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    var form = layui.form;
    var layer = layui.layer;

    form.on('select(is_actived)', function (data) {
        if (data.value == '1') {
            $('#select_spec_two').hide();
            $('#select_spec_three').hide();
            $('#select_spec_one').show();
            form.render('select');
        } else if (data.value == '2') {
             form.render('select');
            $('#select_spec_one').hide();
            $('#select_spec_three').hide();
            $('#select_spec_two').show();

        } else if (data.value == '3') {
            form.render('select');
            $('#select_spec_one').hide();
            $('#select_spec_two').hide();
            $('#select_spec_three').show();

        }
    });
    laydate.render({
        elem: '#date_show_one',
        theme: '#1E9FFF',
        max: String(common.getNowFormatDate()[5]),
        calendar: true,
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
        }
    });
    laydate.render({
        elem: '#date_show_three',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[5]),
        done: function (val, index) {
        }
    });
    laydate.render({
        elem: '#date_show_four',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        done: function (val, index) {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
        }
    });
    table.render({
        elem: '#promote_table'
        , even: true
        , url: '../static/js/user-statics/test.json/'
        , cols: [[
            {field: 'id', title: '用户ID', sort: true}
            , {field: 'username', title: '姓名'}
            , {field: 'phone_number', title: '手机号', sort: true}
            , {field: 'experience', title: '推荐人数'}
            , {field: 'order_count', title: '唤醒人数'}
            , {field: 'experience', title: '发货数', sort: true}
            , {field: 'score', title: '发货人数', sort: true}
            , {field: 'classify', title: '完成数'}
            , {field: 'money', title: '货源金额', sort: true}
            , {field: 'complete', title: '完成金额', sort: true}
            , {
                field: 'wealth', title: '操作',width:86, templet: function (d) {
                    return '<button class="layui-btn layui-btn-sm promote-delete"><i class="layui-icon">&#xe640;</i>删除</button>'
                }
            }
        ]]
        , done: function (res) {
            $('.promote-delete').on('click', function () {
                layer.confirm('您确定删除该条用户信息吗？', {
                    skin: 'layui-layer-molv',
                    btn: ['确认', '取消']
                }, function () {
                    layer.msg('OK', {icon: 1});
                }, function (index) {
                    layer.close(index)
                });
            })
        }
        , page: true
    });

    var $ = layui.$, active = {
        isAll: function () { //验证是否全选
            var checkStatus = table.checkStatus('idTest');
            layer.msg(checkStatus.isAll ? '全选' : '未全选')
        }
    };

    $('.demoTable .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    if (beginTime != '' && finishTime == '') {
        layer.msg('请选择新增结束日期');
        return false;
    }
    if (beginTime == '' && finishTime != '') {
        layer.msg('请选择新增开始日期');
        return false;
    }
});
$('#add_promote_person').on('click', function (e) {
    e.preventDefault();
    var str = "<p  style='position: relative;'><span class='phone-number'>输入号码</span><i class='iconfont icon-dianhua'></i><input id='add_users' maxlength='11' type='text' placeholder='请输入添加人的号码'></p> ";
    layer.confirm(str, {
        title: '新增推广人员',
        btn: ['确定添加', '取消']
    }, function () {
        layer.msg('添加成功')
    }, function (index) {
        layer.msg('取消')
    });
});

$('#search_btn').click(function (e) {
    e.preventDefault();
    dataInit();
});

function dataInit() {
    var requestStartTime = common.timeTransform($('#date_show_one').val() + ' 00:00:00');
    var requestEndTime = common.timeTransform($('#date_show_two').val() + ' 23:59:59');
    var data = {
        start_time: requestStartTime,
        end_time: requestEndTime,
        periods: $('.periods>li').find('button.active').val(),
        dimension: $('#is_actived').val(),
        data_type: $(".select-reset").val()
    };
    console.log(data.data_type)
    var url = '/promote/quality/';
    if (data.dimension == 3) {
        http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
            if (res.status == 100000) {
                var len = res.data.xAxis.length;
                if (len >= 0 && len < 20) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 1, '金额(元)','金额','元')
                } else if (len > 0 && len > 20 && len < 40) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 2, '金额(元)','金额','元')
                } else if (len > 0 && len > 40 && len < 90) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 4, '金额(元)','金额','元')
                }
            }
        })
    } else if (data.dimension == 1 || data.dimension == 2) {
        http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
            if (res.status == 100000) {
                var len = res.data.xAxis.length;
                var X_data = res.data.xAxis;
                if (len >= 0 && len < 20) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 1, '人数(人)','人数','人')
                } else if (len > 0 && len > 20 && len < 40) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 2, '人数(人)','人数','人')
                } else if (len > 0 && len > 40 && len < 90) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 4, '人数(人)','人数','人')
                }
            }
        })
    }
}

function lineChartInit(xAxis, series, interval, str_title,names,units) {
    $('#charts_container_one').highcharts({
        tooltip: {
            shared: true,
            valueSuffix: units,
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
            backgroundColor: '#fff',
            type: 'line'
        },

        title: {
            text: '推广统计变化趋势图'
        },
        subtitle: {
            text: '数据来源：省省官方后台数据库'
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
        xAxis: {
            tickInterval: interval,
            categories: xAxis,
            gridLineColor: '#eee',
            gridLineWidth: 1
        },
        yAxis: {
            title: {
                text: str_title
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
            name: names,
            data: series
        }]
    });
}

var pageSet = {};