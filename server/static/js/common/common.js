var common = {
    display: function (elem) {
        elem.css({'display': 'none'})
    },
    sliderShow: function () {
        $('.tools-tip-icon').mouseenter(function () {
            $('.introduce_tools').addClass('r-0');
            $(this).css({display: 'none'})
        });
        $('.introduce_tools>a').mouseleave(function () {
            if ($('.introduce_tools').css('right') == '0px') {
                $('.tools-tip-icon').css({display: 'block'});
                $('.introduce_tools').removeClass('r-0')
            }
        })
    },
    /*消息框显示隐藏*/
    showData: function (elem, elem2) {
        $(elem).mouseenter(function () {
            if ($(elem2).is(':hidden')) {
                $(elem2).slideDown(100);
                $(elem).html('&#xe619;')
            }
        });
        $(elem).mouseleave(function () {
            $(elem2).slideUp(100);
            $(elem).html('&#xe61a;');
            return false
        })
    },
    init: function () {
        layui.use(['element', 'layer', 'form'], function () {
            var layer = layui.layer;
            var form = layui.form;
            var element = layui.element;
            var clearBtn = $('.clear-select');
            clearBtn.on('click', function () {
                $('#is_called').val("");
                $('#select').reset()
            })
        });
        /*退出登陆*/
        $('.loginOut').click(function () {
            layer.confirm('您确定要退出登陆？', {
                skin: 'layui-layer-molv',
                btn: ['取消', '确定  '] //按钮
            }, function (index) {
                layer.close(index);
            }, function () {
                var url = '/login/';
                $.ajax({
                    url: url,
                    type: 'delete',
                    beforeSend: function () {
                        var index = layer.load(1, {
                            shade: [0.1, '#fff'] //0.1透明度的白色背景
                        });
                    },
                    success: function (res) {
                        if (res.status == 100000) {
                            layer.closeAll('loading');
                            window.location.href = '/login/'
                        }
                    }
                });
            });
        });
        /*根据cookie中menuStatus的值来显示侧边栏的宽度*/
        var menuStatus = $.cookie('menuStatus');
        if (menuStatus == 'true') {
            $('.icon-caidan').click()
        }
    },
    fullScreen: function () {
        var full_screen = $('#fullScreen');
        full_screen.on('click', function () {
            if ($(this).find('strong').text() == '开启全屏展示') {

            } else {
                var el = document;
                var cfs = el.cancelFullScreen || el.webkitCancelFullScreen ||
                    el.mozCancelFullScreen || el.exitFullScreen;
                if (typeof cfs != "undefined" && cfs) {
                    cfs.call(el);
                } else if (typeof window.ActiveXObject != "undefined") {
                    var wscript = new ActiveXObject("WScript.Shell");
                    if (wscript != null) {
                        wscript.SendKeys("{F11}");
                    }
                }
            }
        })
    },
    weather: function () {
        var that = this;
        $.ajax({
            type: "POST",
            dataType: "jsonp",
            url: 'http://api.map.baidu.com/location/ip?ak=m8U4gFO69r0E84nX828eDR1T2t5crH59&ip=',
            success: function (res) {
                var url = "http://restapi.amap.com/v3/weather/weatherInfo";
                var postData = {
                    key: "dfb9a576fbcb2c9a13a65ab736e47004",
                    city: res.content.address_detail.city,
                    extensions: "all"
                };
                $.ajax({
                    url: url,
                    type: 'post',
                    data: postData,
                    success: function (status, data) {
                        var weatherData = status.forecasts[0].casts;
                        $('#weather_now >u:nth-of-type(1)').html('星期' + that.week_transition(weatherData[0].week))
                        $('#weather_now >u:nth-of-type(2)').html(status.forecasts[0].city);
                        $('#weather_now >u:nth-of-type(3)').html(weatherData[0].dayweather);
                        $('#weather_now >u:nth-of-type(4)').html(weatherData[0].daytemp + '℃');
                        $('#weather_now >u:nth-of-type(5)').html(weatherData[0].daywind);
                    },
                    error: function (status) {
                    }
                })
            }
        });

    },
    dateNow: function () {
        var date = new Date();
        var seperator1 = "-";
        var seperator2 = ":";
        var month = date.getMonth() + 1;
        var strDate = date.getDate();
        var strHour = date.getHours();
        var strMinutes = date.getMinutes();
        var strSecond = date.getSeconds();
        if (month >= 1 && month <= 9) {
            month = "0" + month;
        }
        if (strDate >= 0 && strDate <= 9) {
            strDate = "0" + strDate;
        }
        if (strHour >= 0 && strHour <= 9) {
            strHour = "0" + strHour;
        }
        if (strMinutes >= 0 && strMinutes <= 9) {
            strMinutes = "0" + strMinutes;
        }
        if (strSecond >= 0 && strSecond <= 9) {
            strSecond = "0" + strSecond;
        }
        var currentDate = date.getFullYear() + seperator1 + month + seperator1 + strDate;
        var currentHour = strHour + seperator2 + strMinutes + seperator2 + strSecond;
        return [currentDate, currentHour];
    },
    getNowFormatDate: function () {
        var date = new Date();//今天
        var date2 = new Date();//明天
        var date3 = new Date();//八天前
        var date4 = new Date();//昨天
        var date5 = new Date();//前天
        var date6 = new Date();//七天前
        var date7 = new Date();//30天
        var date8 = new Date();//90天前
        var date9 = new Date();//60天前
        date3.setTime(date3.getTime() - 8 * 24 * 60 * 60 * 1000);
        date2.setTime(date2.getTime() + 24 * 60 * 60 * 1000);
        date4.setTime(date4.getTime() - 24 * 60 * 60 * 1000);
        date5.setTime(date5.getTime() - 2 * 24 * 60 * 60 * 1000);
        date6.setTime(date6.getTime() - 7 * 24 * 60 * 60 * 1000);
        date7.setTime(date7.getTime() - 30 * 24 * 60 * 60 * 1000);
        date8.setTime(date8.getTime() - 90 * 24 * 60 * 60 * 1000);
        date9.setTime(date9.getTime() - 60 * 24 * 60 * 60 * 1000);
        var seperator1 = "/";
        var month = date.getMonth() + 1;
        var strDate = date.getDate();
        var monthAnother = date2.getMonth() + 1;
        var month_3 = date3.getMonth() + 1;
        var dateAnother = date2.getDate();
        var date_3 = date3.getDate();
        var month_4 = date4.getMonth() + 1;
        var date_4 = date4.getDate();
        var month_5 = date5.getMonth() + 1;
        var date_5 = date5.getDate();
        var month_6 = date6.getMonth() + 1;
        var date_6 = date6.getDate();
        var month_7 = date7.getMonth() + 1;
        var date_7 = date7.getDate();
        var month_8 = date8.getMonth() + 1;
        var date_8 = date8.getDate();
        var month_9 = date9.getMonth() + 1;
        var date_9 = date9.getDate();
        if (month >= 1 && month <= 9) {
            month = "0" + month;
        }
        if (strDate >= 0 && strDate <= 9) {
            strDate = "0" + strDate;
        }
        if (month_3 >= 1 && month_3 <= 9) {
            month_3 = "0" + month_3;
        }
        if (date_3 >= 0 && date_3 <= 9) {
            date_3 = "0" + date_3;
        }
        if (month_4 >= 1 && month_4 <= 9) {
            month_4 = "0" + month_4;
        }
        if (date_4 >= 0 && date_4 <= 9) {
            date_4 = "0" + date_4;
        }
        if (month_5 >= 1 && month_5 <= 9) {
            month_5 = "0" + month_5;
        }
        if (date_5 >= 0 && date_5 <= 9) {
            date_5 = "0" + date_5;
        }
        if (month_6 >= 1 && month_6 <= 9) {
            month_6 = "0" + month_6;
        }
        if (date_6 >= 0 && date_6 <= 9) {
            date_6 = "0" + date_6;
        }
        if (month_7 >= 1 && month_7 <= 9) {
            month_7 = "0" + month_7;
        }
        if (date_7 >= 0 && date_7 <= 9) {
            date_7 = "0" + date_7;
        }
        if (month_8 >= 1 && month_8 <= 9) {
            month_8 = "0" + month_8;
        }
        if (date_8 >= 0 && date_8 <= 9) {
            date_8 = "0" + date_8;
        }
        if (date_9 >= 0 && date_9 <= 9) {
            date_9 = "0" + date_9;
        }
        monthAnother > 10 ? monthAnother : "0" + monthAnother;
        dateAnother > 10 ? dateAnother : "0" + dateAnother;
        var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate;
        var tommorwdate = date2.getFullYear() + seperator1 + monthAnother + seperator1 + dateAnother;
        var defaultdate = date3.getFullYear() + seperator1 + month_3 + seperator1 + date_3;
        var yesterdaydate = date4.getFullYear() + seperator1 + month_4 + seperator1 + date_4;
        var beforeYesterday = date5.getFullYear() + seperator1 + month_5 + seperator1 + date_5;
        var sevenDayAgo = date6.getFullYear() + seperator1 + month_6 + seperator1 + date_6;
        var thirtyDayAgo = date7.getFullYear() + seperator1 + month_7 + seperator1 + date_7;
        var ninetyDayAgo = date8.getFullYear() + seperator1 + month_8 + seperator1 + date_8;
        var sixtyDayAgo = date9.getFullYear() + seperator1 + month_9 + seperator1 + date_9;
        return [currentdate, tommorwdate, defaultdate, yesterdaydate, beforeYesterday, sevenDayAgo, thirtyDayAgo, ninetyDayAgo, sixtyDayAgo];
    },
    dateInterval: function (num1, num2, dayLength) {
        var date1 = new Date(num1.replace(/-/g, "/"));
        var date2 = new Date(num2.replace(/-/g, "/"));
        var days = date1.getTime() - date2.getTime();
        var time = parseInt(days / (1000 * 60 * 60 * 24));
        if (time < 7) {
            $("#day_methods").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#week_methods").attr("disabled", "disabled").css({'cursor': 'not-allowed'});
            $("#month_methods").attr("disabled", "disabled").css({'cursor': 'not-allowed'});
        } else if (time > 7 && time < 30) {
            $("#day_methods").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#month_methods").attr("disabled", "disabled").css({'cursor': 'not-allowed'});
            $("#week_methods").removeAttr('disabled').css({'cursor': 'pointer'});
        } else if (time > 30 && time < 60) {
            $("#day_methods").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#week_methods").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#month_methods").removeAttr('disabled').css({'cursor': 'pointer'});
        } else if ($('#day_methods').hasClass('active')) {
            if (time > 60) {
                layer.msg('日期超过两个月，无法按日进行显示', function () {

                });
                $("#day_methods").attr("disabled", "disabled").css({'cursor': 'not-allowed'}).removeClass('active');
                $("#week_methods").removeAttr('disabled').css({'cursor': 'pointer'}).addClass('active');
                $("#month_methods").removeAttr('disabled').css({'cursor': 'pointer'});
            }
        } else if (time > 60) {
            $("#day_methods").attr("disabled", "disabled").css({'cursor': 'not-allowed'}).removeClass('active');
        } else {
            $("#day_methods").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#week_methods").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#month_methods").removeAttr('disabled').css({'cursor': 'pointer'});
        }
    },
    dateInterval_Ano: function (num1, num2) {
        var date1 = new Date(num1.replace(/-/g, "/"));
        var date2 = new Date(num2.replace(/-/g, "/"));
        var days = date1.getTime() - date2.getTime();
        var time = parseInt(days / (1000 * 60 * 60 * 24));
        if (time < 7) {
            $("#day_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#week_methods_1").attr("disabled", "disabled").css({'cursor': 'not-allowed'});
            $("#month_methods_1").attr("disabled", "disabled").css({'cursor': 'not-allowed'});
        } else if (time > 7 && time < 30) {
            $("#day_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#month_methods_1").attr("disabled", "disabled").css({'cursor': 'not-allowed'});
            $("#week_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
        } else if (time > 30) {
            $("#day_methods_1").attr("disabled", "disabled").css({'cursor': 'not-allowed'}).removeClass('active');
            $("#week_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#month_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
        } else if ($('#day_methods').hasClass('active')) {
            if (time > 30) {
                layer.msg('日期超过30天，无法按日进行显示', function () {
                });
                $("#day_methods_1").attr("disabled", "disabled").css({'cursor': 'not-allowed'}).removeClass('active');
                $("#week_methods_1").removeAttr('disabled').css({'cursor': 'pointer'}).addClass('active');
                $("#month_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
            }
        } else {
            $("#day_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#week_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
            $("#month_methods_1").removeAttr('disabled').css({'cursor': 'pointer'});
        }
    },
    cookieSet: function () {
        (function ($, document, undefined) {

            var pluses = /\+/g;

            function raw(s) {
                return s;
            }

            function decoded(s) {
                return decodeURIComponent(s.replace(pluses, ' '));
            }

            var config = $.cookie = function (key, value, options) {
                // write
                if (value !== undefined) {
                    options = $.extend({}, config.defaults, options);

                    if (value === null) {
                        options.expires = -1;
                    }

                    if (typeof options.expires === 'number') {
                        var days = options.expires, t = options.expires = new Date();
                        t.setDate(t.getDate() + days);
                    }

                    value = config.json ? JSON.stringify(value) : String(value);

                    return (document.cookie = [
                        encodeURIComponent(key), '=', config.raw ? value : encodeURIComponent(value),
                        options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                        options.path ? '; path=' + options.path : '',
                        options.domain ? '; domain=' + options.domain : '',
                        options.secure ? '; secure' : ''
                    ].join(''));
                }

                // read
                var decode = config.raw ? raw : decoded;
                var cookies = document.cookie.split('; ');
                for (var i = 0, l = cookies.length; i < l; i++) {
                    var parts = cookies[i].split('=');
                    if (decode(parts.shift()) === key) {
                        var cookie = decode(parts.join('='));
                        return config.json ? JSON.parse(cookie) : cookie;
                    }
                }

                return null;
            };

            config.defaults = {};

            $.removeCookie = function (key, options) {
                if ($.cookie(key) !== null) {
                    $.cookie(key, null, options);
                    return true;
                }
                return false;
            };

        })(jQuery, document);
    },
    setLink: function () {
        var link = $('<link rel="shortcut icon " type="images/x-icon" href="../static/images/favicon.ico">');
        var head = $('head');
        head.append(link)
    },
    timeTransform: function (str) {
        var date = new Date(str);
        return date.getTime() / 1000;
    },
    periods: function (id) {
        var lis = $('.'+id+' li');
        lis.on('click', function (e) {
            e.preventDefault();
            $(this).find('button').addClass('active').parent('li').siblings('li').find('button').removeClass('active')
        })
    },
    periods_val: function (val) {
        switch (val) {
            case 1:
                return 1;
                break;
            case 2:
                return 2;
                break;
            case 3:
                return 3;
                break;
        }
    },
    keyDown: function () {
        $(document).keydown(function (event) {
            switch (event.keyCode) {
                case 27:
                    alert('您按下了回车');
                    return;
                case 13:
                    alert('您按下了空格');
                    return;

            }
        });
    },
    returnTop: function () {
        $(window).scroll(function () {
            var scrollTop = $(window).scrollTop();
            scrollTop > 300 ? $("#scrollUp").fadeIn(150).css("display", "block") : $("#scrollUp").fadeOut(150);
        });
        $('#scrollUp').click(function (e) {
            e.preventDefault();
            $('html,body').animate({scrollTop: 0});
        });
    },
    role_area_show: function (elem) {
        var province_id = $.trim(elem.attr('provinceid'));
        var city_id = $.trim(elem.attr('cityid'));
        var region_id = $.trim(elem.attr('regionid'));
        if (region_id != '') {
            return region_id
        } else if (province_id != '' && city_id == '') {
            return province_id
        } else if (province_id == '' && city_id != '') {
            return city_id
        } else if (province_id == '' && city_id == '' && region_id != '') {
            return region_id
        } else if (province_id == '' && city_id == '' && region_id == '') {
            return '';
        }
    },
    week_transition: function (val) {
        if (val == 1) {
            val = '一';
            return val
        } else if (val == 2) {
            val = '二';
            return val
        } else if (val == 3) {
            val = '三';
            return val
        } else if (val == 4) {
            val = '四';
            return val
        } else if (val == 5) {
            val = '五';
            return val
        } else if (val == 6) {
            val = '六';
            return val
        } else if (val == 7) {
            val = '天';
            return val
        }
    },
    clearSelect: function (element) {

    },
    menuSet: function () {//全屏和非全屏切换
        var menu_icon = $('.icon-caidan');
        layui.use('layer', function () {
            var layer = layui.layer;
        });
        $('#second_menu_box').stop().mouseenter(function () {
            if ($(this).width() < 60) {
                var content = '<a class="second-menu-list-child" href="/edit-message/">信息编辑</a><br><a class="second-menu-list-child" href="/root/">用户管理</a>'
                layer.tips(content, $(this), {
                    tips: [2, '#009688'],
                    time: 20000
                });
            }
        });
        $('nav.main-content-left .layui-nav-tree .layui-nav-item>a.first-menu-list').stop().hover(function () {
            if ($(this).width() < 60) {
                layer.tips($(this).text(), $(this), {
                    tips: [2, '#009688'],
                    time: 0
                });
            }
        })
    },
    currentTime: function () {
        var that = this;
        var date = new Date();
        this.year = date.getFullYear();
        this.month = date.getMonth() + 1;
        this.date = date.getDate();
        this.hour = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
        this.minute = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
        this.second = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
        var currentTime = "现在是:" + this.year + "-" + this.month + "-" + this.date + ' ' + this.hour + ":" + this.minute + ":" + this.second;
        currentTime = that.timeTransform(currentTime);
        return currentTime
    },
    isNumber: function (str) {
        var re = /^[0-9]+.?[0-9]*/;//判断字符串是否为数字//判断正整数/[1−9]+[0−9]∗]∗/;//判断字符串是否为数字//判断正整数/[1−9]+[0−9]∗]∗/
        if (!re.test(str)) {
            return true
        }
    },
    ajaxSetting: function () {
        layui.use('layer', function () {
            var layer = layui.layer;
            $.ajaxSetup({
                beforeSend: function () {
                    layer.load()
                },
                success: function () {
                    layer.closeAll('loading')
                },
                complete: function (Xhttp) {
                    layer.closeAll('loading');
                    if (Xhttp.responseJSON.status == 400 && Xhttp.responseJSON.msg == '货源已成单') {
                        $('#popup_one .layui-none').html('货源已被接')
                        $('#popup .layui-none').html('货源已被接')
                    } else if (Xhttp.responseJSON.status == 400 && Xhttp.responseJSON.msg == '货源已删除') {
                        $('#popup_one .layui-none').html('货源已删除')
                        $('#popup .layui-none').html('货源已删除')
                    } else if (Xhttp.responseJSON.status == 400 && Xhttp.responseJSON.msg == '货源不存在') {
                        $('#popup_one .layui-none').html('货源不存在')
                        $('#popup .layui-none').html('货源不存在')
                    } else if (Xhttp.responseJSON.status == 400 && Xhttp.responseJSON.msg == '货源已取消') {
                        $('#popup_one .layui-none').html('货源已取消')
                        $('#popup .layui-none').html('货源已取消')
                    }
                }
            })
        })
    },
    messageSet: function (elem, elemAno, elem_t) {
        elem.mouseenter(function () {
            elem_t.height('200');
            setTimeout(function () {
                elemAno.css({display: 'block'});
                elemAno.addClass('animated fadeInUp')
            }, 300)
        });
        elem_t.mouseleave(function () {
            elem_t.height('auto');
            setTimeout(function () {
                elemAno.css({display: 'none'});
                elemAno.removeClass('animated fadeInUp')
            }, 300)

        });
    },
    messageRequest: function () {
        var url = '/message/user/';
        var _this = this;
        var data = {
            'user_name': $('#user-info').attr('data-user-name'),
            'account': $('#user-info').attr('data-account'),
            'page': 1,
            'limit': 8//只显示最新的前八条
        };

        http.ajax.get_no_loading(true, false, url, data, http.ajax.CONTENT_TYPE_2, function (res) {
            var data = res.data;
            var unread = res.unread;
            var str = '';
            if (data) {
                $.each(data, function (val, index) {
                    str += '<li class="message-center-simple msg-item-' + val + '"><pre><i class="' + select(index.is_read) + '"></i></pre><p>' + index.title + '</p><span> ' + index.create_time + '</span></li>'
                })
                $(".message-count-show").html('当前有' + res.count + '条（已读：' + (res.count - unread) + ';未读:' + unread + '）消息！');
                $(".message-count-show").after(str);

                $('.message-center-simple').click(function () {
                    var route = '/message?msg-item=' + ($(this).index() - 1);//因为前面有一个子元素，所以这里要减一才能和前面的相对应。
                    _this.jump(route)
                })
            }
            $('.header .layui-badge').css({'opacity': '1'});
            if (unread == 0) {
                $('.message-center .layui-badge').css({'background': '#ccc'})
            }
            $('.message-center .layui-badge').html(res.count);

            function select(is_read) {
                if (is_read == 1) {
                    return 'iconfont icon-xinfeng2'
                } else if (is_read == 0) {
                    return 'iconfont icon-xiaoxi'
                }
            }
        })
    },
    secondMenuSet: function (second, second_child) {
        var second = second;
        second.click(function () {
            second.addClass('menu-active').parent('li').siblings().find('.second-menu-box').removeClass('menu-active');
            second.find(".icon-xia").toggleClass("icon-rotate");
            second_child.slideToggle("fast");
            if ($('.menu-line').height() == 376) {
                $('.menu-line').height(442)
            } else if ($('.menu-line').height() == 442) {
                $('.menu-line').height(376)
            }
        });
    },
    iconSet: function (setAbout, value, icon) {
        /*侧边栏是后端生成的，这里是根据中文显示用js控制样式，以后后台每增加一个页面，这里也要对应增加一个判断*/

        var value = value.replace(/(^\s*)|(\s*$)/g, "");
        var setAbout = setAbout;
        var children = '';
        //一级栏目标题
        var treeNode = ['运力统计', '推广统计', '地图工具', '用户统计', '交易统计', '权限管理', '价格统计', '区域商机'];
        //图标样式
        var arr = ['icon-techreport-', 'icon-xianlu', 'icon-ditu', 'icon-user', 'icon-caiwu', 'icon-suo', 'icon-renminbi', 'layui-icon-template-1'];
        switch (value) {
            case treeNode[0]:
                icon.addClass(arr[0]);
                setAbout.addClass('menu-transport');
                var children_0 = setAbout.next().children();
                $.each(children_0, function (val, index) {
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '认证车辆') {
                        $(this).find('a').addClass('vehicle-second-menu')
                    }
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '运力统计') {
                        $(this).find('a').addClass('transport-second-menu')
                    }

                });
                break;
            case treeNode[1]:
                icon.addClass(arr[1]);
                setAbout.addClass('menu-promote');
                var children_1 = setAbout.next().children();
                $.each(children_1, function (val, index) {
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '推广统计') {
                        $(this).find('a').addClass('promote-second-menu')
                    }

                })
                break;
            case treeNode[2]:
                icon.addClass(arr[2]);
                setAbout.addClass('menu-map');
                var children_2 = setAbout.next().children();
                $.each(children_2, function (val, index) {

                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '分布地图') {
                        $(this).find('a').addClass('distribute-second-menu')
                    }
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '货源热图') {
                        $(this).find('a').addClass('goodsMap-second-menu')
                    }
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '用户热图') {
                        $(this).find('a').addClass('userMap-second-menu')
                    }
                })
                break;
            case treeNode[3]:
                icon.addClass(arr[3]);
                setAbout.addClass('menu-users');
                var children_3 = setAbout.next().children();
                $.each(children_3, function (val, index) {
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '活跃留存') {
                        $(this).find('a').addClass('active-retain-second-menu')
                    }
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '用户统计') {
                        $(this).find('a').addClass('users-second-menu')
                    }

                })
                break;
            case treeNode[4]:
                icon.addClass(arr[4]);
                setAbout.addClass('menu-transaction');
                children_4 = setAbout.next().children();
                $.each(children_4, function (val, index) {
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '潜在货源') {
                        $(this).find('a').addClass('lurk-goods')
                    }
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '订单统计') {
                        $(this).find('a').addClass('order-second-menu')
                    }
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '货源统计') {
                        $(this).find('a').addClass('goods-second-menu')
                    }
                });
                break;
            case treeNode[5]:
                icon.addClass(arr[5]);
                setAbout.addClass('menu-power');
                var children_5 = setAbout.next().children();
                $.each(children_5, function (val, index) {
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '消息编辑') {
                        $(this).find('a').addClass('editMSG-second-menu')
                    }
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '用户管理') {
                        $(this).find('a').addClass('userManager-second-menu')
                    }
                });
                break;
            case treeNode[6]:
                icon.addClass(arr[6]);
                setAbout.addClass('menu-price');
                var children_6 = setAbout.next().children();
                $.each(children_6, function (val, index) {
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '价格统计') {
                        $(this).find('a').addClass('price-second-menu')
                    }
                })
                break;
            case treeNode[7]:
                icon.addClass(arr[7]);
                setAbout.addClass('menu-business_msg');
                var children_7 = setAbout.next().children();
                $.each(children_7, function (val, index) {
                    if ($(this).find('a').text().replace(/(^\s*)|(\s*$)/g, "") == '企业用车') {
                        $(this).find('a').addClass('business_msg-second-menu')
                    }
                })
                break;
        }
    },
    roleGet: function () {
        var url = '/role_change/role_change/';
        http.ajax.get_no_loading(true, false, url, {}, http.ajax.CONTENT_TYPE_2, function (res) {
            var str = '';
            var len = res.data.length;
            str += '<a class="current-role" href="javascript:;">' + res.data[0].role + '<span class="layui-nav-more"></span></a>';
            str += '<dl class="role-change-lists">';
            if (len) {
                $.each(res.data, function (index, val) {
                    str += '<dd><a  class="role-change-item" value="' + val.role_id + '">' + val.role + '</a></dd>';
                })
            }
            str += '</dl>';
            $('#role_change').html(str);
            /*切换身份写在这里是因为内容动态加载完成之后再执行这里的代码*/
            $('.current-role').mouseenter(function () {
                var $height = $('.role-change-lists').height();
                setTimeout(function () {
                    $('.role-change-lists').css({display: 'block'});
                    $('.role-change-lists').addClass('animated fadeInUp');
                    $('.current-role > .layui-nav-more').addClass('layui-nav-mored');
                    $('#role_change').height($height + 50)
                }, 250)
            });
            $('#role_change').mouseleave(function () {
                setTimeout(function () {
                    $('.role-change-lists').removeClass('animated fadeInUp');
                    $('.role-change-lists').css({display: 'none'});
                    $('#role_change').height(50);
                    $('.current-role > .layui-nav-more').removeClass('layui-nav-mored');
                }, 250)
            });
            $('.role-change-item').click(function (e) {
                e.preventDefault();
                var url = '/role_change/role_change/' + $(this).attr('value');
                var text = $(this).text();
                http.ajax.put_no_loading(true, false, url, {}, http.ajax.CONTENT_TYPE_2, function (res) {
                    if (res.status == 100000) {
                        layer.closeAll('loading');
                        layer.msg(res.msg, {
                            time: 700
                        });
                        setTimeout(function () {
                            window.location.href = '/admin';
                        }, 1300)
                    }
                })
            });
        })
    },
    jump: function (str) {
        window.location.href = str
    },
    getUrlParam: function (str) {
        var query = window.location.search.substring(1);
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            if (pair[0] == str) {
                return pair[1];
            }
        }
        return (false);
    },
    /*加载下拉框选项 json对象、初始化对象 如：["0":"请选泽","1":"测试数据1"]、document.getElementByid('id') */
    init_select: function (obj, oo) {
        obj.innerHTML = null;
        for (var i in oo) {
            obj.options.add(new Option(oo[i], i));
        }
    }
};

common.cookieSet();
common.menuSet();
common.messageRequest();
common.returnTop();
common.periods('periods');
common.weather();
common.init();
common.setLink();
common.ajaxSetting();
common.messageSet($('.message-center-count'), $('.message-center > ul'), $('.message-center'));
common.showData('#show_hide', '.header > .header-right .dropdown-menu');
common.sliderShow();
common.roleGet();
/*根据中文设置侧边栏样式*/
var second_menu = $('.second-menu-box');
$.each(second_menu, function (val, index) {
    common.secondMenuSet($(this), $('#second_menu_list_' + (val + 1)));
    common.iconSet($(this), $(this).text(), $(this).find('.icon-pic'))
});
/*防止天气信息未加载出来时样式丢失*/
setInterval(function () {
    $('.header-content-main').fadeIn('normal').css({'display': 'inline-block'});
    $('#date_now').html('');
    $('#hour_now').html('');
    $('#date_now').html(common.dateNow()[0]);
    $('#hour_now').html(common.dateNow()[1]);
}, 1000);
