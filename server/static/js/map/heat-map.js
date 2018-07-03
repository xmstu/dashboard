var setAbout = {
  init:function(){
      $('.map-menu-about>a').addClass('selected-active');
      $('.map-menu-about>a>i').addClass('select-active');
      layui.use(['form','table','layer','element'],function(){
          var form = layui.form;
          var table = layui.table;
          var layer = layui.layer;
          var element = layui.element;
      })
  }
};
$('#search_btn').click(function(e){
    e.preventDefault();
});
setAbout.init();
var provinces = {
    //23个省
    "台湾": "taiwan",
    "河北": "hebei",
    "山西": "shanxi",
    "辽宁": "liaoning",
    "吉林": "jilin",
    "黑龙江": "heilongjiang",
    "江苏": "jiangsu",
    "浙江": "zhejiang",
    "安徽": "anhui",
    "福建": "fujian",
    "江西": "jiangxi",
    "山东": "shandong",
    "河南": "henan",
    "湖北": "hubei",
    "湖南": "hunan",
    "广东": "guangdong",
    "海南": "hainan",
    "四川": "sichuan",
    "贵州": "guizhou",
    "云南": "yunnan",
    "陕西": "shanxi1",
    "甘肃": "gansu",
    "青海": "qinghai", //5个自治区
    "新疆": "xinjiang",
    "广西": "guangxi",
    "内蒙古": "neimenggu",
    "宁夏": "ningxia",
    "西藏": "xizang", //4个直辖市
    "北京": "beijing",
    "天津": "tianjin",
    "上海": "shanghai",
    "重庆": "chongqing", //2个特别行政区
    "香港": "xianggang",
    "澳门": "aomen"
};
var toolTipData = [
    {name: "北京", value: [{name: "货源量", value: 177}]},
    {name: "天津", value: [{name: "货源量", value: 42}]},
    {name: "河北", value: [{name: "货源量", value: 102}]},
    {name: "山西", value: [{name: "货源量", value: 81}]},
    {name: "内蒙古", value: [{name: "货源量", value: 47}]},
    {name: "辽宁", value: [{name: "货源量", value: 67}]},
    {name: "吉林", value: [{name: "货源量", value: 82}]},
    {name: "黑龙江", value: [{name: "货源量", value: 66}]},
    {name: "上海", value: [{name: "货源量", value: 50}]},
    {name: "江苏", value: [{name: "货源量", value: 50}]},
    {name: "浙江", value: [{name: "货源量", value: 50}]},
    {name: "安徽", value: [{name: "货源量", value: 50}]},
    {name: "福建", value: [{name: "货源量", value: 50}]},
    {name: "江西", value: [{name: "货源量", value: 50}]},
    {name: "山东", value: [{name: "货源量", value: 50}]},
    {name: "河南", value: [{name: "货源量", value: 50}]},
    {name: "湖北", value: [{name: "货源量", value: 50}]},
    {name: "湖南", value: [{name: "货源量", value: 50}]},
    {name: "重庆", value: [{name: "货源量", value: 50}]},
    {name: "四川", value: [{name: "货源量", value: 50}]},
    {name: "贵州", value: [{name: "货源量", value: 50}]},
    {name: "云南", value: [{name: "货源量", value: 50}]},
    {name: "西藏", value: [{name: "货源量", value: 50}]},
    {name: "陕西", value: [{name: "货源量", value: 50}]},
    {name: "甘肃", value: [{name: "货源量", value: 50}]},
    {name: "青海", value: [{name: "货源量", value: 50}]},
    {name: "宁夏", value: [{name: "货源量", value: 50}]},
    {name: "新疆", value: [{name: "货源量", value: 50}]},
    {name: "广东", value: [{name: "货源量", value: 50}]},
    {name: "广西", value: [{name: "货源量", value: 50}]},
    {name: "海南", value: [{name: "货源量", value: 50}]},
];
var geoCoordMap = {};
var max = 480,
    min = 9; // todo
var maxSize4Pin = 50,
    minSize4Pin = 20;

//直辖市和特别行政区-只有二级地图，没有三级地图
var special = ["北京", "天津", "上海", "重庆", "香港", "澳门"];
var mapdata = [];
var data_ano = []
var data_reset = [
    {name: "北京", value: 177},
    {name: "天津", value: 42},
    {name: "河北", value: 102},
    {name: "山西", value: 81},
    {name: "内蒙古", value: 47},
    {name: "辽宁", value: 67},
    {name: "吉林", value: 82},
    {name: "黑龙江", value: 66},
    {name: "上海", value: 24},
    {name: "江苏", value: 92},
    {name: "浙江", value: 14},
    {name: "安徽", value: 19},
    {name: "福建", value: 16},
    {name: "江西", value: 91},
    {name: "山东", value: 119},
    {name: "河南", value: 137},
    {name: "湖北", value: 116},
    {name: "湖南", value: 114},
    {name: "重庆", value: 91},
    {name: "四川", value: 125},
    {name: "贵州", value: 62},
    {name: "云南", value: 83},
    {name: "西藏", value: 92},
    {name: "陕西", value: 80},
    {name: "甘肃", value: 56},
    {name: "青海", value: 10},
    {name: "宁夏", value: 18},
    {name: "新疆", value: 67},
    {name: "广东", value: 13},
    {name: "广西", value: 59},
    {name: "海南", value: 14},
];
var ynameMap = [];
for (var i = 0; i < data_reset.length; i++) {
    ynameMap.push(data_reset[i].name);
}

