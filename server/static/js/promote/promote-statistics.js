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
    $('.promote-menu-about>a').addClass('selected-active');
    $('.promote-menu-about>a>i').addClass('select-active');
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 10);
layui.use(['laydate', 'layer', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    var form = layui.form;
    var layer = layui.layer;
    form.on('select(is_actived)', function (data) {
        if (data.value == '1') {
            $('#select_spec_two').addClass('none').removeClass('area-select-options-setting');
            $('#select_spec_three').addClass('none').removeClass('area-select-options-setting');
            $('#select_spec_one').removeClass('none').addClass('area-select-options-setting');
        } else if (data.value == '2') {
            $('#select_spec_one').addClass('none').removeClass('area-select-options-setting');
            $('#select_spec_three').addClass('none').removeClass('area-select-options-setting');
            $('#select_spec_two').removeClass('none').addClass('area-select-options-setting');

        } else if (data.value == '3') {
            $('#select_spec_one').addClass('none').removeClass('area-select-options-setting');
            $('#select_spec_two').addClass('none').removeClass('area-select-options-setting');
            $('#select_spec_three').removeClass('none').addClass('area-select-options-setting');
        }
    });
    laydate.render({
        elem: '#date_show_one',
        theme: '#009688',
        max: String(common.getNowFormatDate()[3]),
        calendar: true,
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            var startTime = common.timeTransform($('#date_show_one').val())
            var endTime = common.timeTransform($('#date_show_two').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        done: function (val, index) {
            var startTime = $('#date_show_one').val();
            var endTime = $('#date_show_two').val();
            common.dateInterval(endTime, startTime);
            var startTime = common.timeTransform($('#date_show_one').val())
            var endTime = common.timeTransform($('#date_show_two').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }

    })
    ;
    laydate.render({
        elem: '#date_show_three',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
        done: function (val, index) {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips').show();
            } else {
                $('#date_show_three').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_three').val())
            var endTime = common.timeTransform($('#date_show_four').val())
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#date_show_four',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
        done: function (val, index) {
            if ($('#date_show_four').val() == '') {
                $('#date_show_four').next('.date-tips').show();
            } else {
                $('#date_show_four').next('.date-tips').hide()
            }
            var startTime = common.timeTransform($('#date_show_three').val());
            var endTime = common.timeTransform($('#date_show_four').val());
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });

});
$('#add_promote_person').on('click', function (e) {
    e.preventDefault();
    var str = "<p  style='position: relative;'><span class='phone-number'>人员号码</span><i class='iconfont icon-dianhua'></i><input id='add_users' maxlength='11' type='text' placeholder='请输入添加人的号码'></p> ";
    str += "<p  style='position: relative;'><span class='phone-number'>人员姓名</span><i class='iconfont icon-guanliyuan'></i><input id='add_users_name'  type='text' placeholder='请输入推广人的姓名'></p>";
    layer.confirm(str, {
        skin: 'layui-layer-molv',
        title: '新增推广人员',
        btn: ['确定添加', '取消']
    }, function () {
        var url = '/promote/effect/';
        var mobile = $('#add_users').val();
        var username = $('#add_users_name').val();
        var data = {
            "mobile": mobile
        }
        if (mobile == '' || mobile.length != 11) {
            layer.tips('请检查您输入的的手机号码格式','#add_users', {
                tips: [1, '#3595CC'],
                time: 3000
            });
        } else if (username == '') {
            layer.tips('请输入推广人员姓名','#add_users_name', {
                tips: [1, '#3595CC'],
                time: 3000
            });
        } else {
            $.ajax({
                url: url,
                type: 'post',
                data: JSON.stringify(data),
                dataType: 'json',
                contentType: "application/json; charset=utf-8",
                beforeSend: function () {
                    layer.load();
                },
                success: function (res) {
                    if (res.status == 100000) {
                        layer.msg('添加成功。', {icon: 6});
                    } else {
                        layer.msg('添加失败。', {icon: 5});
                    }
                },
                complete: function (xhttp) {
                    layer.closeAll('loading');
                    if (xhttp.status == 400) {
                        layer.msg('用户名不存在或者重复添加了推荐人')
                    }
                }
            });
        }
    }, function (index) {

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
        data_type: $('.area-select-options-setting .layui-anim > dd.layui-this').attr('lay-value')
    };
    console.log(data.data_type);
    var url = '/promote/quality/';
    if (data.dimension == 3) {
        http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
            if (res.status == 100000) {
                var len = res.data.xAxis.length;
                if (len >= 0 && len < 20) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 1, '金额(元)', '金额', '元')
                } else if (len > 0 && len > 20 && len < 40) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 2, '金额(元)', '金额', '元')
                } else if (len > 0 && len > 40 && len < 90) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.counts_series, 4, '金额(元)', '金额', '元')
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
                    lineChartInit(res.data.xAxis, res.data.series, 1, '人数(人)', '人数', '人')
                } else if (len > 0 && len > 20 && len < 40) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.series, 2, '人数(人)', '人数', '人')
                } else if (len > 0 && len > 40 && len < 90) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.series, 4, '人数(人)', '人数', '人')
                }
            }
        })
    }
}

function lineChartInit(xAxis, series, interval, str_title, names, units) {
    Highcharts.setOptions({
        colors: ['#A47D7C', '#DB843D', '#B6A2DE', '#2EC7C9', '#AA4643', '#5AB1EF', '#3D96AE', '#92A8CD', '#B5CA92']
    });
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
            text: null
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 1100,
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
            },
            labels: {
                format: '{value} 人',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        return this.point.y > 0 ? this.point.y + '人' : this.point.y;
                    }
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

