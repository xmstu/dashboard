var set = {
    init: function () {
        $('.menu-power').addClass('menu-active');
        $('.menu-active .icon-xia').addClass('icon-rotate');
        $('.menu-power').next('.second-menu-list').css({'display': 'block'});
        $('.menu-power').next('.second-menu-list').find('.userManager-second-menu').addClass('selected-active')
        var _this = this;
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
                    {field: 'id', title: '用户ID'},
                    {field: 'user_name', title: '姓名'},
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
                    /*打开用户编辑弹窗*/
                    $('.edit-icon').click(function () {
                        var content = $(this).parents('tr').children('td:eq(1)').find('.layui-table-cell').text();
                        /*设置全局变量，函数外访问*/
                        user_id = $(this).attr('data-id');
                        var location = $(this).parents('tr').children('td:eq(2)').find('.layui-table-cell').text();
                        $('#name_edit').val(content);
                        /**/
                        var url = '/root/management/' + user_id;
                        http.ajax.get_no_loading(true, false, url, {}, http.ajax.CONTENT_TYPE_2, function (res) {
                            console.log(res);
                            var role_list = res.data;
                            var str = '';
                            if (role_list) {
                                for (var i = 0; i < role_list.length; i++) {
                                    str += '<input type="checkbox"  check' + _this.check(role_list[i].status)+ ' lay-filter="checkbox" data-filter="role_checkbox" data-id="' + role_list[i].role_id + '" name="like[root_list_' + i + ']" title=' + role_list[i].name + '>'
                                }
                                $('.edit-user-checkbox').html(str);
                            }
                            /*告诉layui重载*/
                            form.render(null, 'edit_user');
                            layer.closeAll('loading')
                        });
                        layer.open({
                            type: 1,
                            title: '编辑信息',
                            closeBtn: 1,
                            shadeClose: true,
                            area: ['600px', '500px'],
                            skin: "layui-layer-molv",
                            content: $('#popup_one')
                        });
                    });
                    /*用户添加*/
                    $('#confirm_add').click(function (e) {
                        e.preventDefault();
                        var user_command = $('#user_comment_add').val();
                        var role_id = $('#role_id').val();
                        var user_name = $('#user_name').val();
                        var add_user_password = $('#add_user_password').val();
                        var user_id_arr = [];
                        /*监听layui生成的元素*/
                        $('.user-checkbox .layui-unselect').each(function (val) {
                            if ($(this).is('.layui-form-checked')) {
                                user_id_arr.push($(this).prev().attr('data-id'))
                            }
                        });
                        console.log(user_id_arr);
                        var url = '/root/management/';
                        var data = {
                            "comment": user_command,
                            "user_name": user_name,
                            "password": add_user_password,
                            "role_id": user_id_arr
                        };
                        data = JSON.stringify(data);
                        http.ajax.post_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            if (res.status == 100000) {
                                layer.msg('添加成功', function(){
                                    window.location.reload();
                                })
                            }

                        }, function (xhttp) {
                            if (xhttp.responseJSON.status != 100000) {
                                layer.msg('失败', function(){
                                    layer.closeAll()
                                });

                            }
                        })
                    });
                    /*确定用户修改*/
                    $('#confirm_fix').click(function () {
                        var name_edit = $('#name_edit').val();
                        var password = $('#password').val();
                         var role_id_arr = [];
                        /*监听layui生成的元素*/
                        $('.edit-user-checkbox .layui-unselect').each(function (val) {
                            if ($(this).is('.layui-form-checked')) {
                                role_id_arr.push($(this).prev().attr('data-id'))
                            }
                        });

                        var data = {
                            "comment": $('#user_comment_edit').val(),
                            "user_name": name_edit,
                            "password": hex_md5(password),
                            "role_id": role_id_arr,
                            "is_active": Number($('input[name=role]:checked').val())
                        };
                        data = JSON.stringify(data);
                        var url = '/root/management/' + user_id;
                        http.ajax.put_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            if (res.status == 100000) {
                                layer.msg('修改成功',function(){
                                     window.location.reload()
                                });
                            }
                        }, function (xhttp) {
                            if (xhttp.responseJSON.status != 100000) {
                                layer.msg('失败', function(){
                                    layer.closeAll("loading")
                                });
                            }
                        })
                    });
                    /*删除用户*/
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
                                        layer.msg('删除成功',function(){
                                            window.location.reload();
                                        });
                                    }
                                },
                                error: function () {

                                },
                                complete: function (xhttp) {
                                    if (xhttp.responseJSON.status != 100000) {
                                        layer.msg('失败', function(){
                                            layer.closeAll()
                                        })
                                    }
                                }
                            });

                        }, function () {

                        });
                    })
                },
                page: {
                    layout: ['count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                    , first: true //不显示首页
                    , last: true //不显示尾页
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
                    {field: 'id', title: "角色ID"},
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
                    /*编辑图标点击*/
                    $('.edit-operate').click(function () {
                        var content = $(this).parents('tr').children('td:eq(0)').find('.layui-table-cell').text();
                        role_id = $(this).attr('data-id');
                        $('#role_name_edit').val(content);
                        var url = '/root/role_management/' + role_id;
                        http.ajax.get_no_loading(true, false, url, {}, http.ajax.CONTENT_TYPE_2, function (res) {
                            console.log(res.data);
                            var page_list = res.data;
                            var str = '';
                            for (var i = 0; i < page_list.length; i++) {
                                console.log(page_list[i].status)
                                str += '<input type="checkbox"  check' + _this.check(page_list[i].status) + ' lay-filter="edit_role" data-filter="edit_role_checkbox" data-id="' + page_list[i].page_id + '" name="like[root_edit_' + i + ']" title=' + page_list[i].name + '>'
                            }
                            $('.edit-checkbox').html(str);
                            /*告诉layui重载*/
                            form.render(null, 'edit_root');
                            layer.closeAll('loading')
                        });
                        layer.open({
                            type: 1,
                            title: '新增城市经理',
                            closeBtn: 1,
                            shadeClose: true,
                            area: ['560px', '520px'],
                            skin: "layui-layer-molv",
                            content: $('#popup_two')
                        });
                        layer.closeAll('loading')
                    });
                    /*添加*/
                    $('#confirm_add_root').click(function (e) {
                        e.preventDefault();
                        var role_name = $('#role_name_add').val();
                        var region_id = $('#area_add').val();
                        var type = $('#role_add').val();
                        var role_comment_edit = $('#role_comment_add').val();
                        var page_id_arr = [];
                        /*监听layui生成的元素*/
                        $('.checkbox .layui-unselect').each(function (val) {
                            if ($(this).is('.layui-form-checked')) {
                                page_id_arr.push($(this).prev().attr('data-id'))
                            }
                        });
                        console.log(page_id_arr);
                        var url = '/root/role_management/';
                        var data = {
                            "type": type,
                            "role_name": role_name,
                            "role_comment": role_comment_edit,
                            "region_id": region_id,
                            "page_id_list": page_id_arr
                        };
                        data = JSON.stringify(data);
                        http.ajax.post_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            console.log(res)
                            if (res.status == 100000) {
                                layer.msg('添加成功',function(){
                                  layer.closeAll();
                                window.location.reload();
                                })
                            }
                        }, function (xHttp) {
                            layer.closeAll('loading')
                        })
                    });
                    /*编辑*/
                    $('#confirm_edit_root').click(function (e) {
                        e.preventDefault();
                        var role_name = $('#role_name_edit').val();
                        var region_id = $('#area_edit').val();
                        var type = $('#role_edit').val();
                        var role_comment_edit = $('#role_comment_edit').val();
                        var page_id_arr = [];
                        /*监听layui生成的元素*/
                        $('.edit-checkbox .layui-unselect').each(function (val) {
                            if ($(this).is('.layui-form-checked')) {
                                page_id_arr.push(Number($(this).prev().attr('data-id')))
                            }
                        });
                        console.log(page_id_arr);
                        var url = '/root/role_management/' + role_id;
                        var data = {
                            "type": type,
                            "role_name": role_name,
                            "role_comment": role_comment_edit,
                            "region_id": region_id,
                            "page_id_list": page_id_arr
                        };
                        data = JSON.stringify(data);
                        http.ajax.put_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                            if (res.status == 100000) {
                                layer.msg('修改成功',function(){
                                   window.location.reload();
                                })
                            }
                        }, function (xHttp) {
                            layer.closeAll('loading')
                        })
                    });
                    /*删除*/
                    $('.delete-operate').click(function () {
                        var user_id = $(this).attr('data-id');
                        layer.confirm('确定要删除？', {
                            skin: 'layui-layer-molv',
                            btn: ['确认', '取消']
                        }, function () {
                            var url = '/root/role_management/' + user_id;
                            $.ajax({
                                type: 'delete',
                                url: url,
                                dataType: 'json',
                                success: function (res) {
                                    if (res.status == 100000) {
                                        layer.msg('删除成功', function(){
                                            window.location.reload();
                                        });
                                    }
                                },
                                error: function () {

                                },
                                complete: function (xhttp) {
                                    layer.closeAll('loading')
                                    if (xhttp.responseJSON.status != 100000) {

                                        layer.msg('失败', function(){
                                            layer.closeALl()
                                        })
                                    }
                                }
                            });

                        }, function () {

                        });
                    })

                },
                page: {
                    layout: ['count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                    , first: true //不显示首页
                    , last: true //不显示尾页
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
            /*获取所有角色列表*/
            var url = '/root/management/' + 0;
            http.ajax.get_no_loading(true, false, url, {}, http.ajax.CONTENT_TYPE_2, function (res) {
                console.log(res);
                var role_list = res.data;
                var str = '';
                if (role_list) {
                    for (var i = 0; i < role_list.length; i++) {
                        str += '<input type="checkbox" lay-filter="checkbox" data-filter="role_checkbox" data-id="' + role_list[i].role_id + '" name="like[root_list_' + i + ']" title=' + role_list[i].name + '>'
                    }
                    $('.user-checkbox').html(str);
                }
                /*告诉layui重载*/
                form.render(null, 'add_user');
                layer.closeAll('loading')
            });
            layer.open({
                type: 1,
                title: '修改角色信息',
                closeBtn: 1,
                shadeClose: true,
                area: ['550px', '450px'],
                skin: "layui-layer-molv",
                content: $('#popup')
            });

        })
        $('#add_user_city_manager').click(function (e) {
            e.preventDefault();
            /*获取所有页面列表--不想分页就写100*/
            var url = '/root/page_management/?page=1&limit=10';
            http.ajax.get_no_loading(true, false, url, {}, http.ajax.CONTENT_TYPE_2, function (res) {
                var page_list = res.data;
                var str = '';
                for (var i = 0; i < page_list.length; i++) {
                    str += '<input type="checkbox" lay-filter="checkbox" data-filter="role_checkbox" data-id="' + page_list[i].page_id + '" name="like[root_page_' + i + ']" title=' + page_list[i].page_name + '>'
                }
                $('.checkbox').html(str);
                /*告诉layui重载*/
                form.render(null, 'add_root');
                layer.closeAll('loading')
            });
            layer.open({
                type: 1,
                title: '新增角色',
                closeBtn: 1,
                shadeClose: true,
                area: ['560px', '520px'],
                skin: "layui-layer-molv",
                content: $('#popup_three')
            });

        })
    },
    edit: function () {
        var _that = this;
    },
    check: function (str) {
        if (str == 0) {
            return 'e'
        } else if (str == 1) {
            return 'ed'
        }
    }
};
set.init();
set.addUser();
set.edit();