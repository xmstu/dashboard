var dataSet = {
    init: function () {
        var that = this;
        $('#date_show_three').val(String(common.getNowFormatDate()[2]));
        $('#date_show_four').val(String(common.getNowFormatDate()[3]));
        setTimeout(function () {
            $('.layui-form-item .layui-inline ').css({'margin-right': 0});
            $('.part-2').css({'padding-top': '0px', 'border-top': 0});
            $('.transport-menu-about>a').addClass('selected-active');
            that.radar_chart_init($('#charts_container_two'));
            that.tableRender('/transport/list/');
        }, 10);
        $('#area_select').address({
            offsetLeft: '0',
            level: 3,
            onClose: function () {
            }
        });
        $('#start_place').address({
            offsetLeft: '0',
            level: 3,
            onClose: function () {
            }
        });
        $('#end_place').address({
            offsetLeft: '0',
            level: 3,
            onClose: function () {
            }
        });
    },
    dataRender: function () {
        var that = this;
        layui.use(['laydate', 'form', 'table'], function () {
            var laydate = layui.laydate;
            var table = layui.table;
            laydate.render({
                elem: '#date_show_three',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                ready: function () {

                },
                done: function (val, index) {
                    if ($('#date_show_three').val() == '') {
                        $('#date_show_three').next('.date-tips').show();
                    } else {
                        $('#date_show_three').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#date_show_four',
                theme: '#009688',
                calendar: true,
                max: String(common.getNowFormatDate()[0]),
                ready: function () {
                },
                done: function (val, index) {
                    if ($('#date_show_four').val() == '') {
                        $('#date_show_four').next('.date-tips').show();
                    } else {
                        $('#date_show_four').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#start_time_show',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                ready: function () {

                },
                done: function (val, index) {
                    if ($('#start_time_show').val() == '' || val == '') {
                        $('#start_time_show').next('.date-tips').show();
                    } else {
                        $('#start_time_show').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#end_time_show',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                ready: function () {

                },
                done: function (val, index) {
                    if ($('#end_time_show').val() == '' || val == '') {
                        $('#end_time_show').next('.date-tips').show();
                    } else {
                        $('#end_time_show').next('.date-tips').hide()
                    }
                }
            });

        });
    },
    radar_chart_init: function (elem, categories, order_ret, vehicles_ret, goods_ret) {
        Highcharts.setOptions({
            colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
        });
        elem.highcharts({
            chart: {
                polar: true,
                type: 'line'
            },
            title: {
                text: '运力雷达图'
            },
            marker: {
                enabled: false
            },
            pane: {
                size: '80%'
            },
            xAxis: {
                categories: categories,
                tickmarkPlacement: 'on',
                lineWidth: 0
            },
            yAxis: {
                gridLineInterpolation: 'polygon',
                lineWidth: 0,
                min: 0
            },
            tooltip: {
                shared: true,
                pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}辆</b><br/>'
            },
            legend: {
                align: 'left',
                verticalAlign: 'top',
                y: 70,
                layout: 'vertical'
            },
            plotOptions: {
                marker: {
                    enabled: false
                }
            },
            series: [
                {
                    name: '实际接单',
                    data: order_ret,
                    pointPlacement: 'on',
                    type: 'area'
                },
                {
                    name: '车辆数',
                    data: vehicles_ret,
                    pointPlacement: 'on',
                    type: 'line'
                },
                {
                    name: '货源量',
                    data: goods_ret,
                    pointPlacement: 'on',
                    type: 'line'
                }
            ]
        })
    },
    tableRender:function(table_url){
        var that = this;
        layui.use(['table','layer'],function(){
            var layer = layui.layer;
            var table = layui.table;
            table.render({
                elem: '#LAY_table_user'
                , url: table_url,
                even: true,
                response: {
                    statusName: 'status',
                    statusCode: 100000
                }
                , cols: [[
                    {field: 'business', title: '业务类型'},
                    {field: 'from_address', title: '出发地', width: 300}
                    , {field: 'to_address', title: '目的地', width: 300}
                    , {field: 'mileage', title: '里程'}
                    , {field: 'goods_count', title: '货源量'}
                    , {field: 'order_count', title: '车辆数'}
                    , {field: 'vehicle_count', title: '接单量'}
                    , {field: 'create_time', title: '统计时间'}
                    , {
                        field: 'operate', title: '操作', width: 107, templet: function (d) {
                            return '<button value="' + d.business + '" data-from-province="' + d.from_province_id + '"  data-from-city="' + d.from_city_id + '" data-from-town="' + d.from_town_id + '"  data-from-county="' + d.from_county_id + '" data-to-province="' + d.to_province_id + '"  data-to-city="' + d.to_city_id + '"  data-to-town="' + d.to_town_id + '"  data-to-county="' + d.to_county_id + '" class="layui-btn layui-btn-small radar-btn" data-start-time = "' + d.start_time + '" data-end-time = "' + d.end_time + '" style="padding: 0 8px;"><i class="iconfont icon-leidatu" style="margin-right: 2px"></i>雷达图</button>'
                        }
                    }
                ]]
                ,
                done: function (res, curr, count) {
                    layer.closeAll('loading')
                    $('.radar-btn').on('click', function () {
                        layer.load();
                        var url = '/transport/radar/';
                        var business = $(this).val();
                        var from_province_id = $(this).attr('data-from-province');
                        var from_city_id = $(this).attr('data-from-city');
                        var from_county_id = $(this).attr('data-from-county');
                        var from_town_id = $(this).attr('data-from-town');
                        var to_province_id = $(this).attr('data-to-province');
                        var to_city_id = $(this).attr('data-to-city');
                        var to_county_id = $(this).attr('data-to-county');
                        var to_town_id = $(this).attr('data-to-town');
                        var start_time = $(this).attr('data-start-time');
                        var end_time = $(this).attr('data-end-time');
                        var data = {
                            'business': business,
                            'from_province_id': from_province_id,
                            'from_city_id': from_city_id,
                            'from_county_id': from_county_id,
                            'from_town_id': from_town_id,
                            'to_province_id': to_province_id,
                            'to_city_id': to_city_id,
                            'to_county_id': to_county_id,
                            'to_town_id': to_town_id,
                            start_time: start_time,
                            end_time: end_time

                        }
                        $.ajax({
                            type: 'get',
                            url: url,
                            dataType: 'json',
                            data: data,
                            beforeSend: function () {

                            },
                            success: function (res) {
                                $('.popup-tbody').html('')
                                var data = res.data;
                                var vehicle_name_list = data.vehicle_name_list;
                                var goods_ret = data.goods_ret;
                                var orders_ret = data.orders_ret;
                                var vehicle_ret = data.vehicles_ret;
                                console.log(vehicle_ret);
                                that.radar_chart_init($('#radar_charts_container'), vehicle_name_list, orders_ret, vehicle_ret, goods_ret);
                                for (var i = 0; i < vehicle_name_list.length; i++) {
                                    var str = '<tr>';
                                    str += '<td>' + vehicle_name_list[i] + '</td>';
                                    str += '<td>' + goods_ret[i] + '单</td>';
                                    str += '<td>' + vehicle_ret[i] + '辆</td>';
                                    str += '<td style="color: #44c660;font-weight: bold;">' + orders_ret[i] + '单</td>';
                                    str += '<td style="color: #f40;font-weight: bold;">' + that.transition(goods_ret[i], orders_ret[i]) + '</td>';
                                    str += '<tr>';
                                    $('.popup-tbody').append(str)
                                }
                                if ($('.popup-tbody').html() != '') {
                                    layer.open({
                                        type: 1,
                                        title: '运力统计车型雷达图',
                                        content: $('#popup'),
                                        area: ['1400px', '540px'],
                                        skin: 'layui-layer-molv',
                                        colseBtn: 1
                                    })
                                }
                            },
                            failed: function () {
                                layer.msg('数据请求失败')
                            },
                            complete: function () {
                                layer.closeAll('loading')
                            }
                        })

                    })
                }
                , id: 'testReload'
                , page: true
            });
        })
    },
    chart_request: function () {
        var that = this;
        var url = '/transport/radar/';
        var start_time = $('#date_show_three').val();
        var end_time = $('#date_show_four').val();
        if (start_time != '') {
            start_time = common.timeTransform(start_time + ' 00:00:00')
        }
        if (end_time != '') {
            end_time = common.timeTransform(end_time + ' 00:00:00')
        }
        var data = {
            start_time: start_time,
            end_time: end_time,
            region_id: $('#region_id').val() == '' ? common.role_area_show($('#super_manager_area_select_zero')) : $.trim($('#region_id').val()),
            business: $('#business').val()
        };
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var vehicles_ret = res.data.vehicles_ret;
                var goods_ret = res.data.goods_ret;
                var orders_ret = res.data.orders_ret;
                var vehicle_name_list = res.data.vehicle_name_list;
                $('.transport-tbody').html('');
                if (vehicle_name_list.length > 0) {
                    that.radar_chart_init($('#charts_container_two'), vehicle_name_list, orders_ret, vehicles_ret, goods_ret);
                    for (var i = 0; i < vehicle_name_list.length; i++) {
                        var str = '<tr>';
                        str += '<td>' + vehicle_name_list[i] + '</td>';
                        str += '<td>' + goods_ret[i] + '单</td>';
                        str += '<td>' + vehicles_ret[i] + '辆</td>';
                        str += '<td style="color: #44c660;font-weight: bold;">' + orders_ret[i] + '单</td>';
                        str += '<td style="color: #f40;font-weight: bold;">' + that.transition(goods_ret[i], orders_ret[i]) + '</td>';
                        str += '<tr>';
                        $('.transport-tbody').append(str)
                    }

                } else {
                    return false;
                }
            })
        });

    },
    transition: function (val1, val2) {
        if (val1 > 0) {
            var result = (val2 / val1 * 100).toFixed(2) + '%'
        }
        if (val1 == 0 || val2 == 0) {
            result = 0;
        }
        return result
    },
    area_select: function () {
        var auth_role = $('#user-info').attr('data-role')
        if (!!auth_role && auth_role == 1) {
            $('#super_manager_area').css({'display': 'block'})
            $('#super_manager_area_select_zero').address({
                level: 3
            });
        } else {
            $('#super_manager_area').css({'display': 'none'});
            $('#city_manager_one').css({'display': 'block'})
        }
    }
};
dataSet.area_select();
dataSet.init();
dataSet.chart_request();
$('#search_btn').on('click', function (e) {
    e.preventDefault();
    dataSet.chart_request()
});
$('#transport_search_box').click(function (e) {
    e.preventDefault();
    layui.use('layer', function () {
        var layer = layui.layer;
        layer.load()
        var start_time = $('#start_time_show').val();
        var end_time = $('#end_time_show').val();
        if (start_time != '') {
            start_time = common.timeTransform(start_time + ' 00:00:00')
        }
        if (end_time != '') {
            end_time = common.timeTransform(end_time + ' 23:59:59')
        }
        var data = {
            from_province_id: $('#start_place').attr('provinceid') == undefined ? '' : $('#start_place').attr('provinceid'),
            from_city_id: $('#start_place').attr('cityid') == undefined ? '' : $('#start_place').attr('cityid'),
            from_county_id: $('#start_place').attr('districtsid') == undefined ? '' : $('#start_place').attr('districtsid'),
            to_province_id: $('#end_place').attr('provinceid') == undefined ? '' : $('#end_place').attr('provinceid'),
            to_city_id: $('#end_place').attr('cityid') == undefined ? '' : $('#end_place').attr('cityid'),
            to_county_id: $('#end_place').attr('districtsid') == undefined ? '' : $('#end_place').attr('districtsid'),
            vehicle_length: $('#vehicle_length').val(),
            business: $('#business_show').val(),
            filter: $('#transport_filter').val(),
            start_time: start_time,
            end_time: end_time

        };
        var url = '/transport/list?from_province_id=' + data.from_province_id + '&from_city_id=' + data.from_city_id + '&from_county_id=' + data.from_county_id + '&to_province_id=' + data.to_province_id + '&to_city_id=' + data.to_city_id + '&to_county_id=' + data.to_county_id + '&vehicle_length=' + data.vehicle_length + '&business=' + data.business + '&filter=' + data.filter + '&start_time=' + data.start_time + '&end_time=' + data.end_time
        dataSet.tableRender(url)
    })
})