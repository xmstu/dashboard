$(".layui-table-cell").css({
    "height": "auto!important"
});
$(".part-2 .layui-form-item").css({
    "width": "246px"
});
$("#date_show_one").val(String(common.getNowFormatDate()[3]));
$("#date_show_two").val(String(common.getNowFormatDate()[3]));
var dataArr1 = ["待接单", "已接单", "已取消", "已接单车辆", "待接单车辆数"];
var dataArr2 = ["待联系", "已联系", "已接单", "已取消", "已接单车辆", "待接单车辆数"];
setTimeout(function () {
        tableInit("/city/latest_orders/");
        $(".area-menu-about>a").addClass("selected-active");
        $(".area-menu-about>a>i").addClass("select-active");
    },
    10);
layui.use(["laydate", "form", "table"],
    function () {
        dataInit(dataArr2);
        layer.load();
        var laydate = layui.laydate;
        var table = layui.table;
        laydate.render({
            elem: "#date_show_one",
            theme: "#009688",
            calendar: true,
            max: String(common.getNowFormatDate()[0]),
            done: function (val, index) {
                var startTime = common.timeTransform($("#date_show_one").val());
                var endTime = common.timeTransform($("#date_show_two").val());
                if (startTime > endTime) {
                    layer.msg("提示：开始时间大于了结束时间！");
                    return false
                }
            }
        });
        laydate.render({
            elem: "#date_show_two",
            theme: "#009688",
            calendar: true,
            max: String(common.getNowFormatDate()[0]),
            done: function (val, index) {
                var startTime = common.timeTransform($("#date_show_one").val());
                var endTime = common.timeTransform($("#date_show_two").val());
                if (startTime > endTime) {
                    layer.msg("提示：开始时间大于了结束时间！");
                    return false
                }
            }
        })
    });
$("#search_btn").click(function (e) {
    e.preventDefault();
    var current_val = $("#goods_types").val();
    if (current_val == 3) {
        dataInit(dataArr2)
    } else {
        if (current_val == 1) {
            dataInit(dataArr1)
        }
    }
});
$("#user_search_box").on("click",
    function (e) {
        e.preventDefault();
        var data = {
            goods_type: $.trim($("#goods_type").val()),
            is_called: $.trim($("#is_called").val()),
            vehicle_length: $.trim($("#vehicle_length").val()),
            node_id: $.trim($("#node_id").val()) == "" ? common.role_area_show($("#super_manager_area_one")) : $.trim($("#node_id").val()),
            spec_tag: $.trim($("#spec_tag").val()),
            is_addition: $.trim($("#is_addition").val())
        };
        var url = "/city/latest_orders/?goods_type=" + data.goods_type + "&is_called=" + data.is_called + "&vehicle_length=" + data.vehicle_length + "&node_id=" + data.node_id + "&spec_tag=" + data.spec_tag + "&is_addition=" + data.is_addition;
        tableInit(url)
    });

