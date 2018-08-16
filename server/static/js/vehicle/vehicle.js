var set = {
    init: function () {
        var that = this;
        $('.vehicle-menu-about>a').addClass('selected-active');
        layui.use(['layer', 'laydate'], function () {
            var layer = layui.layer;
            var laydate = layui.laydate;
            laydate.render({
                elem: '#date_show_one',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                 format:'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#date_show_one').val();
                    var endTime = $('#date_show_two').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#date_show_one').val())
                    var endTime = common.timeTransform($('#date_show_two').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#date_show_one').val() == '' || val == '') {
                        $('#date_show_one').next('.date-tips').show();
                    } else {
                        $('#date_show_one').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#date_show_two',
                theme: '#009688',
                max: String(common.getNowFormatDate()[3]),
                calendar: true,
                 format:'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#date_show_one').val();
                    var endTime = $('#date_show_two').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#date_show_one').val())
                    var endTime = common.timeTransform($('#date_show_two').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#date_show_two').val() == '' || val == '') {
                        $('#date_show_two').next('.date-tips').show();
                    } else {
                        $('#date_show_two').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#date_show_three',
                theme: '#009688',
                max: String(common.getNowFormatDate()[3]),
                calendar: true,
                 format:'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#date_show_three').val();
                    var endTime = $('#date_show_four').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#date_show_three').val())
                    var endTime = common.timeTransform($('#date_show_four').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#date_show_three').val() == '' || val == '') {
                        $('#date_show_three').next('.date-tips').show();
                    } else {
                        $('#date_show_three').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#date_show_four',
                theme: '#009688',
                max: String(common.getNowFormatDate()[3]),
                calendar: true,
                 format:'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#date_show_three').val();
                    var endTime = $('#date_show_four').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#date_show_three').val())
                    var endTime = common.timeTransform($('#date_show_four').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#date_show_four').val() == '' || val == '') {
                        $('#date_show_four').next('.date-tips').show();
                    } else {
                        $('#date_show_four').next('.date-tips').hide()
                    }
                }
            });
            that.tableRender('/vehicle/list/')
        })
    },
    tableRender: function (url) {
        layui.use(['layer', 'table'], function () {
            var table = layui.table;
            var layer = layui.layer;
            layer.load();
            table.render({
                elem: '#vehicle_table',
                even: true,
                url: url,
                response: {
                    statusName: 'status',
                    statusCode: 100000
                }
                , cols: [[
                    {field: 'id', title: '车辆ID'},
                    {field: 'name', title: '姓名'},
                    {field: 'mobile', title: '手机号'},
                    {field: 'number', title: '车牌号'},
                    {field: 'home_station', title: '常驻地'},
                    {field: 'vehicle_length_type', title: '车长/车型'},
                    {field: 'audit_time', title: '认证时间'},
                    {field: 'last_login_time', title: '最后登陆时间'}
                ]],
                done: function (res) {
                    layer.closeAll('loading')
                },
                page: true,
                id: 'dataTable'
            });
        })
    },
    dataRender: function () {
        var that = this;
        $('#search_btn').click(function (e) {
            e.preventDefault();
            var verify_start_time = $('#date_show_one').val();
            var verify_end_time = $('#date_show_two').val();
            var last_login_start_time = $('#date_show_three').val()
            var last_login_end_time = $('#date_show_four').val()
            var data = {
                mobile: $('#mobile').val(),
                vehicle_number: $('#vehicle_number').val(),
                home_station_id: $.trim($("#region_id").val()) == "" ? common.role_area_show($("#super_manager_area_select_zero")) : $.trim($("#region_id").val()),
                vehicle_length: $('#vehicle_type').val(),
                verify_start_time: verify_start_time,
                verify_end_time: verify_end_time,
                last_login_start_time: last_login_start_time,
                last_login_end_time: last_login_end_time
            };
            if (data.verify_start_time != '') {
                data.verify_start_time = common.timeTransform(data.verify_start_time + ' 00:00:00')
            }
            if (data.verify_end_time != '') {
                data.verify_end_time = common.timeTransform(data.verify_end_time + ' 23:59:59')
            }
            if (data.last_login_start_time != '') {
                data.last_login_start_time = common.timeTransform(data.last_login_start_time + ' 00:00:00')
            }
            if (data.last_login_end_time != '') {
                data.last_login_end_time = common.timeTransform(data.last_login_end_time + ' 23:59:59')
            }
            if (data.verify_end_time != '' && data.verify_start_time == '') {
                layer.tips('请输入开始日期！', '#date_show_one', {
                    tips: [1, '#009688'],
                    time: 3000
                });
                return false;
            }
            if (data.verify_start_time != '' && data.verify_end_time == '') {
                data.verify_end_time = common.currentTime()
            }
            var url = '/vehicle/list/?mobile=' + data.mobile + '&vehicle_number=' + data.vehicle_number + '&home_station_id=' + data.home_station_id + '&vehicle_length=' + data.vehicle_length + '&verify_start_time=' + data.verify_start_time + '&verify_end_time=' + data.verify_end_time + '&last_login_start_time=' + data.last_login_start_time + '&last_login_end_time=' + data.last_login_end_time;
            that.tableRender(url)
        })
    },
    area_select: function () {
        var auth_role = $("#user-info").attr("data-role");
        if (!!auth_role && auth_role == 1) {
            $("#super_manager_area").css({
                "display": "block"
            });
            $("#super_manager_area_select_zero").address({
                level: 3,
                offsetLeft: '-124px'
            })
        } else {
            $("#super_manager_area").css({
                "display": "none"
            });
            $("#city_manager_one").css({
                "display": "block"
            })
        }
    }

};
set.init();
set.dataRender();
set.area_select();