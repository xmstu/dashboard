var set = {
        tableRender: function (url) {
            layui.use(['layer', 'table'], function () {
                var table = layui.table;
                var layer = layui.layer;
                table.render({
                    elem: '#business_msg_table',
                    even: true,
                    url: url,
                    response: {
                        statusName: 'status',
                        statusCode: 100000
                    }
                    , cols: [[
                        {field: 'id', title: '序号', width: 80},
                        {field: 'msg_type', title: '类型'},
                        {field: 'content', title: '信息', width: 400},
                        {field: 'create_time', title: '发布时间'},
                        {field: 'follow_admin_name', title: '跟进人', width: 100},
                        {
                            field: 'follow_result', title: '操作', templet: function (d) {
                                if (d.follow_admin_name != "") {
                                    return "<i  style=\"color:#FF5722\">恭喜您,此单已谈成！</i>";
                                }
                                if (d.follow_result != "" && d.follow_result != "成功") {
                                    return '<i  style="color:#000000">下次继续努力！</i><br><i style="color:#2F4056"><i style="color:#94757c">失败原因:</i>'+d.follow_result+'</i>';
                                }

                                return '<i data-id="' + d.id + '" data-name="' + "假设跟进人" + '" class="layui-icon layui-btn layui-btn-normal layui-icon-praise success-operate" title="谈成了"  style="margin-right: 40px;cursor:pointer;">谈成了</i>' +
                                    '<i data-id="' + d.id + '" style="cursor: pointer" class="layui-icon layui-btn layui-btn-danger layui-btn-xs layui-icon-face-cry defail-operate"  title="没谈成" >没谈成</i>'
                            }
                        }
                    ]],
                    done: function (res) {
                        layer.closeAll('loading');
                        $('.defail-operate').click(function () {
                            var msg_id = $(this).attr('data-id');
                            var msg_id = $(this).attr('data-id');
                            layer.open({
                                type: 1,
                                title: '没谈成-原因',
                                closeBtn: 1,
                                anim: 2,
                                area: ['420px', '240px'], //宽高
                                shadeClose: true, //开启遮罩关闭
                                skin: "layui-layer-lan",
                                content: '<textarea id="defail_result" placeholder="请输入失败原因..." class="layui-textarea"></textarea>' +
                                '\n <div class="bottom"><button onclick="set.fail_(' + msg_id + ')" class="layui-btn layui-btn-normal defail_btn">确认</button> ' +
                                ' <button class="layui-btn layui-btn-primary layui-layer-close layui-layer-close1">关闭</button></div>'
                            });
                        });

                        $('.success-operate').click(function () {
                            var msg_id = $(this).attr('data-id');
                            var url = '/business_msg/business_msg/' + msg_id;
                            var follow_admin_name = $('.user_name_icon').attr('data-user-name');
                            var data = {
                                follow_name: follow_admin_name || "怕不是黑进来的吧?!",
                                follow_result: "成功"
                            };
                            data = JSON.stringify(data);
                            layer.confirm('确定与本条信息谈成了??', {
                                skin: 'layui-layer-lan',
                                btn: ['确认', '取消']
                            }, function () {
                                http.ajax.put_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                                    if (res.status == 100000) {
                                        layer.msg('恭喜您，此单谈成了！', function () {
                                            window.location.reload();
                                        });
                                    }
                                }, function (xhttp) {
                                    if (xhttp.responseJSON.status != 100000) {
                                        layer.msg('失败', function () {
                                            layer.closeAll("loading")
                                        });
                                    }
                                })
                            }, function () {

                            });
                        })
                    },
                    page: true,
                    id: 'dataTable'
                });
            })
        },
        fail_: function (msg_id) {
            var url = '/business_msg/business_msg/' + msg_id;
            var follow_result = $("#defail_result").val();
            var data = {
                follow_name: "",
                follow_result: follow_result || '该客户太忙，没有填写原因...'
            };
            data = JSON.stringify(data);
            http.ajax.put_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                if (res.status == 100000) {
                    layer.msg('没谈成，没关系，下次继续努力！', function () {
                        window.location.reload();
                    });
                }
            }, function (xhttp) {
                if (xhttp.responseJSON.status != 100000) {
                    layer.msg('失败', function () {
                        layer.closeAll("loading")
                    });
                }
            })
        }
    }
;


set.tableRender('/business_msg/business_msg')