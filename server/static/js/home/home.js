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
            elem: "#start_date",
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
            elem: "#end_date",
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
            job_name: $('#job_name').val(),
            jobs_type: $.trim($("#goods_type").val()),
            // region: $.trim($("#is_called").val()),
            pub_time: $.trim($("#vehicle_length").val()),
            region: $.trim($("#node_id").val()) == "" ? common.role_area_show($("#super_manager_area_one")) : $.trim($("#node_id").val()),
        };
        var url = "/jobs/jobs_list/?job_name=" + data.job_name + "&jobs_type=" + data.jobs_type + "&pub_time=" + data.pub_time + "&region=" + data.region;
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
                cols: [[
                    {
                    field: "jobs_name",
                    title: "职业名称",
                    width: 70
                    },
                    {
                        field: "jobs_url",
                        title: "职位链接",
                        width: 78
                    },
                    {
                        field: "salary_range",
                        title: "薪资范围",
                        width: 80
                    },
                    {
                        field: "address",
                        title: "公司地址",
                        width: 200
                    },
                    {
                        field: "experience",
                        title: "工作经验",
                        width: 100
                    },
                    {
                        field: "education",
                        title: "学历",
                        width: 100
                    },
                    {
                        field: "company",
                        title: "公司名字",
                        width: 100
                    },
                    {
                        field: "company_url",
                        title: "公司官网",
                        width: 100
                    },
                    {
                        field: "finance",
                        title: "融资情况",
                        width: 90
                    },
                    {
                        field: "pep_num",
                        title: "公司规模",
                        width: 100
                    },
                    {
                        field: "employee",
                        title: "发布人",
                        width: 100
                    },
                    {
                        field: "employee_job",
                        title: "发布人职位",
                        width: 100
                    },
                    {
                        field: "pub_time",
                        title: "发布时间",
                        width: 100
                    },
                    ]],
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
                            area: ["1200px", "600px"],
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
                            area: ["1200px", "600px"],
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
                    });
                    layer.closeAll('loading')
                }
            })
        })
}

function area_select() {

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
}

area_select();
common.init();
var test = $('#select_box select');
