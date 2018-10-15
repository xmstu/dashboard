var set = {
    init: function () {
        layui.use(['layer', 'laydate'], function () {
            var layer = layui.layer;
            var laydate = layui.laydate;
            laydate.render({
                elem: '#delivery_start_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#delivery_start_time').val();
                    var endTime = $('#delivery_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#delivery_start_time').val());
                    var endTime = common.timeTransform($('#delivery_end_time').val());
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#delivery_start_time').val() == '') {
                        $('#delivery_start_time').next('.date-tips').show();
                    } else {
                        $('#delivery_start_time').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#delivery_end_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#delivery_start_time').val();
                    var endTime = $('#delivery_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#delivery_start_time').val())
                    var endTime = common.timeTransform($('#delivery_end_time').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#delivery_end_time').val() == '' || val == '') {
                        $('#delivery_end_time').next('.date-tips').show();
                    } else {
                        $('#delivery_end_time').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#register_start_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#register_start_time').val();
                    var endTime = $('#register_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#register_start_time').val())
                    var endTime = common.timeTransform($('#register_end_time').val())
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#register_start_time').val() == '' || val == '') {
                        $('#register_start_time').next('.date-tips').show();
                    } else {
                        $('#register_start_time').next('.date-tips').hide()
                    }
                }
            });
            laydate.render({
                elem: '#register_end_time',
                theme: '#009688',
                max: String(common.getNowFormatDate()[0]),
                calendar: true,
                format: 'yyyy/MM/dd',
                done: function (val, index) {
                    var startTime = $('#register_start_time').val();
                    var endTime = $('#register_end_time').val();
                    common.dateInterval(endTime, startTime);
                    var startTime = common.timeTransform($('#date_show_one').val());
                    var endTime = common.timeTransform($('#date_show_two').val());
                    if (startTime > endTime) {
                        layer.msg('提示：开始时间大于了结束时间！');
                        return false;
                    }
                    if ($('#register_end_time').val() == '' || val == '') {
                        $('#register_end_time').next('.date-tips').show();
                    } else {
                        $('#register_end_time').next('.date-tips').hide()
                    }
                }
            });
        });
        $('.menu-map').addClass('menu-active');
        $('.menu-active .icon-xia').addClass('icon-rotate');
        $('.menu-map').next('.second-menu-list').css({'display': 'block'});
        $('.menu-map').next('.second-menu-list').find('.goodsMap-second-menu').addClass('selected-active')
    },
    mapRender: function (heatMapData, maxCount, center) {
        //******根据权限等级限制缩放等级******
        var zoom;
        var role = $('#user-info').attr('data-role-type');//头部可获取登陆用户的等级 1代表超管
        if (role == 1) {
            zoom = 6
        } else {
            zoom = 11
        }
        center ? center = center : center = [116.418261, 39.921984];//中心点
        //******根据权限等级限制缩放等级******

        //******定义地图对象******
        var map = new AMap.Map("container", {
            resizeEnable: true,
            center: center,
            zoom: zoom,
            zooms: [zoom, 14]
        });
        //******定义地图对象******
        if (!isSupportCanvas()) {
            layer.msg('热力图仅对支持canvas的浏览器适用,您所使用的浏览器不能使用热力图功能,请换个浏览器试试~', {
                time: 1500
            })
        }

        //******热力点分布******
        var heatmap;
        map.plugin(["AMap.Heatmap"], function () {
            //初始化heatmap对象
            heatmap = new AMap.Heatmap(map, {
                radius: 10, //给定半径
                opacity: [0.8, 1],
                gradient: {
                    0.1: '#ffffff',
                    0.3: '#00cc04',
                    0.5: '#ffea00',
                    0.8: '#ef7a82',
                    1.0: 'red'
                }
            });
            //设置数据集：该数据为北京部分“公园”数据
            heatmap.setDataSet({
                data: heatMapData,//接口数据
                // data: heatmapData,//模拟数据
                max: 3
            });
            //******热力点分布******
            //******在指定位置打开信息窗体******
            var infoWindow;

            function openInfo(position, infomation) {
                console.log(infomation);
                //构建信息窗体中显示的内容
                var info = [];
                //info.push("<div><div><img style=\"float:left; width: 100px;\" src=\" /static/images/loading.gif \"/></div> ");
                info.push("<div style=\"padding:0px 0px 0px 4px;\"><b>省省回头车</b>");
                info.push("货源量:" + infomation.data.sum_count);
                info.push("地址 :" + address + "</div></div>");
                infoWindow = new AMap.InfoWindow({
                    content: info.join("<br/>"),  //使用默认信息窗体框样式，显示信息内容
                    offset: new AMap.Pixel(0, -30),//信息窗体的相对位置
                    autoMove: true,
                    showShadow: true
                });
                infoWindow.open(map, position);
            }

            //******在指定位置打开信息窗体******
            //******地图控件******
            var scale = new AMap.Scale({
                    visible: false
                }),
                toolBar = new AMap.ToolBar({
                    visible: false
                }),
                overView = new AMap.OverView({
                    visible: false
                });
            map.addControl(scale);
            // map.addControl(toolBar);
            //map.addControl(overView);
            scale.show();
            //******地图控件******
            //******逆地理编码-通过经纬度获取地址******
            var geocoder;
            var address = "";

            function regeoCode(lnglat) {
                if (!geocoder) {
                    geocoder = new AMap.Geocoder({
                        city: "010", //城市设为北京，默认：“全国”
                        radius: 1000 //范围，默认：500
                    });
                }
                geocoder.getAddress(lnglat, function (status, result) {
                    if (status === 'complete' && result.regeocode) {
                        var adcode = result.regeocode.addressComponent.adcode;
                        address = result.regeocode.formattedAddress;
                        //获取相邻最近的用户经纬度以及相关字段信息
                        Getuserinfo("/map/goods_map/", lnglat, adcode, function (info) {
                            openInfo(lnglat, info);
                            add_marker(lnglat);//添加marker标记
                        });

                    } else {
                        layer.msg('不在服务范围内...')
                        //alert(JSON.stringify(result))
                    }
                });
            }

            //******逆地理编码-通过经纬度获取地址******
            //******ajax获取用户信息******
            function Getuserinfo(url, lnglat, adcode, fun) {
                if (map.getZoom() < 10) {
                    //缩放到11等级，才允许点击
                    layer.msg('范围太大，请缩放地图调整光点位置');
                    return false;
                }
                if (adcode.length <= 0) {
                    layer.msg('获取地图信息失败，请重新尝试！');
                    return false;
                }
                var Zoom_s = {10: 2.5, 11: 1.25, 12: 0.5, 13: 0.25, 14: 0.125}
                console.log('辐射范围倍数：' + Zoom_s[map.getZoom()]);
                var data = {
                    "lat": lnglat[1],
                    "lng": lnglat[0],
                    "region_id": adcode,
                    "multiple": Zoom_s[map.getZoom()],//倍数基本单位是1km
                    goods_price_type: $('#goods_price_type').val(),
                    haul_dist: $('#haul_dist').val(),
                    vehicle_length: $('#vehicle_length').val(),
                    goods_status: $('#goods_status').val(),
                    special_tag: $('#special_tag').val(),
                    delivery_start_time: common.timeTransform($('#delivery_start_time').val()+ ' 00:00:00'),
                    delivery_end_time: common.timeTransform($('#delivery_end_time').val() + ' 23:59:59'),
                    register_start_time:common.timeTransform($('#register_start_time').val() + ' 00:00:00'),
                    register_end_time: common.timeTransform($('#register_end_time').val() + ' 23:59:59')
                };
                console.log(data);
                data = JSON.stringify(data);
                http.ajax.post(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                    if (res.status == 100000) {
                        if (res.data.sum_count == 0 || res.data.lng == 0) {
                            //返回值经纬度为0
                            layer.msg('没有相关信息点！');
                            map.remove(m);//移除marker标记
                            infoWindow.close();//关闭信息窗体
                        }
                        else {
                            fun(res);
                        }
                    }
                }, function (xhttp) {
                    if (xhttp.responseJSON.status != 100000) {
                        layer.msg('失败', function () {
                            layer.closeAll("loading")
                        });
                    }
                })
            }

            //******ajax获取用户信息******
            //******创建矩形******
            function createRec(LngLat) {
                //未完成  暂停！
                //基础方法：根据当前点击经纬度 换算半径1000米后的四个经纬度点给后台，后台判断回传
                //var south=LngLat[0]-2500；
                var southWest = new AMap.LngLat(116.356449, 39.859008)
                var northEast = new AMap.LngLat(116.417901, 39.893797)
                var bounds = new AMap.Bounds(southWest, northEast)
                var rectangle = new AMap.Rectangle({
                    bounds: bounds,
                    strokeColor: 'red',
                    strokeWeight: 6,
                    strokeOpacity: 0.5,
                    strokeDasharray: [30, 10],
                    // strokeStyle还支持 solid
                    strokeStyle: 'dashed',
                    fillColor: 'blue',
                    fillOpacity: 0.5,
                    cursor: 'pointer',
                    zIndex: 50,
                })
                rectangle.setMap(map)
                // 缩放地图到合适的视野级别
                map.setFitView([rectangle])
            }

            //******创建矩形******
            //******增加标记marker，并移除上一个marker******
            var m = {};

            function add_marker(LngLat) {
                map.remove(m);
                var m1 = new AMap.Marker({
                    position: LngLat,
                    animation: 'AMAP_ANIMATION_DROP',
                    title: address
                    //icon: "https://webapi.amap.com/theme/v1.3/markers/n/mark_r.png"
                });
                m = m1;
                map.add(m1);
            }

            //******增加标记marker，并移除上一个marker******
            map.on('click', function (e) {
                console.log(heatmap.getMap());
                var LngLat = [e.lnglat.getLng(), e.lnglat.getLat()];
                regeoCode(LngLat);//经纬度->地址
                $(".weather-city-search").html("地图-经纬度:" + LngLat[0] + "," + LngLat[1] + "  缩放级别：" + map.getZoom());
            });
            map.on('rightclick', function (e) {
                map.remove(m);//移除marker标记
                $(".weather-city-search").html("");//清空头部信息
                infoWindow.close();//关闭信息窗体
            });

            $('#heatMapHide').click(function () {
                heatmap.hide();
            });
            $('#heatMapShow').click(function () {
                heatmap.show();
                console.log(heatmap.getMap());
                console.log(heatmap.getOptions());
                console.log(heatmap.getDataSet());
            });
        });

        //判断浏览区是否支持canvas
        function isSupportCanvas() {
            var elem = document.createElement('canvas');
            return !!(elem.getContext && elem.getContext('2d'));
        }
    },
    operate: function () {
        var _this = this;
        var url = '/map/goods_map/';
        var data = {
            goods_price_type: $('#goods_price_type').val(),
            haul_dist: $('#haul_dist').val(),
            vehicle_length: $('#vehicle_length').val(),
            goods_status: $('#goods_status').val(),
            special_tag: $('#special_tag').val(),
            delivery_start_time: $('#delivery_start_time').val(),
            delivery_end_time: $('#delivery_end_time').val(),
            register_start_time: $('#register_start_time').val(),
            register_end_time: $('#register_end_time').val()
        };
        console.log(data)
        if (data.delivery_start_time != '') {
            data.delivery_start_time = common.timeTransform($('#delivery_start_time').val() + ' 00:00:00');
        }
        if (data.delivery_end_time != '') {
            data.delivery_end_time = common.timeTransform($('#delivery_end_time').val() + ' 23:59:59');
        }
        if (data.register_start_time != '') {
            data.register_start_time = common.timeTransform($('#register_start_time').val() + ' 00:00:00');
        }
        if (data.register_end_time != '') {
            data.register_end_time = common.timeTransform($('#register_end_time').val() + ' 23:59:59');
        }
        layui.use('layer', function () {
            var layer = layui.layer;
            http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
                if (res.data == '') {
                    layer.msg('该条件无数据！', {icon: 5});
                } else {
                    var heatMapData = res.data;
                    var maxCount = res.max_lat_lng.max_count;
                    var center = [];
                    center.push(res.max_lat_lng.lng);
                    center.push(res.max_lat_lng.max_lat);
                    _this.mapRender(heatMapData, maxCount, center)
                }
            }, function (xhttp) {
                layer.closeAll('loading')
            })
        })
    }
};
set.operate();
set.init();
set.mapRender();
$('#search_btn').click(function (e) {
    e.preventDefault();
    set.operate();
});

