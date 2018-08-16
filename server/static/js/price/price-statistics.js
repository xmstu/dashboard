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
        $('#date_show_one').val(common.getNowFormatDate()[7]);
        $('#date_show_two').val(common.getNowFormatDate()[0]);
        $('.price-menu-about>a').addClass('selected-active');
        $('.price-menu-about>a>i').addClass('select-active');
        that.dataInit();
        $('#start_address').address({
            level: 3
        });
        $('#end_address').address({
            level: 3,
            offsetLeft: '-124px'
        });
    },
    chartRender: function (price_trend_series, avg_price) {
        var dom = document.getElementById("charts_container");
        var myChart = echarts.init(dom);
        var datas = splitData(price_trend_series);
        console.log(datas.values);

        function splitData(rawData) {
            var categoryData = [],
                values = [],
                nows = [];
            for (var i = 0; i < rawData.length; i++) {
                categoryData.push(rawData[i].splice(0, 1)[0]); //日期
                nows.push(rawData[i][3] - 0.23); //日期
                values.push(rawData[i]) //开，收，低，高
            }
            return {
                categoryData: categoryData,
                now: nows,
                values: values
            };
        }

        var config = {
            barWidth: 20,//指定柱宽度
            col: {
                /* up: 'rgb(153, 14, 14)',
                 down: '#19b34c',
                 m5: '#f00',
                 m10: 'yellow',
                 m30: '#dd1ce0'*/
                up: 'rgb(0,198,215)',
                down: 'rgb(5,41,99)',
                m5: 'rgb(0,198,215)',
                m10: 'yellow',
                m30: '#dd1ce0'
            },
            // bg: '#000',
            st: 10,
            ed: 60
        }
        option = {
            backgroundColor: config.bg,
            // color: '#fff',
            title: {
                text: null
            },

            // 提示框浮层的位置
            tooltip: {
                trigger: 'axis',
                position: [10, '70%'],
                formatter: function (params) {
                    console.log(params);
                    if (params.length > 1) {
                        var str = '日期：' + params[0].name;
                        var string_data = '今日价格最低：￥' + params[0].data[1];
                        string_data += '<br>' + '今日价格最高：￥' + params[0].data[2];

                        str += '<br>' + params[1].seriesName + ':￥' + (params[0].data[4]).toFixed(2);
                        if (params[1].seriesName == undefined) {
                            params[1].seriesName = '平均价'
                        }
                        return str + '<br>' + string_data
                    } else {
                        var str = '日期：' + params[0].name;
                        var string_data = '今日价格最低：￥' + params[0].data[2];
                        string_data += '<br>' + '今日价格最高：￥' + params[0].data[1];
                        return str + '<br>' + string_data
                    }
                },
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
                            a: {}
                        }
                    },
                    crossStyle: {
                        type: 'solid'
                    }
                }
            },
            legend: {
                data: ['价格趋势', '日平均']
            },
            grid: [{
                top: '10%',
                // show:true,
                left: '5%', //grid 组件离容器左侧的距离。
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
            // 上下两个图表的x轴数据
            xAxis: [{
                type: 'category',
                boundaryGap: true,
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
                    name: '价格趋势',
                    itemStyle: {
                        normal: {
                            color: config.col.up, //阳线填充色
                            color0: config.col.down,
                            borderColor: config.col.up, //阳线边框色
                            borderColor0: config.col.down
                        }
                    },
                    data: datas.values
                },
                {
                    type: 'line',
                    name: '日平均',
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
                from_county_id: $('#start_address').attr('districtsid') == undefined ? '' : $('#start_address').attr('districtsid'),
                to_province_id: $('#end_address').attr('provinceid') == undefined ? '' : $('#end_address').attr('provinceid'),
                to_city_id: $('#end_address').attr('cityid') == undefined ? '' : $('#end_address').attr('cityid'),
                to_county_id: $('#end_address').attr('districtsid') == undefined ? '' : $('#end_address').attr('districtsid'),
                min_mileage: $('#min_mileage').val(),
                max_mileage: $('#max_mileage').val(),
                vehicle_length: $('#vehicle_type').val(),
                order_status: $('#order_status').val(),
                start_time: start_time,
                end_time: end_time
            };
            console.log(data.to_province_id)
            if (data.min_mileage != '') {
                if (common.isNumber(data.min_mileage)) {
                    layer.tips('请检查数据格式-(数字)', '#min_mileage', {
                        tips: [1, '#009688'],
                        time: 3000
                    });
                    return false;
                }
            }
            if (data.max_mileage != '') {
              if (common.isNumber(data.max_mileage)) {
                  layer.tips('请检查数据格式-(数字)', '#max_mileage', {
                      tips: [1, '#009688'],
                      time: 3000
                  });
                  return false;
              }
            }
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                var avg_price = res.data.avg_price;
                var price_trend_series = res.data.price_trend_series;
                that.chartRender(price_trend_series, avg_price)
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
