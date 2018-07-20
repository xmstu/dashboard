$(window).load(function () {
    $('.main-content-right').addClass('animated fadeIn')
});
var set = {
    init: function () {
        layui.use('laydate', function () {
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
        var that = this;
        $('#date_show_one').val(common.getNowFormatDate()[5]);
        $('#date_show_two').val(common.getNowFormatDate()[0]);
        $('.price-menu-about>a').addClass('selected-active');
        $('.price-menu-about>a>i').addClass('select-active');
        that.chartRender();
        that.dataInit();
        that.tableRender()
        $('#start_address').address({
            level: 3
        });
        $('#end_address').address({
            level: 3,
            offsetLeft: '-124px'
        });
    },
    chartRender: function (price_trend_series, xAxis_data, avg_price) {
        var dom = document.getElementById("charts_container");
        var myChart = echarts.init(dom);
        var config = {
            col: {
                up: 'rgb(153, 14, 14)',
                down: '#19b34c',
                m5: '#f00',
                m10: 'yellow',
                m30: '#dd1ce0'
            },
            st: 10,
            ed: 40
        };
        option = {
            backgroundColor: config.bg,
            // color: '#fff',
            title: {
                text: null
            },
            tooltip: {
                trigger: 'axis',
                position: [10, '70%'],
                formatter: function (params) {
                    var res = params[0].seriesName + ' ' + params[0].name;
                    var resAno = params[1].seriesName;
                    resAno += "￥" + params[1].value;
                    res += '<br/>最高 : ￥' + params[0].value[3];
                    res += '<br/>最低 : ￥' + params[0].value[2];
                    return res + '<br>' + resAno;
                },
                borderWidth: 1,
                textStyle: {
                    color: '#fff',
                    width: '100%'
                },
                axisPointer: {
                    type: 'cross',
                    label: {
                        show: true,
                        color: '#ff0'
                    },
                    crossStyle: {
                        type: 'solid'
                    }
                }
            },
            legend: {
                data: ['价格波动', '日平均值']
            },
            grid: [{
                top: '10%',
                left: '5%',
                right: '5%',
                height: '76%'
            }, {
                top: '86%',
                left: '5%',
                right: '5%',
                height: '0%'
            }],
            axisPointer: {
                link: {
                    xAxisIndex: 'all'
                },
                label: {
                    backgroundColor: '#777'
                }
            },
            xAxis: [{
                type: 'category',
                axisLine: {
                    onZero: false
                },
                axisLabel: {
                    show: true
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    show: true
                },
                data: xAxis_data
            }, {
                type: 'category',
                gridIndex: 1,
                axisTick: {
                    show: false
                },
                axisLabel: {
                    show: false
                }
            }],
            //
            yAxis: [{
                axisLabel: {
                    color: config.col.y
                },
                scale: true,
                position: 'left',
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: ['#888'],
                        type: 'dotted'
                    }
                }
            }, {
                gridIndex: 1,
                position: 'left',
                xAxisIndex: 1,
                splitArea: {
                    show: false
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: ['#888'],
                        type: 'dotted'
                    }
                },
                axisLabel: {
                    color: config.col.y
                }
            }],

            dataZoom: [{
                type: 'inside',
                show: true,
                xAxisIndex: [0, 1],
                start: config.st,
                end: config.ed
            }, {
                show: true,
                type: 'slider',
                xAxisIndex: [0, 1],
                y: '94%',
                start: config.st,
                end: config.ed
            }],
            series: [
                {
                    type: 'k', //Candlestick
                    name: '价格波动',
                    itemStyle: {
                        normal: {
                            color: config.col.up, //阳线填充色
                            color0: config.col.down,
                            borderColor: config.col.up, //阳线边框色
                            borderColor0: config.col.down
                        }
                    },
                    data: price_trend_series
                },
                {
                    type: 'line',
                    name: '日平均值',
                    data: avg_price,
                    lineStyle: {
                        normal: {
                            color: config.col.m5
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: config.col.m5
                        }
                    }
                }
            ]
        };
        if (option && typeof option === "object") {
            myChart.setOption(option, true)
        }
    },
    dataInit: function () {
        var that = this
        layui.use(['layer', 'laydate'], function () {
            var layer = layui.layer;
            var laydate = layui.laydate;
            var url = '/price/price_trend/'
            var start_time = $('#date_show_one').val();
            var end_time = $('#date_show_two').val();
            if (start_time != '') {
                start_time = common.timeTransform(start_time + ' 00:00:00')
            }
            if (end_time != '') {
                end_time = common.timeTransform(end_time + ' 23:59:59')
            }
            var data = {
                from_province_id: $('#start_address').attr('provinceid') == undefined ? '' : $('#start_address').attr('provinceid'),
                from_city_id: $('#start_address').attr('cityid') == undefined ? '' : $('#start_address').attr('cityid'),
                from_county_id: $('#end_address').attr('districtsid') == undefined ? '' : $('#end_address').attr('districtsid'),
                to_province_id: $('#end_address').attr('provinceid') == undefined ? '' : $('#end_address').attr('provinceid'),
                to_city_id: $('#end_place').attr('cityid') == undefined ? '' : $('#end_place').attr('cityid'),
                to_country_id: $('#end_place').attr('districtsid') == undefined ? '' : $('#end_place').attr('districtsid'),
                min_mileage: $('#min_mileage').val(),
                max_mileage: $('#max_mileage').val(),
                vehicle_length: $('#vehicle_type').val(),
                pay_method: $('#pay_methods').val(),
                start_time: start_time,
                end_time: end_time
            }
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                console.log(res)
                var avg_price = res.data.avg_price;
                var xAxis = res.data.xAxis;
                var price_trend_series = res.data.price_trend_series;
                that.chartRender(price_trend_series, xAxis, avg_price)
            })
        })
    }
};
set.init();
$('#search_btn').click(function (e) {
    e.preventDefault()
    set.dataInit();
    console.log($('#date_show_one').val())
})
/*
$(window).load(function () {
    $('.main-content-right').addClass('animated fadeIn')
});
var dom = document.getElementById("charts_container");
var myChart = echarts.init(dom);
var datas = splitData([
    ['2017-1-3', 21.37, 20.99, 20.9, 21.37],
    ['2017-1-4', 20.92, 21.17, 20.84, 21.24],
    ['2017-1-5', 21.15, 20.99, 20.95, 21.18],
    ['2017-1-6', 20.98, 20.69, 20.68, 21.07],
    ['2017-8-18', 16.52, 17.26, 16.51, 17.38],
    ['2017-8-21', 17.15, 17.2, 16.98, 17.23],
    ['2017-8-22', 17.2, 17.33, 17.13, 17.71]
]);
// 获取对应的数据格式
function splitData(rawData) {
    var categoryData = [],
        values = [],
        nows = [];
    for (var i = 0; i < rawData.length; i++) {
        categoryData.push(rawData[i].splice(0, 1)[0]); //日期
        nows.push(rawData[i][3]-0.23); //日期
        values.push(rawData[i]) //开，收，低，高
    }
    return {
        categoryData: categoryData,
        now: nows,
        values: values
    };
}
// 平均值
function calculateMA(dayCount) {
    var result = [];
    for (var i = 0, len = datas.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += datas.values[i - j][1];
        }
        result.push((sum / dayCount).toFixed(2));
    }
    return result;
}
// 下面折线图的数据
function calculateSA() {
    var result = [];
    result.push(0);
    for (var i = 0, len = datas.values.length; i < len; i++) {
        if (i > 0) {
            var k = Math.abs(datas.values[i][3] - datas.values[i][2]) / datas.values[i - 1][1] * 100;
            result.push(k.toFixed(2));
        }
    }
    return result;
}
// 下面柱状图的数据
function calculateUD() {
    var result = [];
    result.push(0);
    for (var i = 0, len = datas.values.length; i < len; i++) {
        if (i > 0) {
            var k = (datas.values[i][1] - datas.values[i - 1][1]) / datas.values[i - 1][1] * 100;
            result.push(k.toFixed(2));
        }
    }
    return result;
}
var config = {
    // barWidth: 10,//指定柱宽度
    col: {
        up: 'rgb(153, 14, 14)',
        down: '#19b34c',
        m5: '#f00',
        m10: 'yellow',
        m30: '#dd1ce0',
        // y: '#ffefef'
    },
    // bg: '#000',
    st: 10,
    ed: 40
}
option = {
    backgroundColor: config.bg,
    // color: '#fff',
    title: {
        text: 'k线'
    },

    // 提示框浮层的位置
    tooltip: {
        trigger: 'axis',
        position: [10, '70%'],
        formatter: '{a0}:{c0}  {a1}:{c1} {a2}:{c2}',
        // formatter:function(params){
        //     return params.data
        // },
        // backgroundColor: '#fff',
        borderWidth: 1,
        textStyle: {
            color: '#fff',
            width: '100%'
        },
        // 坐标轴指示器配置项
        axisPointer: {
            type: 'cross',
            label: {
                show: true,
                color: '#ff0',
                rich: {
                    a: {
                        // 没有设置 `lineHeight`，则 `lineHeight` 为 56
                    }
                }
                // formatter: function(params) {
                //     // 假设此轴的 type 为 'time'。
                //     return 'some text' + params.value;
                // },
            },
            crossStyle: {
                type: 'solid'
            },

        }
    },
    legend: {
        data: ['分时', '日K', '5日平均线', '10日平均线', '30日平均线', '振幅', '增加']
    },
    grid: [{
        top: '10%',
        // show:true,
        left: '5%', //grid 组件离容器左侧的距离。
        right: '5%',
        height: '76%',
        // borderColor:'#ccc',
    }, {
        top: '86%',
        left: '5%',
        right: '5%',
        height: '0%',
    }],
    axisPointer: {

        link: {
            xAxisIndex: 'all'
        },
        label: {
            backgroundColor: '#777'
        },
        // triggerOn:'click'
    },
    // 上下两个图表的x轴数据
    xAxis: [{
        type: 'category',
        // scale: true,
        // 坐标轴两边留白策略，类目轴和非类目轴的设置和表现不一样。
        // boundaryGap: false,
        axisLine: {
            // show: false,
            onZero: false
        },
        axisLabel: {
            show: true
        },
        axisTick: {
            show: false
        },
        splitLine: {
            show: true
        },
        data: datas.categoryData
    }, {
        type: 'category',
        //boundaryGap: false,
        gridIndex: 1,
        axisTick: {
            show: false
        },
        axisLabel: {
            show: false
        },
        data: datas.categoryData
    }],
    //
    yAxis: [{
        axisLabel: {
            color: config.col.y
        },
        scale: true,
        position: 'left',
        // splitArea: {
        //     show: false
        // },
        splitLine: {
            show: true,
            lineStyle: {
                color: ['#888'],
                type: 'dotted'
            }
        }
        // splitNumber: 10
    }, {
        gridIndex: 1,
        position: 'left',
        xAxisIndex: 1,
        //splitNumber: 3,
        splitArea: {
            show: false
        },
        splitLine: {
            show: true,
            lineStyle: {
                color: ['#888'],
                type: 'dotted'
            }
        },
        axisLabel: {
            // show: true,
            color: config.col.y
        }
    }],

    dataZoom: [{
        type: 'inside',
        show:true,
        xAxisIndex: [0, 1],
        start: config.st,
        end: config.ed
    }, {
        show: true,
        type: 'slider',
        xAxisIndex: [0, 1],
        y: '94%',
        start: config.st,
        end: config.ed
    }],
    series: [
        {
            type: 'line',
            name: '5日平均线',
            data: calculateMA(1),
            lineStyle: {
                normal: {
                    color: config.col.m5
                }
            },
            itemStyle: {
                normal: {
                    color: config.col.m5
                }
            }
        },
        {
            type: 'k', //Candlestick
            name: '日K',
            // barWidth: config.barWidth, //指定柱宽度
            itemStyle: {
                normal: {
                    color: config.col.up, //阳线填充色
                    color0: config.col.down,
                    borderColor: config.col.up, //阳线边框色
                    borderColor0: config.col.down
                }
            },
            data: datas.values
        }
    ]
};
console.log(calculateUD());
if (option && typeof option === "object") {
    myChart.setOption(option, true)
}*/
