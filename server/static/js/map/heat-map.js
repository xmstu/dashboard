var provinces = {
    "台湾": "taiwan",
    "河北": "130000",
    "山西": "140000",
    "辽宁": "210000",
    "吉林": "220000",
    "黑龙江": "230000",
    "江苏": "320000",
    "浙江": "330000",
    "安徽": "340000",
    "福建": "350000",
    "江西": "360000",
    "山东": "370000",
    "河南": "410000",
    "湖北": "420000",
    "湖南": "460000",
    "广东": "440000",
    "海南": "150300",
    "四川": "510000",
    "贵州": "520000",
    "云南": "530000",
    "陕西": "610000",
    "甘肃": "620000",
    "青海": "630000", //5个自治区
    "新疆": "650000",
    "广西": "450000",
    "内蒙古": "150000",
    "宁夏": "640000",
    "西藏": "540000", //4个直辖市
    "北京": "110000",
    "天津": "120000",
    "上海": "310000",
    "重庆": "500000", //2个特别行政区
    "香港": "810000",
    "澳门": "820000"
};
var geoCoordMap = {};
var max = 480,
    min = 9; // todo
var mapdata = [];
var data_ano = [];
$('.main-content-right').addClass('animated fadeIn');
var special = ["北京", "天津", "上海", "重庆", "香港", "澳门"];
var set = {
    init: function () {
        $('#date_show_one').val(String(common.getNowFormatDate()[2]));
        $('#date_show_two').val(String(common.getNowFormatDate()[3]));
    },
    dataInit: function () {
        var that = this;
        layui.use(['form', 'layer'], function () {
            var layer = layui.layer;
            var form = layui.form;
            that.init();
            var start_time = common.timeTransform($('#date_show_one').val() + ' 00:00:00');
            var end_time = common.timeTransform($('#date_show_two').val() + ' 23:59:59');
            form.on('select(methods_select)', function (data) {
                if (data.value == '1') {
                    $('#filter').removeClass('none').addClass('area-select-options-setting');
                    $('#vehicle_select').addClass('none').removeClass('area-select-options-setting');
                    $('#role_select').addClass('none').removeClass('area-select-options-setting');
                    $('#heat_maps_tabs').removeClass('none').addClass('map-select-options-setting');
                    $('#heat_maps_tabs_one').addClass('none').removeClass('map-select-options-setting');
                    $('#heat_maps_tabs_two').addClass('none').removeClass('map-select-options-setting');
                } else if (data.value == '2') {
                    $('#role_select').removeClass('none').addClass('area-select-options-setting');
                    $('#filter').addClass('none').removeClass('area-select-options-setting');
                    $('#vehicle_select').addClass('none').removeClass('area-select-options-setting');
                    $('#heat_maps_tabs_one').removeClass('none').addClass('map-select-options-setting');
                    $('#heat_maps_tabs_two').addClass('none').removeClass('map-select-options-setting');
                    $('#heat_maps_tabs').addClass('none').removeClass('map-select-options-setting');
                } else if (data.value == '3') {
                    $('#vehicle_select').removeClass('none').addClass('area-select-options-setting');
                    $('#filter').addClass('none').removeClass('area-select-options-setting');
                    $('#role_select').addClass('none').removeClass('area-select-options-setting');
                    $('#heat_maps_tabs_two').removeClass('none').addClass('map-select-options-setting');
                    $('#heat_maps_tabs_one').addClass('none').removeClass('map-select-options-setting');
                    $('#heat_maps_tabs').addClass('none').removeClass('map-select-options-setting');
                }
            });
            var url = '/map/heat_map/';
            var area_select = $('.area-select-options-setting .layui-anim > dd.layui-this').attr('lay-value');
            var map_select = $('.map-select-options-setting .layui-anim > dd.layui-this').attr('lay-value');
            var data = {
                dimension: $.trim($('#dimension').val()),
                filter: area_select == undefined ? 0 : area_select,
                field: map_select == undefined ? 0 : map_select,
                start_time: start_time,
                end_time: end_time,
                region_id: ''
            };
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                    var data_reload = res.data
                    var roles = data_reload.authority_region_id;
                    var city_manager_map = data_reload.map_data;
                    var city_manager_tooltip = data_reload.toolTipData;
                    var city_manager_max_value = data_reload.max_value
                    if (data_reload.authority_region_id == 0) {
                        if (res.status == 100000) {
                            var data = res.data;
                            var data_reset = data.map_data;
                            var province_reset = data.map_data;
                            var max_value = data.max_value;
                            var toolTipData = data.toolTipData;
                            var chart = echarts.init(document.getElementById('map_container'));
                            var option = {
                                backgroundColor: '#f6f6f6',
                                title: {
                                    text: null,
                                    subtext: null,
                                    link: null,
                                    subtextStyle: null
                                }
                                , tooltip: {
                                    trigger: 'item',
                                    formatter: function (params) {
                                        if (typeof(params.value)[2] == "undefined") {
                                            var toolTiphtml = '';
                                            for (var i = 0; i < toolTipData.length; i++) {
                                                if (params.name == toolTipData[i].name) {
                                                    toolTiphtml += toolTipData[i].name + ':<br>';
                                                    for (var j = 0; j < toolTipData[i].value.length; j++) {
                                                        toolTiphtml += toolTipData[i].value[j].name + ':' + toolTipData[i].value[j].value + "<br>"
                                                    }
                                                }
                                            }
                                            return toolTiphtml;
                                        } else {
                                            var toolTiphtml = '';
                                            for (var i = 0; i < toolTipData.length; i++) {
                                                if (params.name == toolTipData[i].name) {
                                                    toolTiphtml += toolTipData[i].name + ':<br>';
                                                    for (var j = 0; j < toolTipData[i].value.length; j++) {
                                                        toolTiphtml += toolTipData[i].value[j].name + ':' + toolTipData[i].value[j].value + "<br>"
                                                    }
                                                }
                                            }
                                            return toolTiphtml;
                                        }
                                    }
                                },
                                visualMap: {
                                    min: 0,
                                    max: max_value + (max_value / 5),
                                    left: 'left',
                                    top: 'bottom',
                                    text: ['高', '低'], // 文本，默认为数值文本
                                    calculable: true,
                                    seriesIndex: [1],
                                    colorLightness: [0.2, 100],
                                    color: ['#c05050', '#e5cf0d', '#5ab1ef']
                                },
                                xAxis: {
                                    gridIndex: 0,
                                    axisTick: {
                                        show: true
                                    },
                                    axisLabel: {
                                        show: true
                                    },
                                    splitLine: {
                                        show: true
                                    },
                                    axisLine: {
                                        show: true
                                    }
                                },
                                yAxis: {
                                    data: ynameMap_(data_reset),
                                    axisTick: {
                                        show: true
                                    },
                                    axisLabel: {
                                        show: true
                                    },
                                    splitLine: {
                                        show: true
                                    },
                                    axisLine: {
                                        lineStyle: {
                                            color: "#009688"
                                        }
                                    }
                                },
                                grid: {
                                    right: '3%',
                                    top: 0,
                                    width: '16%'
                                },
                                animationDuration: 1000,
                                animationEasing: 'cubicOut',
                                animationDurationUpdate: 1000
                            };
                            $.getJSON('/static/map/china.json', function (data) {
                                d = [];
                                for (var i = 0; i < data.features.length; i++) {
                                    d.push({
                                        name: data.features[i].properties.name
                                    })
                                }
                                mapdata = d;
                                if (d.length != 0) {
                                    d = data_reset;
                                }
                                echarts.registerMap('china', data);
                                pageSet.renderMap('china', d);
                            });
                            chart.on('click', function (params) {
                                var data_province = {
                                    dimension: $.trim($('#dimension').val()),
                                    filter: area_select == undefined ? 0 : area_select,
                                    field: map_select == undefined ? 0 : map_select,
                                    region_id: provinces[params.name],
                                    start_time: start_time,
                                    end_time: end_time
                                };
                                http.ajax.get(true, false, url, data_province, http.ajax.CONTENT_TYPE_2, function (res) {
                                    if (res.status == 100000) {
                                        var data = res.data;
                                        var map_data = data.map_data;
                                        var city_toolTipData = data.toolTipData;
                                        var max_value_reset = data.max_value;
                                        if (params.name in provinces) {
                                            $.getJSON('/static/map/province/' + provinces[params.name] + '.json', function (data) {
                                                echarts.registerMap(params.name, data);
                                                var d = [];
                                                for (var i = 0; i < data.features.length; i++) {
                                                    d.push({
                                                        name: data.features[i].properties.name
                                                    })
                                                }
                                                toolTipData = city_toolTipData;
                                                data_reset = map_data;
                                                d = map_data;
                                                var data_length = d.length;
                                                var dataArr = [];
                                                if (data_length > 20) {
                                                    data_length = 20
                                                    for (var i = 0; i < data_length; i++) {
                                                        dataArr.push(d[i].name);
                                                    }
                                                } else if (data_length < 20) {
                                                    for (var i = 0; i < data_length; i++) {
                                                        dataArr.push(d[i].name);
                                                    }
                                                }
                                                option.visualMap.max = max_value_reset;
                                                option.yAxis.data = dataArr;
                                                pageSet.renderMap(params.name, d);
                                            });
                                        } else if (params.seriesName in provinces) {
                                            if (special.indexOf(params.seriesName) >= 0) {
                                                pageSet.renderMap('china', mapdata);
                                            } else {
                                                $.getJSON('/static/map/city/' + cityMap[params.name] + '.json', function (data) {
                                                    var city_data = {
                                                        dimension: $.trim($('#dimension').val()),
                                                        filter: area_select == undefined ? 0 : area_select,
                                                        field: map_select == undefined ? 0 : map_select,
                                                        region_id: cityMap[params.name],
                                                        start_time: start_time,
                                                        end_time: end_time
                                                    };
                                                    http.ajax.get(true, false, url, city_data, http.ajax.CONTENT_TYPE_2, function (res) {
                                                        if (res.status == 100000) {
                                                            var city_data = res.data;
                                                            var city_map_data = city_data.map_data;
                                                            var city_map_tooltip = city_data.toolTipData;
                                                            var max_value_reset1 = city_data.max_value;
                                                            echarts.registerMap(params.name, data);
                                                            var d = [];
                                                            for (var i = 0; i < data.features.length; i++) {
                                                                d.push({
                                                                    name: data.features[i].properties.name
                                                                })
                                                            }
                                                            toolTipData = city_map_tooltip;
                                                            data_reset = city_map_data;
                                                            d = city_map_data;
                                                            var dataArr_ = [];
                                                            var data_length_ = d.length;
                                                            if (data_length_ > 20) {
                                                                data_length_ = 20;
                                                                for (var i = 0; i < data_length_; i++) {
                                                                    dataArr_.push(d[i].name);
                                                                }
                                                            } else if (data_length_ < 20) {
                                                                for (var i = 0; i < data_length_; i++) {
                                                                    dataArr_.push(d[i].name);
                                                                }
                                                            }
                                                            option.yAxis.data = dataArr_;
                                                            option.visualMap.max = max_value_reset1;
                                                            pageSet.renderMap(params.name, d);
                                                        }
                                                    });
                                                });
                                            }
                                        } else {
                                            var province_length = province_reset.length;
                                            var province_arr = [];
                                            for (var l = 0; l < province_length; l++) {
                                                province_arr.push(province_reset[l].name)
                                            }
                                            option.yAxis.data = province_arr;
                                            option.visualMap.max = max_value + (max_value / 5);
                                            pageSet.renderMap('china', province_reset);
                                        }
                                    } else {
                                        layer.msg('接口请求异常')
                                    }
                                });

                            });
                            var pageSet = {
                                init: function () {
                                    $.ajax({
                                        url: '/static/map/china.json',
                                        dataType: 'json',
                                        type: 'get',
                                        success: function (res) {
                                            $.each(res.features, function (val, index) {
                                                $.each(index, function (v, i) {
                                                    var name = i.name;
                                                    geoCoordMap[name] = i.cp;
                                                    data_ano.push({
                                                        name: name,
                                                        value: Math.round(Math.random() * 100 + 10)
                                                    })
                                                })
                                            });
                                        }
                                    });

                                    $('.map-menu-about>a').addClass('selected-active');
                                    $('.map-menu-about>a>i').addClass('select-active');
                                    layui.use(['laydate', 'layer', 'form', 'table'], function () {
                                        var form = layui.form;
                                        var table = layui.table;
                                        var layer = layui.layer;
                                        var laydate = layui.laydate;
                                        laydate.render({
                                            elem: '#date_show_one',
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
                                            }
                                        });
                                    })

                                },
                                renderMap: function (map, data) {
                                    option.title.subtext = map;
                                    option.series = [
                                        {
                                            name: '散点',
                                            type: 'scatter',
                                            coordinateSystem: 'geo',
                                            label: {
                                                normal: {},
                                                emphasis: {}
                                            },
                                            itemStyle: {
                                                normal: {
                                                    color: '#009688'
                                                }
                                            }
                                        },
                                        {
                                            name: map
                                            , type: 'map'
                                            , mapType: map
                                            , roam: false,
                                            borderWidth: 1.6,
                                            aspectScale: 0.68,
                                            geoIndex: 0,
                                            left: '10%',
                                            top: '2%',
                                            width: '60%',
                                            height: '76%',
                                            nameMap: {
                                                'china': '中国'
                                            }
                                            , label: {
                                                normal: {
                                                    show: true
                                                    , textStyle: {
                                                        color: '#999'
                                                        , fontSize: 13
                                                    }
                                                }
                                                , emphasis: {
                                                    show: true
                                                    , textStyle: {
                                                        color: '#333'
                                                        , fontSize: 13
                                                    }
                                                }
                                            }
                                            , itemStyle: {
                                                normal: {
                                                    areaColor: '#fff'
                                                    , borderColor: 'skublue'
                                                }
                                                , emphasis: {
                                                    areaColor: 'darkorange'
                                                }
                                            }
                                            , data: data
                                        },
                                        {
                                            name: '数量排名',
                                            zlevel: 1,
                                            xAxisIndex: 0,
                                            yAxisIndex: 0,
                                            type: 'bar',
                                            barMaxWidth: 20,
                                            label: {
                                                normal: {
                                                    show: true,
                                                    position: 'right'
                                                },
                                                emphasis: {
                                                    show: true
                                                }
                                            },
                                            data: data
                                        }
                                    ];
                                    chart.setOption(option);
                                }
                            };
                            pageSet.init();
                        } else {
                            layer.msg('error')
                        }
                    } else if (data_reload.authority_region_id != 0) {
                        layui.use(['laydate', 'layer', 'form', 'table'], function () {
                            var form = layui.form;
                            var table = layui.table;
                            var layer = layui.layer;
                            var laydate = layui.laydate;
                            laydate.render({
                                elem: '#date_show_one',
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
                                }
                            });
                        })
                        var chart_container = echarts.init(document.getElementById('map_container'));
                        var mapdata = [];
                        $.getJSON('/static/map/city/' + roles + '.json', function (data) {
                            echarts.registerMap('hangzhou', data);
                            var d = [];
                            for (var i = 0; i < data.features.length; i++) {
                                d.push({
                                    name: data.features[i].properties.name
                                })
                            }
                            RenderMap('hangzhou', d);
                        });
                        var map_option = {
                            backgroundColor: '#f5f5f5',
                            title: {
                                text: null,
                                subtext: null,
                                link: null,
                                left: 'center',

                                subtextStyle: {
                                    color: '#ccc',
                                    fontSize: 13,
                                    fontWeight: 'normal',
                                    fontFamily: "Microsoft YaHei"
                                }
                            },
                            tooltip: {
                                trigger: 'item',
                                formatter: function (params) {
                                    var toolTiphtml = '';
                                    for (var i = 0; i < city_manager_tooltip.length; i++) {
                                        if (params.name == city_manager_tooltip[i].name) {
                                            toolTiphtml += city_manager_tooltip[i].name + ':<br>';
                                            for (var j = 0; j < city_manager_tooltip[i].value.length; j++) {
                                                toolTiphtml += city_manager_tooltip[i].value[j].name + ':' + city_manager_tooltip[i].value[j].value + "<br>"
                                            }
                                        }
                                    }
                                    return toolTiphtml;
                                }
                            },
                            visualMap: {
                                min: 0,
                                max: city_manager_max_value,
                                left: 'left',
                                top: 'bottom',
                                text: ['高', '低'], // 文本，默认为数值文本
                                calculable: true,
                                colorLightness: [0.2, 100],
                                color: ['skyblue', '#fff']
                            },
                            toolbox: {
                                show: true,
                                orient: 'vertical',
                                left: 'right',
                                top: 'center',
                                feature: {
                                    dataView: {readOnly: false},
                                    restore: {},
                                    saveAsImage: {}
                                },
                                iconStyle: {
                                    normal: {
                                        color: '#fff'
                                    }
                                }
                            },
                            /*------------------start----------------------*/
                            /*-------------------end-----------------------*/
                            animationDuration: 1000,
                            animationEasing: 'cubicOut',
                            animationDurationUpdate: 1000
                        };

                        function RenderMap(map, data) {
                            data = city_manager_map;
                            map_option.title.subtext = map;
                            map_option.series = [
                                {
                                    name: map,
                                    type: 'map',
                                    mapType: map,
                                    roam: false,
                                    nameMap: {
                                        'china': '中国'
                                    },
                                    label: {
                                        normal: {
                                            show: true,
                                            textStyle: {
                                                color: '#999',
                                                fontSize: 13
                                            }
                                        },
                                        emphasis: {
                                            show: true,
                                            textStyle: {
                                                color: '#fff',
                                                fontSize: 13
                                            }
                                        }
                                    },
                                    itemStyle: {
                                        normal: {
                                            areaColor: '#fff',
                                            borderColor: 'dodgerblue'
                                        },
                                        emphasis: {
                                            areaColor: 'darkorange'
                                        }
                                    },
                                    data: data
                                },

                            ];
                            //渲染地图
                            chart_container.setOption(map_option);
                        }
                    }

                    function ynameMap_(d) {
                        var ynameMap = [];
                        var data_length = d.length
                        if (data_length > 20) {
                            data_length = 20
                            for (var i = 0; i < data_length; i++) {
                                ynameMap.push(d[i].name);
                            }
                        } else if (data_length < 20) {
                            for (var i = 0; i < data_length; i++) {
                                ynameMap.push(d[i].name);
                            }
                        }
                        return ynameMap
                    }
                }
            )
        })
    }
};


set.dataInit();
$('#search_btn').click(function (e) {
    e.preventDefault();
    set.dataInit();
});