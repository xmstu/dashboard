var dataSet = {
    init: function () {
        var that = this;
        $('#date_show_three').val(String(common.getNowFormatDate()[2]));
        $('#date_show_four').val(String(common.getNowFormatDate()[3]));
        setTimeout(function () {
            $('.layui-form-item .layui-inline ').css({'margin-right': 0});
            $('.part-2').css({'padding-top': '0px', 'border-top': 0});
            $('.transport-menu-about>a').addClass('selected-active')
            that.radar_chart_init();
            that.dateRender();
        }, 10);
        $('#area_select').address({
            offsetLeft: '0',
            level: 3,
            onClose: function () {
            }
        });
    },
    dateRender: function () {
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
            table.render({
                elem: '#LAY_table_user'
                , url: '/transport/list/',
                even: true,
                response: {
                    statusName: 'status',
                    statusCode: 100000
                },
                done: function (res, curr, count) {

                }
                , cols: [[
                    {field: 'id', title: '业务类型', sort: true},
                    {field: 'user_name', title: '出发地', width: 350}
                    , {field: 'mobile', title: '目的地', width: 350}
                    , {field: 'user_type', title: '里程'}
                    , {field: 'role_auth', title: '货源量'}
                    , {field: 'usual_city', title: '车辆数'}
                    , {field: 'goods_count', title: '接单量'}
                    , {field: 'order_count', title: '图表'}
                ]]
                , id: 'testReload'
                , page: true
            });
        });
    },
    radar_chart_init: function (categories,order_ret,vehicles_ret,goods_ret) {
        Highcharts.setOptions({
            colors: ['#37A2DA', '#32C5E9', '#67E0E3', '#9FE6B8', '#FFDB5C', '#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF']
        });
        $('#charts_container_two').highcharts({
            chart: {
                polar: true,
                type: 'line'
            },
            title: {
                text: '运力雷达图',
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
            series: [{
                name: '实际接单',
                data: order_ret,
                pointPlacement: 'on',
                type: 'area'
            }, {
                name: '车辆数',
                data:vehicles_ret,
                pointPlacement: 'on',
                type: 'line'
            }, {
                name: '货源量',
                data: goods_ret,
                pointPlacement: 'on',
                type: 'area'
            }]
        })
    },
    chart_request: function () {
        var that = this;
        var url = '/transport/radar/';
        var start_time =  $('#date_show_three').val();
        var end_time = $('#date_show_four').val();
        if(start_time!=''){
            start_time=common.timeTransform(start_time+' 00:00:00')
        }
        if(end_time!=''){
            end_time=common.timeTransform(end_time+' 00:00:00')
        }
        var data = {
            start_time:start_time,
            end_time: end_time,
            region_id: $('#region_id').val(),
            business: $('#business').val()
        };
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var vehicles_ret = res.data.vehicles_ret;
                var goods_ret = res.data.goods_ret;
                var orders_ret = res.data.orders_ret;
                var vehicle_name_list = res.data.vehicle_name_list;
                if(vehicle_name_list.length>0){
                  that.radar_chart_init(vehicle_name_list,orders_ret,vehicles_ret,goods_ret);
                  for(var i =0;i<vehicle_name_list.length;i++){
                      var str='<tr>';
                      str+='<td>'+vehicle_name_list[i]+'</td>';
                      str+='<td>'+goods_ret[i]+'单</td>';
                      str+='<td>'+vehicles_ret[i]+'辆</td>';
                      str+='<td style="color: #44c660;font-weight: bold;">'+orders_ret[i]+'单</td>';
                      str+='<td style="color: #f40;font-weight: bold;">'+that.transition(goods_ret[i],orders_ret[i])+'</td>';
                      str+='<tr>';
                      $('.transport-tbody').append(str)
                  }

                }else {
                    return false;
                }
            })
        });

    },
    transition:function(val1,val2){
        if(val1>0){
            var result = (val2/val1*100).toFixed(2)+'%'
        }
        if(val1==0||val2==0) {
            result=0;
        }
        return result
    }

};
dataSet.init()
dataSet.chart_request()