function dataInit(dataArrSet) {
    layui.use("layer",
        function () {
            var layer = layui.layer;
            var start_time = $.trim($("#date_show_one").val());
            var end_time = $.trim($("#date_show_two").val());
            if (common.timeTransform(start_time) > common.timeTransform(end_time)) {
                layer.msg("提示：开始时间大于了结束时间！");
                return false
            }
            var goods_types = $.trim($("#goods_types").val());
            var region_id = $.trim($("#city_area").val()) == "" ? common.role_area_show($("#super_manager_area_zero")) : $.trim($("#city_area").val());
            if (start_time != "") {
                start_time = common.timeTransform(start_time + " 00:00:00")
            }
            if (end_time != "") {
                end_time = common.timeTransform(end_time + " 23:59:59")
            }
            var url = "/city/resource/";
            var data = {
                start_time: start_time,
                end_time: end_time,
                region_id: region_id,
                goods_type: goods_types
            };
            http.ajax.get(true, false, url, data, http.ajax.CONTENT_TYPE_2,
                function (res) {
                    var arr = Object.keys(res.data);
                    /*if(arr.length==0){
                        var results_ ='<li style="font-size: 13px;color: #ccc;text-align: center;line-height: 22px;">该条件下无数据</li>'
                        console.log(results_)
                        $('.part-1-bottom').text(1234)
                    }*/
                    var str = "";
                    for (var i = 0; i < arr.length; i++) {
                        str += '<li class="charts-lists"><div class="charts-container" id="charts_container_' + i + '"></div><div class="data-list-container' + i + '"></li>';
                        $(".data-list-container0").append($(".tip-list-show0"))
                    }
                    $(".part-1-bottom ul").empty();
                    $(".part-1-bottom ul").append(str);
                    var dataStyle = {
                        normal: {
                            label: {
                                show: false
                            },
                            labelLine: {
                                show: false
                            }
                        }
                    };
                    var result = "";
                    $.each(res.data,
                        function (index, val) {
                            if (val[1][2].value < 0) {
                                val[1][2].value = 0
                            }
                            if (arr.length >= 0) {
                                arr.length--
                            }
                            var result = '<span class=" tip-show-set tip-list-show' + arr.length + '">' + val[0][0].name + ":" + val[0][0].value + "单</span>";
                            result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][1].name + ":" + val[0][1].value + "单</span>";
                            result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][2].name + ":" + val[0][2].value + "单</span>";
                            result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][0].name + ":" + val[1][0].value + "辆</span>";
                            result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][1].name + ":" + val[1][1].value + "辆</span>";
                            result += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][2].name + ":" + val[1][2].value + "辆</span>";
                            var all_count = '<p class="all_count">货源数:<span>' + (val[0][0].value + val[0][1].value + val[0][2].value) + "单</span></p>";
                            var all_count_1 = '<p class="all_count_1">车辆数:<span>' + (val[1][0].value + val[1][1].value) + "辆</span></p>";
                            if ($("#goods_types").val() == 1 || $("#goods_types").val() == 2) {
                                $(".data-list-container" + arr.length).html("");
                                $(".data-list-container" + arr.length).append(all_count + all_count_1 + result)
                            } else {
                                if ($("#goods_types").val() == 3) {
                                    var result_ano = '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][0].name + ":" + val[0][0].value + "单</span>";
                                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][1].name + ":" + val[0][1].value + "单</span>";
                                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][2].name + ":" + val[0][2].value + "单</span>";
                                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[0][3].name + ":" + val[0][3].value + "单</span>";
                                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][0].name + ":" + val[1][0].value + "辆</span>";
                                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][1].name + ":" + val[1][1].value + "辆</span>";
                                    result_ano += '<span class="tip-show-set tip-list-show' + arr.length + '">' + val[1][2].name + ":" + val[1][2].value + "辆</span>";
                                    var all_count_ano = '<p class="all_count">货源数:<span>' + (val[0][0].value + val[0][1].value + val[0][2].value + val[0][3].value) + "单</span></p>";
                                    var all_count_ano_1 = '<p class="all_count_1">车辆数:<span>' + (val[1][0].value + val[1][1].value) + "辆</span></p>";
                                    $(".data-list-container" + arr.length).html("");
                                    $(".data-list-container" + arr.length).append(all_count_ano + all_count_ano_1 + result_ano)
                                }
                            }
                            var dom = document.getElementById("charts_container_" + arr.length + "");
                            var myChart = echarts.init(dom);
                            option = {
                                title: {
                                    text: index,
                                    subtext: null,
                                    x: "center",
                                    y: "center",
                                    itemGap: 20,
                                    textStyle: {
                                        color: "skyblue",
                                        fontFamily: "微软雅黑",
                                        fontSize: 18,
                                        fontWeight: "bolder"
                                    }
                                },
                                tooltip: {
                                    trigger: "item",
                                    show: true,
                                    formatter: "{a} <br/>{b} : {c} ({d}%)",
                                    extraCssText: "width:auto;height:60px;background:rgba(0,0,0,.4);"
                                },
                                legend: {
                                    orient: "vertical",
                                    x: "left",
                                    y: "top",
                                    data: dataArrSet
                                },
                                toolbox: {
                                    show: true,
                                    feature: {
                                        mark: {
                                            show: true
                                        }
                                    }
                                },
                                color: ["skyblue", "#7dd4f8", "#60b2d3", "#2973a7", "#497080", "#5fd779", "#56b35d"],
                                series: [{
                                    name: "货源数",
                                    type: "pie",
                                    clockWise: false,
                                    radius: [90, 105],
                                    itemStyle: dataStyle,
                                    data: val[0]
                                },
                                    {
                                        name: "车辆数",
                                        type: "pie",
                                        clockWise: false,
                                        radius: [75, 90],
                                        itemStyle: dataStyle,
                                        data: val[1]
                                    }]
                            };
                            if (option && typeof option === "object") {
                                myChart.setOption(option, true)
                            }
                        });
                    if ($(".charts-lists").html() != "") {
                        layer.closeAll("loading");
                        $(".main-content-right").addClass("animated fadeIn")
                    }
                })
        })
}

