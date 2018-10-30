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
        tableInit("/jobs/jobs_list/");
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
            region: $("#region").val(),
            time_scale: $("#time_scale").val(),
        };
        var url = "/jobs/jobs_list/?job_name=" + data.job_name + "&region=" + data.region + "&time_scale=" + data.time_scale;
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
                        field: "job_name",
                        title: "职业名称",
                        width: 70
                    },
                    {
                        field: "job_url",
                        title: "职位链接",
                        width: 78
                    },
                    {
                        field: "salary_range",
                        title: "薪资范围",
                        width: 80
                    },
                    {
                        field: "addr",
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
                        field: "sectors",
                        title: "所属行业",
                        width: 90
                    },
                    {
                        field: "finance",
                        title: "融资情况",
                        width: 90
                    },
                    {
                        field: "peo_num",
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
                parseData: function (res) { //res 即为原始返回的数据
                    return {
                        "status": res.status, //解析接口状态
                        "msg": res.msg, //解析提示文本
                        "count": res.count, //解析数据长度
                        "data": res.data //解析数据列表
                    };
                },
                id: "testReload",
                page: true
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