var chart = echarts.init(document.getElementById('map_container'));
var option = {
    backgroundColor: '#fff',
    activeArea: []
    , title: {
        text: '数据统计地图'
        , subtext: null
        , link: null
        , left: 'center'
        , textStyle: {
            color: '#fff',
            fontSize: 14,
            fontWeight: 'normal',
            fontFamily: "Microsoft YaHei"
        }
        , subtextStyle: {
            color: '#ccc'
            , fontSize: 13
            , fontWeight: 'normal'
            , fontFamily: "Microsoft YaHei"
        }
    }
    , tooltip: {
        trigger: 'item',
        formatter: function (params) {
            if (typeof(params.value)[2] == "undefined") {
                var toolTiphtml = ''
                for (var i = 0; i < toolTipData.length; i++) {
                    if (params.name == toolTipData[i].name) {
                        toolTiphtml += toolTipData[i].name + ':<br>'
                        for (var j = 0; j < toolTipData[i].value.length; j++) {
                            toolTiphtml += toolTipData[i].value[j].name + ':' + toolTipData[i].value[j].value + "<br>"
                        }
                    }
                }
                return toolTiphtml;
            } else {
                var toolTiphtml = ''
                for (var i = 0; i < toolTipData.length; i++) {
                    if (params.name == toolTipData[i].name) {
                        toolTiphtml += toolTipData[i].name + ':<br>'
                        for (var j = 0; j < toolTipData[i].value.length; j++) {
                            toolTiphtml += toolTipData[i].value[j].name + ':' + toolTipData[i].value[j].value + "<br>"
                        }
                    }
                }
                return toolTiphtml;
            }
        }
    }
    , toolbox: {
        show: true
        , orient: 'vertical'
        , left: 'right'
        , top: 'center'
        , feature: {
            dataView: {
                readOnly: false
            }
            , restore: {}
            , saveAsImage: {}
        }
        , iconStyle: {
            normal: {
                color: '#fff'
            }
        }
    },
    visualMap: {
        show: true,
        min: 0,
        max: 200,
        left: 'left',
        top: 'bottom',
        seriesIndex: [1],
        text: ['高', '低'],
        calculable: true,
        colorLightness: [0.2, 100],
        color: ['#c05050', '#e5cf0d', '#5ab1ef'],
    },
    xAxis: {
        gridIndex: 0,
        axisTick: {
            show: false
        },
        axisLabel: {
            show: false
        },
        splitLine: {
            show: false
        },
        axisLine: {
            show: false
        }
    },
    yAxis: {
        gridIndex: 0,
        interval: 0,
        data: ynameMap,
        axisTick: {
            show: false
        },
        axisLabel: {
            show: true
        },
        splitLine: {
            show: false
        },
        axisLine: {
            show: false,
            lineStyle: {
                color: "#00effc"
            }
        }
    },
    grid: {
        right: 20,
        top: 100,
        bottom: 40,
        width: '24%'
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
    echarts.registerMap('china', data);
    pageSet.renderMap('china', d);
});
chart.on('click', function (params) {
    if (params.name in provinces) {
        $.getJSON('/static/map/province/' + provinces[params.name] + '.json', function (data) {
            echarts.registerMap(params.name, data);
            var d = [];
            for (var i = 0; i < data.features.length; i++) {
                d.push({
                    name: data.features[i].properties.name
                })
            }
            pageSet.renderMap(params.name, d);
        });
    } else if (params.seriesName in provinces) {
        if (special.indexOf(params.seriesName) >= 0) {
            pageSet.renderMap('china', mapdata);
        } else {
            $.getJSON('/static/map/city/' + cityMap[params.name] + '.json', function (data) {
                echarts.registerMap(params.name, data);
                var d = [];
                for (var i = 0; i < data.features.length; i++) {
                    d.push({
                        name: data.features[i].properties.name
                    })
                }
                pageSet.renderMap(params.name, d);
            });
        }
    } else {
        pageSet.renderMap('china', mapdata);
    }
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
                console.log(geoCoordMap)
            }
        })
    },
    renderMap: function (map, data) {
        data = data_reset;
        option.title.subtext = map;
        option.series = [
            {
                name: '散点',
                type: 'scatter',
                coordinateSystem: 'geo',
                label: {
                    normal: {
                        formatter: '{b}',
                        position: 'center',
                        show: true
                    },
                    emphasis: {
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        color: '#05C3F9'
                    }
                }
            },
            {
                name: map
                , type: 'map'
                , mapType: map
                , roam: false,
                aspectScale: 0.70,
                geoIndex: 0,
                left: '1%',
                top: 10,
                width: '64%',
                height: '90%',
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
                            color: '#fff'
                            , fontSize: 13
                        }
                    }
                }
                , itemStyle: {
                    normal: {
                        areaColor: '#323c48'
                        , borderColor: 'dodgerblue'
                    }
                    , emphasis: {
                        areaColor: 'darkorange'
                    }
                }
                , data: data
            },
            {
                name: '数量排名',
                type: 'bar',
                top: 10,
                right: 'right',
                xAxisIndex: 0,
                yAxisIndex: 0,
                barWidth: '35%',
                itemStyle: {
                    normal: {
                        color: '#00effc'
                    }
                },
                label: {
                    normal: {
                        show: true,
                        position: "bottom",
                        textStyle: {
                            color: "#00effc"
                        }
                    }
                },
                data: data_reset
            },

        ];
        chart.setOption(option);
    }
};

function chartsRender(data) {

}

function converData(data) {
    pageSet.init();
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var geoCoord = geoCoordMap[data[i].name];
        if (geoCoord) {
            console.log('success')
            res.push({
                name: data[i].name,
                value: geoCoord.concat(data[i].value)
            });
        }

    }
    return res;
}

pageSet.init()
console.log(converData(JSON.stringify(data_reset)));