function tableInit(url) {
    layui.use(["layer", "table", "form"],
        function () {
            var table = layui.table;
            var form = layui.form;
            var layer = layui.layer;
            layer.load();
            table.render({
                elem: "#LAY_table_goods",
                even: true,
                url: url,
                response: {
                    statusName: "status",
                    statusCode: 100000
                },
                loading: true,
                cols: [[{
                    field: "goods_id",
                    title: "货源ID",
                    width: 70
                },
                    {
                        field: "goods_type",
                        title: "类型",
                        width: 70
                    },
                    {
                        field: "content",
                        title: "货物规格",
                        width: 120
                    },
                    {
                        field: "address",
                        title: "出发地-目的地",
                        width: 296
                    },
                    {
                        field: "vehicle",
                        title: "车型要求",
                        width: 80
                    },
                    {
                        field: "price",
                        title: "运费",
                        width: 100
                    },
                    {
                        field: "mobile",
                        title: "货主手机",
                        width: 90
                    },
                    {
                        field: "call_count",
                        title: "通话数",
                        width: 60
                    },
                    {
                        field: "goods_time",
                        title: "时间",
                        width: 154
                    },
                    {
                        field: "supplier_node",
                        title: "所属网点"
                    },
                    {
                        field: "operate",
                        title: "附近的车",
                        width: 100,
                        templet: function (d) {
                            return '<button data-type="1" value="' + d.goods_id + '" id="nearly_' + d.goods_id + '" class="layui-btn layui-btn-small nearby-one admin-table-button"><i class="iconfont icon-dituleixianlu" style="margin-right: 2px"></i>接单线路</button><button data-type="2"  value="' + d.goods_id + '" id="nearly_' + d.goods_id + '" class="layui-btn nearby-two layui-btn-small admin-table-button"><i class="iconfont icon-suozaichengshi" style="margin-right: 2px"></i>常驻地</button> <p class="display-content" style="display: none">' + d.address + '</p>'
                        }
                    }]],
                done: function (res, curr, count) {
                    layer.closeAll("loading");
                    $("[data-field]>div").css({
                        "padding": "0 6px"
                    });
                    $(".nearby-one").on("click", function (e) {
                        e.preventDefault();
                        var content_title = $(this).siblings('p.display-content').text()
                        if (content_title != '') {
                            var result_title = content_title.split('\n')
                            result_title = '<p>' + result_title[0] + '&nbsp;&nbsp;&nbsp;到&nbsp;&nbsp;&nbsp;' + result_title[1] + '</p'
                        }
                        layer.load();
                        var val = $(this).val();
                        var goods_type = $(this).attr('data-type')
                        var url = "/city/nearby_cars/" + val + '?goods_type=' + goods_type;
                        /*
                           首页表格按钮框点击弹出的遮罩层筛选
                         form.on("select(interest)",
                               function (res) {
                                   var value = res.value;
                                   var url_reset = "/city/nearby_cars/" + val + "?goods_type" + value;
                                   tableReset(url_reset)
                               });*/
                        tableReset(url);
                        layer.open({
                            type: 1,
                            title: result_title,
                            area: ["1300px", "600px"],
                            skin: "layui-layer-molv",
                            closeBtn: 1,
                            content: $("#popup")
                        })
                    });
                    $(".nearby-two").on('click', function (e) {
                        e.preventDefault()
                        var content_title = $(this).siblings('p.display-content').text()
                        if (content_title != '') {
                            var result_title = content_title.split('\n')
                            result_title = '<p>' + result_title[0] + '&nbsp;&nbsp;&nbsp;到&nbsp;&nbsp;&nbsp;' + result_title[1] + '</p'
                        }
                        var val = $(this).val();
                        var goods_type = $(this).attr('data-type')
                        var url = "/city/nearby_cars/" + val + '?goods_type=' + goods_type;
                        layer.open({
                            type: 1,
                            title: result_title,
                            area: ["1300px", "600px"],
                            skin: "layui-layer-molv",
                            closeBtn: 1,
                            content: $("#popup_one")
                        })
                        layer.load();
                        popupRender(url)
                    })
                    $("td[data-field='price']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            str = str.split("\n");
                            $(this).html(str[0] + "<br>" + str[1])
                        }
                    });
                    $("td[data-field='mobile']").children().each(function () {
                        var str = $(this).text();
                        if (str != "") {
                            str = str.split("\n");
                            if (str[0] == "") {
                                $(this).html(str[0])
                            } else {
                                if (str[0] != "" && str[1] == "" && str[2] != "") {
                                    $(this).html(str[0] + '<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ")</span>")
                                } else {
                                    if (str[0] != "" && str[1] != "" && str[2] == "") {
                                        $(this).html(str[0] + "<br>" + str[1])
                                    } else {
                                        if (str[0] != "" && str[1] != "" && str[2] != "") {
                                            $(this).html(str[0] + "<br>" + str[1] + '<br><span style="color: #f40;font-weight: bold;">(' + str[2] + ")</span>")
                                        }
                                    }
                                }
                            }
                        }
                    });
                    $("td[data-field='vehicle']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            str = str.split("\n");
                            if (str[1] == "" || str[1] == undefined) {
                                $(this).html(str[0])
                            } else {
                                $(this).html(str[0] + "<br>" + str[1])
                            }
                        }
                    });
                    $("td[data-field='goods_time']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            str = str.split("\n");
                            $(this).html("发布:" + str[0] + "<br>装货:" + str[1])
                        }
                    });
                    $("td[data-field='address']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            str = str.split("\n");
                            $(this).html('<span style="color: purple;">' + str[0] + "</span><br>" + str[1] + "<br>" + str[2])
                        }
                    });
                    $("td[data-field='call_count']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            $(this).html(str + "次")
                        }
                    });
                    $("td[data-field='goods_type']").children().each(function () {
                        if ($(this).text() == "跨城定价") {
                            $(this).html('<span style="color: #01AAED;">跨城定价</span>')
                        }
                        if ($(this).text() == "跨城议价") {
                            $(this).html('<span style="color: #f40;">跨城议价</span>')
                        }
                        if ($(this).text() == "同城") {
                            $(this).html('<span style="color: green;">同城</span>')
                        }
                    })
                },
                id: "testReload",
                page: true
            })
        })
}

