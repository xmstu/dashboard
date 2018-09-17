var set = {
    init: function () {
        /*   var secondMenu = document.getElementById('second_menu_list');
           secondMenu.style.display = 'block';
           $('#second_menu_list>li:nth-of-type(2) a').addClass('selected-active');
           $('#second_menu_box').addClass('menu-active');*/
        layui.use(['form', 'layer', 'table'], function () {
            var layer = layui.layer;
            var table = layui.table;
             form = layui.form;
            var url = '/root/management/';
            var role_url = '/root/role_management/';
            /*-----从这里到下面的注释是用户管理*/
            var tableIns = table.render({
                elem: '#root_table',
                url: url,
                skin: 'nob',
                response: {
                    statusName: 'status',
                    statusCode: 100000
                }
                , cols: [[
                    {field: 'id', title: '角色ID'},
                    {field: 'user_name', title: '姓名'},
                    {field: 'account', title: '手机号'},
                    {field: 'role_name', title: '用户角色'},
                    {field: 'status', title: '状态'},
                    {
                        field: 'region_id', title: '操作', width: 120, templet: function (d) {
                            return '<i data-id="' + d.id + '" class="layui-icon layui-icon-edit edit-icon" title="编辑"  style="margin-right: 40px;cursor:pointer;">&#xe642;</i><i data-id="' + d.id + '" style="cursor: pointer" class="layui-icon delete-icon"  title="删除" >&#xe640;</i>'
                        }
                    }
                ]],
                done: function (res) {
                    layer.closeAll('loading');
                    $('.edit-icon').click(function () {
                        var content = $(this).parents('tr').children('td:eq(1)').find('.layui-table-cell').text();
                        /*设置全局变量，函数外访问*/
                        user_id = $(this).attr('data-id');
                        phone = $(this).parents('tr').children('td:eq(2)').find('.layui-table-cell').text();
                        var location = $(this).parents('tr').children('td:eq(2)').find('.layui-table-cell').text();
                        $('#name_edit').val(content);
                        layer.open({
                            type: 1,
                            title: '编辑信息',
                            closeBtn: 1,
                            shadeClose: true,
                            area: ['460px', '290px'],
                            skin: "layui-layer-molv",
                            content: $('#popup_one')
                        });
                    });
                    $('#confirm_add').click(function (e) {
                        e.preventDefault()
                        var phone_number = $('#phone_number').val();
                        var role_id = $('#role_id').val();
                        var user_name = $('#user_name').val();
                        var add_user_password = $('#add_user_password').val();
                        var url = '/root/management/';
                        var data = {
                            "account": phone_number,
                            "user_name": user_name,
                            "password": add_user_password,
                            "role_id": role_id
                        };
                        data = JSON.stringify(data);
                        http.ajax.post_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            if (res.status == 100000) {
                                layer.msg('添加成功', {
                                    time: 700
                                })
                            }
                            setTimeout(function () {
                                layer.closeAll();
                                window.location.reload();
                            }, 700)
                        }, function (xhttp) {
                            if (xhttp.responseJSON.status != 100000) {
                                layer.msg('失败', {
                                    time: 1000
                                });
                                setTimeout(function () {
                                    layer.closeAll()
                                }, 1000)
                            }
                        })
                    });
                    $('#confirm_fix').click(function () {
                        var name_edit = $('#name_edit').val();
                        var password = $('#password').val();
                        var role_id =  $('#user_id').val();
                        var data = {
                            "account": phone,
                            "user_name": name_edit,
                            "password": password,
                            "role_id":role_id,
                            "is_active":$('input[name=role]:checked').val()
                        };
                        data = JSON.stringify(data);
                        var url = '/root/management/' + user_id;
                        http.ajax.put_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            if (res.status == 100000) {
                                layer.msg('修改成功', {
                                    time: 700
                                });
                                setTimeout(function () {
                                    layer.closeAll(); //
                                    tableIns.reload()
                                }, 700)
                            }
                        }, function (xhttp) {
                            if (xhttp.responseJSON.status != 100000) {
                                layer.msg('失败', {
                                    time: 1000
                                });
                                setTimeout(function () {
                                    layer.closeAll()
                                }, 1000)
                            }
                        })
                    });
                    $('.delete-icon').click(function () {
                        var user_id = $(this).attr('data-id');
                        layer.confirm('确定要删除？', {
                            skin: 'layui-layer-molv',
                            btn: ['确认', '取消']
                        }, function () {
                            var url = '/root/management/' + user_id;
                            $.ajax({
                                type: 'delete',
                                url: url,
                                dataType: 'json',
                                success: function (res) {
                                    if (res.status == 100000) {
                                        layer.msg('删除成功', {
                                            time: 700,
                                        });
                                        setTimeout(function () {
                                            tableIns.reload();
                                        }, 700)
                                    }
                                },
                                error: function () {

                                },
                                complete: function (xhttp) {
                                    if (xhttp.responseJSON.status != 100000) {

                                        layer.msg('普通管理员无权限', {
                                            time: 1000
                                        })
                                        setTimeout(function () {
                                            layer.closeAll()
                                        }, 1000)
                                    }
                                }
                            });

                        }, function () {

                        });
                    })
                },
                page: {
                    layout: ['count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                    , groups: 1 //只显示 1 个连续页码
                    , first: false //不显示首页
                    , last: false //不显示尾页
                },
                id: 'dataTable'
            })
            /*---------------------------------------------------------*/
            /*从这里是角色管理*/
            /*从这里是角色管理*/
            var tableRender = table.render({
                elem: '#root_city_table',
                even: true,
                url: role_url,
                skin: 'nob',
                response: {
                    statusName: 'status',
                    statusCode: 100000
                }
                , cols: [[
                    {field: 'role_name', title: '身份信息'},
                    {field: 'region_id', title: '城市id'},
                    {field: 'region_name', title: '管理城市'},
                    {field: 'page_name', title: '管理页面'},
                    {
                        field: 'region_id', title: '操作', width: 120, templet: function (d) {
                            return '<i data-id="' + d.id + '" class="layui-icon layui-icon-edit edit-operate" title="编辑"  style="margin-right: 40px;cursor:pointer;">&#xe642;</i><i data-id="' + d.id + '" style="cursor: pointer" class="layui-icon delete-operate"  title="删除" >&#xe640;</i>'
                        }
                    }
                ]],
                done: function (res) {
                    layer.closeAll('loading');
                    $('.edit-operate').click(function () {
                        /* var content = $(this).parents('tr').children('td:eq(0)').find('.layui-table-cell').text();
                         user_id = $(this).attr('data-id');
                         phone = $(this).parents('tr').children('td:eq(1)').find('.layui-table-cell').text();
                         var location = $(this).parents('tr').children('td:eq(2)').find('.layui-table-cell').text();
                         $('#name_edit').val(content);
                         $('#city_picker_search_second').val(location);*/
                        layer.open({
                            type: 1,
                            title: '编辑信息',
                            closeBtn: 1,
                            shadeClose: true,
                            area: ['550px', '320px'],
                            skin: "layui-layer-molv",
                            content: $('#popup_two')
                        });
                    });
                    $('#confirm_add_root').click(function () {
                        var phone_number = $('#phone_number').val();
                        var city_picker_search = $('#city_picker_search').attr('cityid');
                        var user_name = $('#user_name').val();
                        var add_user_password = $('#add_user_password').val();
                        var url = '/root/management/';
                        var data = {
                            "account": phone_number,
                            "user_name": user_name,
                            "password": add_user_password,
                            "region_id": city_picker_search
                        };
                        data = JSON.stringify(data);
                        http.ajax.post_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            if (res.status == 100000) {
                                layer.msg('添加成功', {
                                    time: 700
                                })
                            }
                            setTimeout(function () {
                                layer.closeAll();
                                tableIns.reload();
                            }, 700)
                        }, function (xhttp) {
                            if (xhttp.responseJSON.status != 100000) {
                                layer.msg('普通管理员无权限', {
                                    time: 1000
                                });
                                setTimeout(function () {
                                    layer.closeAll()
                                }, 1000)
                            }
                        })
                    });
                    /*$('#confirm_fix').click(function () {
                        var name_edit = $('#name_edit').val();
                        var password = $('#password').val();
                        var city_picker_search_second = $('#city_picker_search_second').attr('cityid');
                        var data = {
                            "account": phone,
                            "user_name": name_edit,
                            "password": password,
                            "region_id": city_picker_search_second
                        };
                        data = JSON.stringify(data);
                        var url = '/root/management/' + user_id;
                        http.ajax.put_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            if (res.status == 100000) {
                                layer.msg('修改成功', {
                                    time: 700
                                });
                                setTimeout(function () {
                                    layer.closeAll(); //
                                    tableIns.reload()
                                }, 700)
                            }
                        }, function (xhttp) {
                            if (xhttp.responseJSON.status != 100000) {
                                layer.msg('普通管理员无权限', {
                                    time: 1000
                                });
                                setTimeout(function () {
                                    layer.closeAll()
                                }, 1000)
                            }
                        })
                    });
                    $('.delete-icon').click(function () {
                        var user_id = $(this).attr('data-id');
                        layer.confirm('确定要删除？', {
                            skin: 'layui-layer-molv',
                            btn: ['确认', '取消']
                        }, function () {
                            var url = '/root/management/' + user_id;
                            $.ajax({
                                type: 'delete',
                                url: url,
                                dataType: 'json',
                                success: function (res) {
                                    if (res.status == 100000) {
                                        layer.msg('删除成功', {
                                            time: 700,
                                        });
                                        setTimeout(function () {
                                            tableIns.reload();
                                        }, 700)
                                    }
                                },
                                error: function () {

                                },
                                complete: function (xhttp) {
                                    if (xhttp.responseJSON.status != 100000) {

                                        layer.msg('普通管理员无权限', {
                                            time: 1000
                                        })
                                        setTimeout(function () {
                                            layer.closeAll()
                                        }, 1000)
                                    }
                                }
                            });

                        }, function () {

                        });
                    })*/
                },
                page: {
                    layout: ['count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                    , groups: 1 //只显示 1 个连续页码
                    , first: false //不显示首页
                    , last: false //不显示尾页
                },
                id: 'managerTable'
            })
        })
    },
    addUser: function () {
        var _that = this;
        $('#city_picker_search').address({
            level: 2,
            offsetLeft: 0
        });
        $('#city_picker_search_second').address({
            level: 2,
            offsetLeft: 0
        });
        $('#add_user').click(function () {
            layer.open({
                type: 1,
                title: '新增城市经理',
                closeBtn: 1,
                shadeClose: true,
                area: ['450px', '300px'],
                skin: "layui-layer-molv",
                content: $('#popup')
            });

        })
        $('#add_user_city_manager').click(function (e) {
            e.preventDefault();
            /*不想分页就写100*/
            var url = '/root/page_management/?page=1&limit=100';
            http.ajax.get_no_loading(true,false,url,{},http.ajax.CONTENT_TYPE_2,function(res){
                var page_list = res.data.page_list;
                var str = '';
                for(var i =0;i<page_list.length;i++){
                    str+='<input type="checkbox" data-id="'+page_list[i].page_id+'" name="like[root_page_'+i+']" title='+page_list[i].page_name+'>'
                }
                $('.checkbox').html(str);
                /*告诉layui重载*/
                form.render(null,'add_root');
            });
            layer.open({
                type: 1,
                title: '新增城市经理',
                closeBtn: 1,
                shadeClose: true,
                area: ['512px', '320px'],
                skin: "layui-layer-molv",
                content: $('#popup_three')
            });

        })
    },
    edit: function () {
        var _that = this;
    }
};
set.init();
set.addUser();
set.edit()