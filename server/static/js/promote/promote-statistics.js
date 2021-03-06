/**
 * 推广统计
 */
/*----------------设置日期框中的初始化值----------------------*/
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
layui.use('layer', function () {
    var layer = layui.layer;
    dataInit();
    $('.layui-form-item').css({width: '184px'})
    $('.area').css({width: '250px'})
});
/*----------------设置侧边栏样式----------------------*/
setTimeout(function () {
    $('.menu-promote').addClass('menu-active');
    $('.menu-active .icon-xia').addClass('icon-rotate')
    $('.menu-promote').next('.second-menu-list').css({'display': 'block'});
    $('.menu-promote').next('.second-menu-list').find('.promote-second-menu').addClass('selected-active')
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 10);
/*------------对表单进行校验----------------*/
layui.use(['laydate', 'layer', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    var form = layui.form;
    var layer = layui.layer;
    form.on('select(is_actived)', function (data) {
        /*监听select达到模拟联动效果*/
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
        format: 'yyyy/MM/dd',
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
        format: 'yyyy/MM/dd',
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
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#date_show_three').val() == '') {
                $('#date_show_three').next('.date-tips-icon').show();
            } else {
                $('#date_show_three').next('.date-tips-icon').hide()
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
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#date_show_four').val() == '') {
                $('#date_show_four').next('.date-tips-icon').show();
            } else {
                $('#date_show_four').next('.date-tips-icon').hide()
            }
            var startTime = common.timeTransform($('#date_show_three').val());
            var endTime = common.timeTransform($('#date_show_four').val());
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#statistic_start_time',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#statistic_start_time').val() == '') {
                $('#statistic_start_time').next('.date-tips-icon').show();
            } else {
                $('#statistic_start_time').next('.date-tips-icon').hide()
            }
            var startTime = common.timeTransform($('#statistic_start_time').val());
            var endTime = common.timeTransform($('#statistic_end_time').val());
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
    laydate.render({
        elem: '#statistic_end_time',
        theme: '#009688',
        calendar: true,
        max: String(common.getNowFormatDate()[0]),
        format: 'yyyy/MM/dd',
        done: function (val, index) {
            if ($('#statistic_end_time').val() == '') {
                $('#statistic_end_time').next('.date-tips-icon').show();
            } else {
                $('#statistic_end_time').next('.date-tips-icon').hide()
            }
            var startTime = common.timeTransform($('#statistic_start_time').val());
            var endTime = common.timeTransform($('#statistic_end_time').val());
            if (startTime > endTime) {
                layer.msg('提示：开始时间大于了结束时间！');
                return false;
            }
        }
    });
});
/*推广中的新增按钮点击*/
$('#add_promote_person').on('click', function (e) {
    e.preventDefault();
    var str = "<p  style='position: relative;'><span class='phone-number'>人员号码</span><i class='iconfont icon-dianhua'></i><input id='add_users' maxlength='11' type='text' placeholder='请输入推广人号码'></p> ";
    str += "<p  style='position: relative;'><span class='phone-number'>人员姓名</span><i class='iconfont icon-guanliyuan'></i><input id='add_users_name'  type='text' placeholder='请输入推广人姓名'></p>";
    layer.confirm(str, {
        skin: 'layui-layer-molv',
        title: '新增推广人员',
        btn: ['确定', '取消']
    }, function () {
        var url = '/promote/effect/';
        var mobile = $('#add_users').val();
        var username = $('#add_users_name').val();
        var data = {
            "mobile": mobile,
            "user_name": username
        };
        if (mobile == '' || mobile.length != 11) {
            layer.tips('请检查您输入的的手机号码格式', '#add_users', {
                tips: [1, '#009688'],
                time: 3000
            });
        } else if (username == '') {
            layer.tips('请输入推广人员姓名', '#add_users_name', {
                tips: [1, '#009688'],
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

                },
                success: function (res) {
                    if (res.status == 100000) {
                        layer.msg('添加成功。', {icon: 6});
                        window.location.reload();
                    } else {
                        layer.msg('添加失败。', {icon: 5});
                    }
                },
                complete: function (xhttp) {
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
    var url = '/promote/quality/';
    if (data.dimension == 3) {
        http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
            if (res.status == 100000) {
                var len = res.data.xAxis.length;
                if (len >= 0 && len < 20) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.series, 1, '金额(元)', '金额', '元')
                } else if (len > 0 && len > 20 && len < 40) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.series, 3, '金额(元)', '金额', '元')
                } else if (len > 0 && len > 40 && len < 90) {
                    $('.chart-tips').css({'display': 'none'});
                    lineChartInit(res.data.xAxis, res.data.series, 5, '金额(元)', '金额', '元')
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
        colors: ['#009688', '#DB843D', '#B6A2DE', '#2EC7C9', '#AA4643', '#5AB1EF', '#3D96AE', '#92A8CD', '#B5CA92']
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
                        return this.point.y > 0 ? this.point.y + '人' : null;
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
            var statistic_start_time = $('#statistic_start_time').val();
            var statistic_end_time = $('#statistic_end_time').val();
            if (requestStrat != '') {
                requestStrat = Number(common.timeTransform($('#date_show_three').val() + ' 00:00:00'));
            }
            if (endRequest != '') {
                endRequest = common.timeTransform($('#date_show_four').val() + ' 23:59:59');
            }
            if (statistic_start_time != '') {
                statistic_start_time = Number(common.timeTransform($('#statistic_start_time').val() + ' 00:00:00'));
            }
            if (statistic_end_time != '') {
                statistic_end_time = Number(common.timeTransform($('#statistic_end_time').val() + ' 23:59:59'));
            }
            if (requestStrat != '' && endRequest == '') {
                endRequest = common.currentTime();
            }
            if (requestStrat == '' && endRequest != '') {
                layer.tips('请输入开始日期！', '#date_show_three', {
                    tips: [1, '#009688'],
                    time: 3000
                });
                return false;
            }
            var url = '/promote/effect/';
            var data = {
                user_name: $('#user_name').val(),
                mobile: $('#phone_number').val(),
                goods_type: $('#goods_type').val(),
                register_start_time: requestStrat,
                register_end_time: endRequest,
                statistic_start_time: statistic_start_time,
                statistic_end_time: statistic_end_time,
                region_id: $.trim($("#node_id").val()) == "" ? common.role_area_show($("#super_manager_area_one")) : $.trim($("#node_id").val())
            };
            var url = '/promote/effect/?user_name=' + data.user_name + '&mobile=' + data.mobile + '&goods_type=' + data.goods_type + '&register_start_time=' + data.register_start_time + '&register_end_time=' + data.register_end_time + '&statistic_start_time=' + data.statistic_start_time + '&statistic_end_time=' + data.statistic_end_time+'&region_id='+data.region_id;
            that.tableRender(url)
        })
    },
    tableRender: function (url) {
        layui.use(['layer', 'table'], function () {
            var table = layui.table;
            var layer = layui.layer;
            table.render({
                elem: '#promote_table'
                , even: true
                , url: url
                , response: {
                    statusName: 'status',
                    statusCode: 100000
                },
                data:null,
                totalRow: true,
                cols: [[
                    {field: 'user_id', title: '姓名ID', unresize: true, totalRowText: '合计行'},
                    {field: 'user_name', title: '姓名'},
                    {field: 'region_name', title: '城市'}
                    , {field: 'mobile', title: '手机号'}
                    , {field: 'register_owner_count', title: '注册货主数',totalRow: true}
                    , {field: 'goods_count', title: '发货数',totalRow: true}
                    , {field: 'goods_owner_count', title: '发货人数', sort: true,totalRow: true}
                    , {field: 'goods_received_count', title: '货源被接数', sort: true,totalRow: true}
                    , {field: 'register_driver_count', title: '注册司机',totalRow: true}
                    , {field: 'auth_driver_count', title: '认证司机数',totalRow: true}
                    , {field: 'accept_order_count', title: '司机接单数',totalRow: true}
                    , {field: 'sticker_driver_count', title: '百万车贴',totalRow: true}
                    , {
                        field: 'wealth', title: '操作', width: 96, templet: function (d) {
                            return '<button id="deleteButton_' + d.user_id + '" value="' + d.mobile + '" class="layui-btn layui-btn-sm promote-delete"><i class="layui-icon">&#xe640;</i>删除</button>'
                        }
                    }
                ]]
                , done: function (res) {
                    $('.main-content-right').addClass('animated fadeIn');
                    $("td[data-field='accept_order_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '次')
                        }
                    })
                    $("td[data-field='goods_owner_count']").children().each(function () {
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
                    $("td[data-field='goods_received_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '次')
                        }
                    })

                    $("td[data-field='sticker_driver_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '次')
                        }
                    })
                    $("td[data-field='auth_driver_count']").children().each(function () {
                        if ($(this).text() != '') {
                            var str = $(this).text();
                            $(this).html(str + '次')
                        }
                    })
                    $('.promote-delete').on('click', function (e) {
                        e.preventDefault();
                        var current_val = $(this).val();
                        layer.confirm('您确定删除该条用户信息吗？', {
                            skin: 'layui-layer-molv',
                            btn: ['确认', '取消']
                        }, function () {
                            var url = '/promote/effect/' + current_val;
                            $.ajax({
                                url: url,
                                type: 'DELETE',
                                beforeSend: function () {

                                },
                                success: function (res) {
                                    if (res.status == 100000) {
                                        layer.msg('已成功删除该条用户。', {icon: 1});
                                        $('#deleteButton_' + current_val).parents('tr').css({'display': 'none'});
                                        var requestStrat = $('#date_show_three').val();
                                        var endRequest = $('#date_show_four').val();
                                        var statistic_start_time = $('#statistic_start_time').val();
                                        var statistic_end_time = $('#statistic_end_time').val();

                                        if (requestStrat != '') {
                                            requestStrat = common.timeTransform($('#date_show_three').val() + ' 00:00:00');
                                        }
                                        if (endRequest != '') {
                                            endRequest = common.timeTransform($('#date_show_four').val() + ' 23:59:59');
                                        }
                                        if (statistic_start_time != '') {
                                            statistic_start_time = common.timeTransform($('#statistic_start_time').val() + ' 00:00:00');
                                        }
                                        if (statistic_end_time != '') {
                                            statistic_end_time = common.timeTransform($('#statistic_end_time').val() + ' 23:59:59');
                                        }
                                        table.reload('dataTable', {
                                            where: {
                                                user_name: $('#user_name').val(),
                                                mobile: $('#phone_number').val(),
                                                goods_type: $('#goods_type').val(),
                                                register_start_time: requestStrat,
                                                register_end_time: endRequest,
                                                statistic_start_time: statistic_start_time,
                                                statistic_end_time: statistic_end_time
                                            },
                                            loading: true
                                        });
                                    } else {
                                        layer.msg('删除失败。', {icon: 5});
                                    }
                                },
                                complete: function (xhttp) {
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

function area_select() {
    var auth_role = $("#user-info").attr("data-role-type");
    if (!!auth_role && auth_role == 1) {
        $("#super_manager_area").css({
            "display": "block"
        });
        $("#super_manager_area_two").css({
            "display": "block"
        });
        $("#super_manager_area_one").address({
            level: 3,
            offsetLeft: '-124px'
        });
        $("#super_manager_area_zero").address({
            level: 3,
            offsetLeft: '-124px'
        })
    } else {
        $("#super_manager_area").css({
            "display": "none"
        });
        $("#city_manager_area_one").css({
            "display": "block"
        });
        $("#super_manager_area_two").css({
            "display": "none"
        });
        $("#city_manager_two").css({
            "display": "block"
        })
    }
}

area_select();