function tableReset(url) {
    layui.use(["table", 'layer', "form"],
        function () {
            var layer = layui.layer;
            var table = layui.table;
            layer.load()
            table.render({
                elem: "#demo",
                url: url,
                page: false,
                width: 1272,
                response: {
                    statusName: "status",
                    statusCode: 100000
                },
                loading: true,
                cols: [[{
                    field: "name",
                    title: "司机姓名",
                    width: 86
                },
                    {
                        field: "mobile",
                        title: "手机号码",
                        width: 108
                    },
                    {
                        field: "booking_line",
                        title: "接单线路"
                    },
                    {
                        field: "booking_time",
                        title: "设置时间",
                        width: 100
                    },
                    {
                        field: "locations",
                        title: "最新定位",
                        width: 300
                    },
                    {
                        field: "vehicel_length",
                        title: "车长",
                        width: 80
                    },
                    {
                        field: "is_trust_member",
                        title: "诚信会员",
                        sort: true,
                        width: 90
                    },
                    {
                        field: "order_count",
                        title: "接单数",
                        sort: true,
                        width: 80
                    },
                    {
                        field: "order_finished",
                        title: "完成数",
                        sort: true,
                        width: 80
                    },
                    {
                        field: "order_cancel",
                        sort: true,
                        title: "取消数",
                        width:80
                    }]],
                done: function (res) {
                    $("td[data-field='is_trust_member']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            if (str == 1) {
                                $(this).text("是")
                            } else {
                                if (str == 0) {
                                    $(this).text("否")
                                }
                            }
                        }
                    });
                    $("td[data-field='credit_level']").children().each(function () {
                        var value_level = $(this).text();
                        if (value_level == 1) {
                            $(this).html('<p><i class="iconfont icon-iconfontxingxing"></i></p>')
                        }
                        if (value_level == 2) {
                            $(this).html('<p><i class="iconfont icon-iconfontxingxing"></i></p>')
                        }
                        if (value_level == 5) {
                            $(this).html('<p style="color: #009f95;"><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i></p>')
                        }
                    })
                    layer.closeAll('loading')
                }
            })
        })
}

