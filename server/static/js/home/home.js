/**
 * 首页，上面的圆环是用echarts做的，下面是layui的数据表格。
 */
$(".layui-table-cell").css({
    "height": "auto!important"
});
$(".part-2 .layui-form-item").css({
    "width": "180px"
});
$("#date_show_one").val(String(common.getNowFormatDate()[0]));
$("#date_show_two").val(String(common.getNowFormatDate()[0]));
/*圆环的legel显示，echarts中legal数据要与data中的数据一直才能显示*/
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
        layer.load();
        var laydate = layui.laydate;
        var table = layui.table;
        laydate.render({
            elem: "#date_show_one",
            theme: "#009688",
            calendar: true,
            format: 'yyyy/MM/dd',
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
            format: 'yyyy/MM/dd',
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

$("#user_search_box").on("click",
    function (e) {
        e.preventDefault();
        var data = {
            mobile: $('#phone_number').val(),
            goods_type: $.trim($("#goods_type").val()),
            is_called: $.trim($("#is_called").val()),
            vehicle_length: $.trim($("#vehicle_length").val()),
            node_id: $.trim($("#node_id").val()) == "" ? common.role_area_show($("#super_manager_area_one")) : $.trim($("#node_id").val()),
            spec_tag: $.trim($("#spec_tag").val()),
            is_addition: $.trim($("#is_addition").val()),
            goods_price_type: $('#goods_price_type').val()
        };
        var url = "/city/latest_orders/?goods_type=" + data.goods_type + "&mobile=" + data.mobile + "&is_called=" + data.is_called + "&goods_price_type=" + data.goods_price_type + "&vehicle_length=" + data.vehicle_length + "&node_id=" + data.node_id + "&spec_tag=" + data.spec_tag + "&is_addition=" + data.is_addition;
        tableInit(url)
    });

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
                        width: 78
                    },
                    {
                        field: "content",
                        title: "货物规格",
                        width: 80
                    },
                    {
                        field: "address",
                        title: "出发地-目的地",
                        width: 294
                    },
                    {
                        field: "vehicle",
                        title: "车型要求",
                        width: 78
                    },
                    {
                        field: "price",
                        title: "运费",
                        width: 120
                    },
                    {
                        field: "mobile",
                        title: "货主手机",
                        width: 90
                    },
                    {
                        field: "call_count",
                        title: "通话数",
                        width: 70
                    },
                    {
                        field: "goods_time",
                        title: "时间",
                        width: 172
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
                            return '<button data-type="1" value="' + d.goods_id + '" id="nearly_' + d.goods_id + '" class="layui-btn layui-btn-small nearby-one admin-table-button"><i class="iconfont icon-dituleixianlu" style="margin-right: 2px"></i>接单线路</button><button data-type="2"  value="' + d.goods_id + '" id="nearly_' + d.goods_id + '" class="layui-btn nearby-two layui-btn-small admin-table-button"><i class="iconfont icon-qicheqianlian-" style="margin-right: 2px"></i>附近的车</button> <p class="display-content" style="display: none">' + d.from_region + '&nbsp;&nbsp;到&nbsp;&nbsp;' + d.to_region + '(' + d.vehicle + ')</p>'
                        }
                    }]],
                done: function (res, curr, count) {
                    layer.closeAll("loading");
                    common.clearSelect()
                    $("[data-field]>div").css({"padding": "0 6px"});
                     $("td[data-field='goods_type']").children().each(function (val) {
                            if ($(this).text() != '') {
                                var result = $(this).text().split('\n');
                                $(this).html(result[0] +'<br>'+ result[1])
                            }
                        })
                    $(".nearby-one").on("click", function (e) {
                        e.preventDefault();
                        var content_title = $(this).siblings('p.display-content').text()
                        if (content_title != '') {
                            // var result_title = content_title.split('\n')
                            result_title = '<p>' + content_title + '</p>'
                        }
                        layer.load();
                        var val = $(this).val();
                        var goods_type = $(this).attr('data-type')
                        var url = "/city/nearby_cars/" + val + '?goods_type=' + goods_type;
                        tableReset(url);
                        layer.open({
                            type: 1,
                            title: result_title,
                            shadeClose: true,
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
                            result_title = '<p>' + content_title + '</p'
                        }
                        var val = $(this).val();
                        var goods_type = $(this).attr('data-type')
                        var url = "/city/nearby_cars/" + val + '?goods_type=' + goods_type;
                        layer.open({
                            type: 1,
                            title: result_title,
                            shadeClose: true,
                            area: ["1300px", "600px"],
                            skin: "layui-layer-molv",
                            closeBtn: 1,
                            content: $("#popup_one")
                        })
                        layer.load();
                        popupRender(url)
                    })
                    //对后端返回的数据重新进行渲染
                    $("td[data-field='content']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            str = str.split("\n");
                            $(this).html(str[0] + "<br>" + str[1] + "<br>" + str[2])
                        }
                    });
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
                            $(this).html('<span>' + str[0] + "</span><br>" + str[1] + "<br>" + str[2])
                        }
                    });
                    $("td[data-field='call_count']").children().each(function () {
                        if ($(this).text() != "") {
                            var str = $(this).text();
                            $(this).html(str + "次")
                        }
                    });
                    $('.main-content-right').addClass('animated fadeIn')
                },
                id: "testReload",
                page: true
            })
        })
}

function tableReset(url) {
    layui.use(["table", 'layer', "form"],
        function () {
            var none_data = null;
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
                    //  width: 86
                },
                    {
                        field: "mobile",
                        title: "手机号码",
                        //  width: 108
                    },
                    {
                        field: "booking_line",
                        title: "接单线路",
                        width: 300
                    },
                    {
                        field: "booking_time",
                        title: "设置时间",
                        //  width: 100
                    },
                    {
                        field: "last_login_time",
                        title: "最后登陆",
                        //width: 100
                    },
                    {
                        field: "vehicle_length",
                        title: "车长",
                        // width: 80
                    },
                    {
                        field: "vehicle_type",
                        title: "车型",
                        // width: 80
                    },
                    {
                        field: "is_trust_member",
                        title: "诚信会员"
                    },
                    {
                        field: "order_count",
                        title: "接单数",
                        sort: true,
                        //width: 80
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
                        width: 80
                    }]],
                done: function (res) {
                    common.ajaxSetting()
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
                    width: 86
                },
                    {
                        field: "mobile",
                        title: "手机号码",
                        width: 108
                    },
                    {
                        field: "usual_region",
                        title: "常驻地",
                        width: 200
                    },
                    {
                        field: "locations",
                        title: "最新定位"
                    },
                    {
                        field: "vehicle_length",
                        title: "车长",
                        width: 94
                    },
                    {
                        field: "is_trust_member",
                        title: "诚信会员",
                        width: 80
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
                        title: "取消数",
                        sort: true,
                        width: 80
                    }]],
                done: function (res) {
                    common.ajaxSetting()
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
