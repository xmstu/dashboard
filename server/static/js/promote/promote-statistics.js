/**
 * Created by Creazy_Run on 2018/5/30.
 */
lineChartInit();
$('#date_show_one').val(String(common.getNowFormatDate()[2]));
$('#date_show_two').val(String(common.getNowFormatDate()[3]));
$('#date_show_three').val();
$('#date_show_four').val();
setTimeout(function () {
    common.dateInterval($('#date_show_one').val(), $('#date_show_one').val());
}, 100);
layui.use(['laydate', 'form', 'table'], function () {
    var laydate = layui.laydate;
    var table = layui.table;
    var form = layui.form;
    form.on('select(is_actived)', function (data) {
        if (data.value == '1') {
            $('#select_spec_two').hide();
            $('#select_spec_three').hide();
            $('#select_spec_one').show()
        } else if (data.value == '2') {
            $('#select_spec_one').hide();
            $('#select_spec_three').hide();
            $('#select_spec_two').show()

        } else if (data.value == '3') {
            $('#select_spec_one').hide();
            $('#select_spec_two').hide();
            $('#select_spec_three').show()
        }
    });
    laydate.render({
        elem: '#date_show_one',
        theme: '#1E9FFF',
        max: String(common.getNowFormatDate()[5]),
        calendar: true,
        done: function (val, index) {

        }
    });
    laydate.render({
        elem: '#date_show_two',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        done: function (val, index) {

        }
    });
    laydate.render({
        elem: '#date_show_three',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[5]),
        done: function (val, index) {
        }
    });
    laydate.render({
        elem: '#date_show_four',
        theme: '#1E9FFF',
        calendar: true,
        max: String(common.getNowFormatDate()[3]),
        done: function (val, index) {
        }
    });
    //监听工具条
     table.render({
    elem: '#test'
    ,url:'/demo/table/user/'
    ,cols: [[
      {type:'checkbox'}
      ,{field:'id', width:80, title: 'ID', sort: true}
      ,{field:'username', width:80, title: '用户名'}
      ,{field:'sex', width:80, title: '性别', sort: true}
      ,{field:'city', width:80, title: '城市'}
      ,{field:'sign', title: '签名', minWidth: 100}
      ,{field:'experience', width:80, title: '积分', sort: true}
      ,{field:'score', width:80, title: '评分', sort: true}
      ,{field:'classify', width:80, title: '职业'}
      ,{field:'wealth', width:135, title: '财富', sort: true}
    ]]
    ,page: true
  });
    table.on('tool(demo)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.confirm('真的删除行么', function (index) {
                obj.del();
                layer.close(index);
            });
        }
    });
    var $ = layui.$, active = {
        isAll: function () { //验证是否全选
            var checkStatus = table.checkStatus('idTest');
            layer.msg(checkStatus.isAll ? '全选' : '未全选')
        }
    };

    $('.demoTable .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
    });
});
$('#user_search_box').on('click', function (e) {
    e.preventDefault();
    if (beginTime != '' && finishTime == '') {
        layer.msg('请选择新增结束日期')
        return false;
    }
    if (beginTime == '' && finishTime != '') {
        layer.msg('请选择新增开始日期')
        return false;
    }
});
$('#add_promote_person').on('click', function (e) {
    e.preventDefault();
    var str = "<p  style='position: relative;'><span class='phone-number'>输入号码</span><i class='iconfont icon-dianhua'></i><input id='add_users' type='text' placeholder='请输入添加人的号码'></p> "
    layer.confirm(str, {
        title: '新增推广人员',
        btn: ['确定添加', '取消'] //按钮
    }, function () {
        layer.msg('success')
    }, function () {
        layer.msg('取消')
    });
});

function lineChartInit() {
    $('#charts_container_one').highcharts({
        tooltip: {
            shared: false,
            crosshairs: [{
                width: 1,
                color: '#ccc'
            }, {
                width: 1,
                color: '#ccc'
            }],
            plotOptions: {
                spline: {
                    marker: {
                        radius: 4,
                        lineColor: '#666666',
                        lineWidth: 1
                    }
                }
            }
        },
        chart: {
            backgroundColor: '#fff',
            type: 'line'
        },

        title: {
            text: '推广统计变化趋势图'
        },
        subtitle: {
            text: '数据来源：省省官方后台数据库'
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 1300,
            y: 0,
            floating: true,
            borderWidth: 1,
            backgroundColor: 'transparent',
            labelFormatter: function () {
                return this.name
            }
        },
        xAxis: {
            categories: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
            gridLineColor: '#eee',
            gridLineWidth: 1
        },
        yAxis: {
            title: {
                text: '人数 (人)'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: '人数',
            data: [7.0, 6.9, 9.5, 14.5, 18.4, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
        }]
    });
}

var pageSet = {};