function popupRender(url) {
    layui.use(["table", 'layer', "form"],
        function () {
            var table = layui.table;
            var layer = layui.layer;
            layer.load()
            table.render({
                elem: "#demo_one",
                url: url,
                page: false,
                width: 1272,
                response: {
                    statusName: "status",
                    statusCode: 100000
                },
                loading: true,
                cols: [[{
                    field: "name",
                    title: "司机姓名",
                    width:86
                },
                    {
                        field: "mobile",
                        title: "手机号码",
                        width:108
                    },
                    // {
                    //     field: "usual_region",
                    //     title: "常驻地",
                    //     width:300
                    // },
                    {
                        field: "locations",
                        title: "最新定位",
                        width:300
                    },
                    {
                        field: "vehicle_length",
                        title: "车长",
                        width:94
                    },
                    {
                        field: "is_trust_member",
                        title: "诚信会员",
                        width:80
                    },
                    {
                        field: "order_count",
                        title: "接单数",
                        sort: true,
                        width:80
                    },
                    {
                        field: "order_finished",
                        title: "完成数",
                        sort: true,
                        width:80
                    },
                    {
                        field: "order_cancel",
                        title: "取消数",
                        sort: true,
                        width:80
                    }]],
                done: function (res) {
                    $("td[data-field='is_trust_member']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            if (str == 1) {
                                $(this).text("是")
                            } else {
                                if (str == 0) {
                                    $(this).text("否")
                                }
                            }
                        }
                    });
                    $("td[data-field='credit_level']").children().each(function () {
                        var value_level = $(this).text();
                        if (value_level == 1) {
                            $(this).html('<p><i class="iconfont icon-iconfontxingxing"></i></p>')
                        }
                        if (value_level == 2) {
                            $(this).html('<p><i class="iconfont icon-iconfontxingxing"></i></p>')
                        }
                        if (value_level == 5) {
                            $(this).html('<p style="color: #009f95;"><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i><i class="iconfont icon-iconfontxingxing"></i></p>')
                        }
                    })
                    layer.closeAll('loading')
                }
            })
        })
}

function area_select() {
    var auth_role = $("#user-info").attr("data-role");
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
common.init()
var test = $('#select_box select')
