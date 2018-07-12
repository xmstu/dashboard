var provinces = {
    "台湾": "taiwan",
    "河北": "130000",
    "山西": "140000",
    "辽宁": "210000",
    "吉林": "220000",
    "黑龙江": "230000",
    "江苏": "320000",
    "浙江": "340000",
    "安徽": "340000",
    "福建": "350000",
    "江西": "360000",
    "山东": "370000",
    "河南": "410000",
    "湖北": "420000",
    "湖南": "460000",
    "广东": "440000",
    "海南": "hainan",
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

function dataInit() {
    layui.use('layer', function () {
        var layer = layui.layer;
        var url = '/map/heat_map/';
        var data = {
            filter: $.trim($('#filter').val()),
            dimension: $.trim($('#dimension').val()),
            field: $.trim($('.heat-maps-tabs > li.active').attr('data-value')),
            region_id: ''
        };
        http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
            if (res.status == 100000) {
                var data = res.data;
                var data_reset = data.map_data;
                var max_value = data.max_value;
                var toolTipData = data.toolTipData;
                var ynameMap = [];
                for (var i = 0; i < data_reset.length; i++) {
                    ynameMap.push(data_reset[i].name);
                }
                var chart = echarts.init(document.getElementById('map_container'));
                var option = {
                    backgroundColor: '#f6f6f6',
                    title: {
                        text: '数据统计地图',
                        subtext: null,
                        link: null,
                        left: '30%',
                        textStyle: {
                            fontSize: 14,
                            fontWeight: 'normal',
                            fontFamily: "Microsoft YaHei",
                            color: 'red'
                        },
                        subtextStyle: null
                    }
                    , tooltip: {
                        trigger: 'item',
                        formatter: function (params) {
                            if (typeof(params.value)[2] == "undefined") {
                                var toolTiphtml = ''
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
                    dataRange: {
                        min: 0,
                        max: max_value + (max_value / 5),
                        text: ['High', 'Low'],
                        realtime: false,
                        calculable: true,
                        color: ['orangered', 'yellow', 'lightskyblue']
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
                        data: ynameMap,
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
                        filter: $.trim($('#filter').val()),
                        dimension: $.trim($('#dimension').val()),
                        field: $.trim($('.heat-maps-tabs > li.active').attr('data-value')),
                        region_id: provinces[params.name]
                    };
                    http.ajax.get(true, false, url, data_province, http.ajax.CONTENT_TYPE_2, function (res) {
                        if (res.status == 100000) {
                            console.log(res.data);
                            var data = res.data;
                            var map_data = data.map_data;
                            var city_toolTipData = data.toolTipData;
                            if (params.name in provinces) {
                                $.getJSON('/static/map/province/' + provinces[params.name] + '.json', function (data) {
                                    console.log(params.name);
                                    echarts.registerMap(params.name, data);
                                    var d = [];
                                    for (var i = 0; i < data.features.length; i++) {
                                        d.push({
                                            name: data.features[i].properties.name
                                        })
                                    }
                                    toolTipData=city_toolTipData
                                    d = map_data;
                                    pageSet.renderMap(params.name, d);
                                });
                            } else if (params.seriesName in provinces) {
                                if (special.indexOf(params.seriesName) >= 0) {
                                    pageSet.renderMap('china', mapdata);
                                } else {
                                    $.getJSON('/static/map/city/' + cityMap[params.name] + '.json', function (data) {
                                        console.log(cityMap[params.name]);
                                        var city_data = {
                                            filter: $.trim($('#filter').val()),
                                            dimension: $.trim($('#dimension').val()),
                                            field: $.trim($('.heat-maps-tabs > li.active').attr('data-value')),
                                            region_id: cityMap[params.name]
                                        };
                                        http.ajax.get(true, false, url, city_data, http.ajax.CONTENT_TYPE_2, function (res) {
                                            console.log(res.data)
                                            if (res.status == 100000) {
                                                var city_data = res.data;
                                                var city_map_data = city_data.map_data;
                                                var city_map_tooltip = city_data.ToolTipData;
                                                echarts.registerMap(params.name, data);
                                                var d = [];
                                                for (var i = 0; i < data.features.length; i++) {
                                                    d.push({
                                                        name: data.features[i].properties.name
                                                    })
                                                }
                                                toolTipData=city_map_tooltip
                                                d = city_map_data;
                                                pageSet.renderMap(params.name, d);
                                            }
                                        });
                                    });
                                }
                            } else {
                                pageSet.renderMap('china', mapdata);
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
                        $('#date_show_one').val(String(common.getNowFormatDate()[2]));
                        $('#date_show_two').val(String(common.getNowFormatDate()[3]));
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
                                ready: function () {

                                },
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
                                ready: function () {

                                },
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
                                        areaColor: 'yellow'
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
                                data: data_reset
                            }
                        ];
                        chart.setOption(option);
                    },
                    tab: function () {
                        var lis = $('.heat-maps-tabs > li');
                        lis.click(function () {
                            $(this).addClass('active').siblings('li').removeClass('active')
                        })
                    }
                };
                pageSet.init();
                pageSet.tab();
            } else {
                layer.msg('error')
            }
        })
    })

}

dataInit();
$('#search_btn').click(function (e) {
    e.preventDefault();
});