var pageSet = {
    tableInit: function () {
        var that = this;
        layui.use(['table', 'layer'], function () {

            var layer = layui.layer;
            var requestStrat = $('#date_show_three').val();
            var endRequest = $('#date_show_four').val();
            if (requestStrat != '') {
                requestStrat = common.timeTransform($('#date_show_three').val() + ' 00:00:00');
            }
            if (endRequest != '') {
                endRequest = common.timeTransform($('#date_show_four').val() + ' 23:59:59');
            }
            var url = '/promote/effect/';
            var data = {
                user_name: $('#user_name').val(),
                mobile: $('#phone_number').val(),
                role_type: $('#is_referenced').val(),
                goods_type: $('#goods_type').val(),
                is_actived: $('#is_active_select').val(),
                is_car_sticker: $('#is_car_sticker').val(),
                start_time: requestStrat,
                end_time: endRequest
            };
            var url = '/promote/effect/?user_name=' + data.user_name + '&mobile=' + data.mobile + '&role_type=' + data.role_type + '&goods_type=' + data.goods_type + '&is_actived=' +
                data.is_actived + '&is_car_sticker=' + data.is_car_sticker + '&start_time=' + data.start_time + '&end_time=' + data.end_time;
            that.tableRender(url)
        })
    },
    tableRender: function (url) {
        layui.use('table', function () {
            var table = layui.table;
            table.render({
                elem: '#promote_table'
                , even: true
                , url: url
                , response: {
                    statusName: 'status',
                    statusCode: 100000
                }
                , cols: [[
                    {field: 'reference_id', title: '用户ID', sort: true}
                    , {field: 'reference_name', title: '姓名'}
                    , {field: 'reference_mobile', title: '手机号', sort: true}
                    , {field: 'user_count', title: '推荐人数'}
                    , {field: 'wake_up_count', title: '唤醒人数'}
                    , {field: 'goods_count', title: '发货数', sort: true}
                    , {field: 'goods_user_count', title: '发货人数', sort: true}
                    , {field: 'order_over_count', title: '完成数'}
                    , {field: 'goods_price', title: '货源金额', sort: true}
                    , {field: 'order_over_price', title: '完成金额', sort: true}
                    , {
                        field: 'wealth', title: '操作', width: 96, templet: function (d) {
                            return '<button id="deleteButton_' + d.reference_id + '" value="' + d.reference_id + '" class="layui-btn layui-btn-sm promote-delete"><i class="layui-icon">&#xe640;</i>删除</button>'
                        }
                    }
                ]]
                , done: function (res) {
                    $("td[data-field='user_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '人')
                        }
                    })
                    $("td[data-field='wake_up_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '人')
                        }
                    })
                    $("td[data-field='goods_user_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '人')
                        }
                    })
                    $("td[data-field='goods_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '次')
                        }
                    })
                    $("td[data-field='order_over_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '次')
                        }
                    })

                    $("td[data-field='goods_price']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '元')
                        }
                    })
                    $("td[data-field='order_over_price']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '元')
                        }
                    })
                    $('.promote-delete').on('click', function (e) {
                        e.preventDefault();
                        var current_val = $(this).val();
                        layer.confirm('您确定删除该条用户信息吗？', {
                            skin: 'layui-layer-molv',
                            btn: ['确认', '取消']
                        }, function () {
                            var url = '/promote/effect/?reference_id=' + current_val;
                            $.ajax({
                                url: url,
                                type: 'DELETE',
                                beforeSend: function () {
                                    layer.load();
                                },
                                success: function (res) {
                                    if (res.status == 100000) {
                                        layer.msg('已成功删除该条用户。', {icon: 1});
                                        $('#deleteButton_' + current_val).parents('tr').css({'display': 'none'})
                                        var requestStrat = $('#date_show_three').val();
                                        var endRequest = $('#date_show_four').val();
                                        if (requestStrat != '') {
                                            requestStrat = common.timeTransform($('#date_show_three').val() + ' 00:00:00');
                                        }
                                        if (endRequest != '') {
                                            endRequest = common.timeTransform($('#date_show_four').val() + ' 23:59:59');
                                        }
                                        table.reload('dataTable', {
                                            where: {
                                                user_name: $('#user_name').val(),
                                                mobile: $('#phone_number').val(),
                                                role_type: $('#is_referenced').val(),
                                                goods_type: $('#goods_type').val(),
                                                is_actived: $('#is_active_select').val(),
                                                is_car_sticker: $('#is_car_sticker').val(),
                                                start_time: requestStrat,
                                                end_time: endRequest
                                            },
                                            loading: true
                                        });
                                    } else {
                                        layer.msg('删除失败。', {icon: 5});
                                    }
                                },
                                complete: function (xhttp) {
                                    layer.closeAll('loading');
                                    if (xhttp.status == 400) {
                                        layer.msg('request error', {icon: 5})
                                    }
                                }
                            });
                        }, function (index) {
                            layer.close(index)
                        });
                    });

                }
                , page: true
                , id: 'dataTable'
            });

            $('.demoTable .layui-btn').on('click', function () {
                var type = $(this).data('type');
                active[type] ? active[type].call(this) : '';
            });
        })

    }
};
pageSet.tableRender('/promote/effect/');
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    pageSet.tableInit();
});

