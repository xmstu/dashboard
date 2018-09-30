var dataSet = {
    init: function () {
        var that = this;
        $('.part-2 .layui-form-item').width('184');
        $('.part-3 .layui-input-inline').width('108');
        $('#date_show_three').val(String(common.getNowFormatDate()[2]));
        $('#date_show_four').val(String(common.getNowFormatDate()[0]));
        setTimeout(function () {
            $('.menu-transport').addClass('menu-active');
            $('.menu-active .icon-xia').addClass('icon-rotate');
            $('.menu-transport').next('.second-menu-list').css({'display': 'block'});
            $('.menu-transport').next('.second-menu-list').find('.transport-second-menu').addClass('selected-active')
            $('.layui-form-item .layui-inline ').css({'margin-right': 0});
            $('.part-2').css({'padding-top': '0px', 'border-top': 0});
            that.tableRender('/transport/list/');
        }, 10);
        $('#area_select').address({
            offsetLeft: '-124px',
            level: 4,
            onClose: function () {
            }
        });
        $('#start_place').address({
            offsetLeft: '-124px',
            level: 2,
            onClose: function () {
            }
        });
        $('#end_place').address({
            offsetLeft: '-124px',
            level: 2,
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
                format: 'yyyy/MM/dd',
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
                format: 'yyyy/MM/dd',
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
                format: 'yyyy/MM/dd',
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
                format: 'yyyy/MM/dd',
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
    radar_chart_init: function (elem, categories, vehicles_ret, vehicles_all_ret) {
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
                    name: '活跃司机数',
                    data: vehicles_ret,
                    pointPlacement: 'on',
                    type: 'area'
                },
                {
                    name: '总司机数',
                    data: vehicles_all_ret,
                    pointPlacement: 'on',
                    type: 'line'
                }
            ]
        })
    },
    tableRender: function (table_url) {
        var that = this;
        layui.use(['table', 'layer'], function () {
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
                    {field: 'from_address', title: '出发地'}
                    , {field: 'to_address', title: '目的地'}
                    , {field: 'login_driver_count', title: '登陆司机'}
                    , {field: 'total_driver_count', title: '总司机数'}
                    , {
                        field: 'operate', title: '操作', templet: function (d) {
                            return '<button  data-from-city="' + d.from_city_id + '"  data-from-county="'+d.from_county_id+'" data-to-city="' + d.to_city_id + '" data-to-county="' + d.to_county_id + '" class="layui-btn layui-btn-small radar-btn" data-start-time = "' + d.start_time + '" data-end-time = "' + d.end_time + '" style="padding: 0 8px;"><i class="iconfont icon-leidatu" style="margin-right: 2px"></i>雷达图</button>'
                        }
                    }
                ]]
                ,
                done: function (res, curr, count) {
                    $('.main-content-right').addClass('animated fadeIn');
                    $('.preview').removeClass('none');
                    var general_situation=res.general_situation;
                    var str_ = ''
                    $('.preview ul').html('')
                    if(general_situation.length>0){
                        $.each(general_situation,function(val,index){
                            console.log(index);
                            str_+='<li>'+index.from_address+'</li>';
                            str_+='<li>'+index.to_address+'</li>';
                            str_+='<li>'+index.login_driver_count+'</li>';
                            str_+='<li>'+index.total_driver_count+'</li>';
                        });
                    }else{
                          str_+='<li>无数据</li>';
                    }
                     $('.preview ul').html(str_)
                    $('.radar-btn').on('click', function () {
                        var url = '/transport/radar/';
                        var from_city_id = $(this).attr('data-from-city');
                        var from_county_id = $(this).attr('data-from-county');
                        var to_city_id = $(this).attr('data-to-city');
                        var to_county_id = $(this).attr('data-to-county');
                        var start_time = $(this).attr('data-start-time');
                        var end_time = $(this).attr('data-end-time');
                        var data = {
                            'from_city_id': from_city_id,
                            'from_county_id': from_county_id,
                            'to_city_id': to_city_id,
                            'to_county_id': to_county_id,
                            start_time: start_time,
                            end_time: end_time

                        };
                        $.ajax({
                            type: 'get',
                            url: url,
                            dataType: 'json',
                            data: data,
                            beforeSend: function () {
                                layer.load()
                            },
                            success: function (res) {
                                $('.popup-tbody').html('')
                                var data = res.data;
                                var vehicle_name_list = data.vehicle_name_list;
                                var vehicle_ret = data.vehicles_ret;
                                var vehicles_all_ret = data.vehicles_all_ret
                                console.log(vehicle_ret);
                                that.radar_chart_init($('#radar_charts_container'), vehicle_name_list, vehicle_ret, vehicles_all_ret);
                                for (var i = 0; i < vehicle_name_list.length; i++) {
                                    var str = '<tr>';
                                    str += '<td>' + vehicle_name_list[i] + '</td>';
                                    str += '<td>' + vehicle_ret[i] + '人</td>';
                                    str += '<td>' + vehicles_all_ret[i] + '人</td>';
                                    str += '<tr>';
                                    $('.popup-tbody').append(str)
                                }
                                if ($('.popup-tbody').html() != '') {
                                    layer.open({
                                        type: 1,
                                        title: '运力统计车型雷达图',
                                        content: $('#popup'),
                                        shadeClose: true,
                                        area: ['1300px', '540px'],
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
                    });
                    common.clearSelect()
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
            end_time = common.timeTransform(end_time + ' 23:59:59')
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
                var vehicle_name_list = res.data.vehicle_name_list;
                var vehicles_all_ret = res.data.vehicles_all_ret
                $('.transport-tbody').html('');
                if (vehicle_name_list.length > 0) {
                    that.radar_chart_init($('#charts_container_two'), vehicle_name_list, vehicles_ret, vehicles_all_ret);
                    for (var i = 0; i < vehicle_name_list.length; i++) {
                        var str = '<tr>';
                        str += '<td>' + vehicle_name_list[i] + '</td>';
                        str += '<td>' + vehicles_ret[i] + '人</td>';
                        str += '<td>' + vehicles_all_ret[i] + '人</td>';
                        str += '<tr>';
                        $('.transport-tbody').append(str)
                    }
                } else {
                    return false;
                }
            }, function () {
                layer.closeAll('loading')
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
        var auth_role = $('#user-info').attr('data-role-type');
        if (!!auth_role && auth_role == 1) {
            $('#super_manager_area').css({'display': 'block'});
            $('#super_manager_area_select_zero').address({
                level: 3,
                offsetLeft: '-124px',
            });
        } else {
            $('#super_manager_area').css({'display': 'none'});
            $('#city_manager_one').css({'display': 'block'})
        }
    }
};
dataSet.area_select();
dataSet.dataRender();
dataSet.init();
dataSet.chart_request();
$('#search_btn').on('click', function (e) {
    e.preventDefault();
    dataSet.chart_request()
});
$('#transport_search_box').click(function (e) {
    e.preventDefault();
    var from_province_id = $('#start_place').attr('provinceid');
    var from_city_id = $('#start_place').attr('cityid');
    var to_province_id = $('#end_place').attr('provinceid');
    var to_city_id = $('#end_place').attr('cityid');

    layui.use('layer', function () {
        var layer = layui.layer;
        var start_time = $('#start_time_show').val();
        var end_time = $('#end_time_show').val();
          if (from_province_id && !from_city_id) {
            layer.tips('必须选择到城市级别', '#start_place', {
                tips: [1, '#009688'],
                time: 4000
            });
            return
        }
        if (to_province_id && !to_city_id) {
            layer.tips('必须选择到城市级别', '#end_place', {
                tips: [1, '#009688'],
                time: 4000
            });
            return
        }
        if (start_time != '') {
            start_time = common.timeTransform(start_time + ' 00:00:00')
        }
        if (end_time != '') {
            end_time = common.timeTransform(end_time + ' 23:59:59')
        }
        var data = {
            from_city_id: from_city_id?from_city_id:'',
            to_city_id: to_city_id?to_city_id:'',
            calc_town: $('#computed_type').val(),
            start_time: start_time,
            end_time: end_time
        };
        var url = '/transport/list?from_city_id=' + data.from_city_id + '&to_city_id=' + data.to_city_id + '&calc_town=' + data.calc_town + '&start_time=' + data.start_time + '&end_time=' + data.end_time;
        dataSet.tableRender(url)
    })
})