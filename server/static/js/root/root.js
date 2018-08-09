var set = {
    init: function () {
        var secondMenu = document.getElementById('second_menu_list');
        secondMenu.style.display = 'block';
        $('#second_menu_list>li:nth-of-type(2) a').addClass('selected-active');
        $('#second_menu_box').addClass('menu-active')
        layui.use(['layer', 'table'], function () {
            var layer = layui.layer;
            var table = layui.table;
            var url = '/root/management/'
            var tableIns = table.render({
                elem: '#root_table',
                even: true,
                url: url,
                skin: 'nob',
                response: {
                    statusName: 'status',
                    statusCode: 100000
                }
                , cols: [[
                    {field: 'user_name', title: '姓名'},
                    {field: 'account', title: '手机号'},
                    {field: 'region_name', title: '所属城市'},
                    {
                        field: 'region_id', title: '操作', width: 120, templet: function (d) {
                            return '<i data-number="' + d.account + '" class="layui-icon layui-icon-edit edit-icon" title="编辑"  style="margin-right: 40px;cursor:pointer;">&#xe642;</i><i data-id="' + d.id + '" style="cursor: pointer" class="layui-icon delete-icon"  title="删除" >&#xe640;</i>'
                        }
                    }
                ]],
                done: function (res) {
                    layer.closeAll('loading');
                    $('.edit-icon').click(function () {
                        var content = $(this).parents('tr').children('td:eq(0)').find('.layui-table-cell').text();
                        var location = $(this).parents('tr').children('td:eq(2)').find('.layui-table-cell').text();
                        $('#name_edit').val(content);
                        $('#city_picker_search_second').val(location);
                        layer.open({
                            type: 1,
                            title: '编辑信息',
                            closeBtn: 1,
                            shadeClose: true,
                            scrollbar: false,
                            area: ['450px', '270px'],
                            skin: "layui-layer-molv",
                            content: $('#popup_one')
                        });
                    });
                    $('#confirm_add').click(function () {
                        var name_edit = $('#name_edit').val();
                        var password = $('#password').val();
                        var city_picker_search_second = $('#city_picker_search_second').val();
                        var phone = $(this).attr('data-number');
                        var data = {
                            "account": phone,
                            "user_name": name_edit,
                            "password": password,
                            "region_id": city_picker_search_second
                        };
                        var url = '/root/management/';
                        http.ajax.post_no_loading(true, false, url,data,http.ajax.CONTENT_TYPE_2,function(res){
                            console.log(res)
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
                                    console.log(res);
                                    if (res.status == 100000) {
                                        layer.msg('删除成功', {
                                            time: 1000,
                                        });
                                        setTimeout(function () {
                                            tableIns.reload();
                                        }, 1000)
                                    }
                                },
                                error: function () {

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
        })
    },
    addUser: function () {
        var _that = this;
        $('#city_picker_search').address({
            level: 2,
            offsetLeft: 0
        });
        $('#add_user').click(function () {
            layer.open({
                type: 1,
                title: '新增城市经理',
                closeBtn: 1,
                shadeClose: true,
                scrollbar: false,
                area: ['450px', '270px'],
                skin: "layui-layer-molv",
                content: $('#popup')
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