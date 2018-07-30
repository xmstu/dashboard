var common = {
    display: function (elem) {
        elem.css({'display': 'none'})
    },
    showData: function (elem, elem2) {
        $(elem).mouseenter(function () {
            if ($(elem2).is(':hidden')) {
                $(elem2).slideDown(100);
                $(elem).html('&#xe619;')
            }
        });
        $(elem2).mouseleave(function () {
            $(elem2).slideUp(100);
            $(elem).html('&#xe61a;');
            return false
        })
    },
    init: function () {
        layui.use(['layer', 'form'], function () {
            var layer = layui.layer;
            var form = layui.form;
            var clearBtn = $('.clear-select');
            clearBtn.on('click', function () {
                $('#is_called').val("");
                $('#select').reset()
            })

        });
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
        var menuStatus = $.cookie('menuStatus')
        console.log(menuStatus)
        if (menuStatus == 'true') {
            $('.icon-caidan').click()
        }
    },
    fullScreen: function () {
        var full_screen = $('#fullScreen');
        full_screen.on('click', function () {
            if ($(this).find('strong').text() == '开启全屏展示') {
                $(this).find('strong').text('关闭全屏展示');
                var el = document.documentElement;
                var rfs = el.requestFullScreen || el.webkitRequestFullScreen || el.mozRequestFullScreen || el.msRequestFullScreen;
                if (typeof rfs != "undefined" && rfs) {
                    rfs.call(el);
                } else if (typeof window.ActiveXObject != "undefined") {
                    var wscript = new ActiveXObject("WScript.Shell");
                    if (wscript != null) {
                        wscript.SendKeys("{F11}");
                    }
                }
            } else {
                $(this).find('strong').text('开启全屏展示');
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
            url: 'http://api.map.baidu.com/location/ip?ak=ZVizfVIbcLc0qNhduvT3dSbqG8YV8YoP&ip=',
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
        date3.setTime(date3.getTime() - 8 * 24 * 60 * 60 * 1000);
        date2.setTime(date2.getTime() + 24 * 60 * 60 * 1000);
        date4.setTime(date4.getTime() - 24 * 60 * 60 * 1000);
        date5.setTime(date5.getTime() - 2 * 24 * 60 * 60 * 1000);
        date6.setTime(date6.getTime() - 7 * 24 * 60 * 60 * 1000);
        date7.setTime(date7.getTime() - 30 * 24 * 60 * 60 * 1000);
        date8.setTime(date8.getTime() - 90 * 24 * 60 * 60 * 1000);
        var seperator1 = "-";
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
        return [currentdate, tommorwdate, defaultdate, yesterdaydate, beforeYesterday, sevenDayAgo, thirtyDayAgo, ninetyDayAgo];
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
    periods: function () {
        var lis = $('.periods li');
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
    menuSet: function () {
        var menu_icon = $('.icon-caidan');
        menu_icon.on('click', function () {
            var $width = $('.main-content-left').width()
            if ($width >= 110) {
                $(this).css({'transform': 'rotateZ(-90deg)'});
                $.cookie('menuStatus', true, {expires: 7, path: '/'});
                $('.layui-nav-tree').css({'width': '100%', 'margin': 0});
                $('.nav-content').css({'display': 'none'});
                $('nav.main-content-left .layui-nav-tree .layui-nav-item>a').width('80%');
                $('.main-content-left').css({width: '38px', 'margin-left': 0, 'min-width': '38px'});
                $('.layui-nav-item>a>i:nth-child(1)').css({'margin': '0 7px'});
                $('.menu-line').css({'left': '19px'});
                $('.main-content-right').css({'margin-left': '38px'})
            } else {
                $.cookie('menuStatus', false, {expires: 7, 'path': '/'});
                $(this).css({'transform': 'rotateZ(0deg)'});
                $('.layui-nav-tree').css({'width': '94%', 'margin': '10px 4% 0 2%'});
                $('.nav-content').css({'display': 'block'});
                $('.main-content-left').css({width: '8%', 'margin-left': 0, 'min-width': '110px'});
                $('.layui-nav-item>a>i:nth-child(1)').css({'margin-left': '6%', 'margin-right': '10%'});
                $('nav.main-content-left .layui-nav-tree .layui-nav-item>a').width('100%');
                $('.menu-line').css({'left': '19px'});
                $('.main-content-right').css({'margin-left': '8%'})
            }
        })

        $('nav.main-content-left .layui-nav-tree .layui-nav-item>a').stop().hover(function () {
            if ($(this).width() < 60) {
                layer.tips($(this).text(), $(this), {
                    tips: [2, '#009688'],
                    time: 0
                });
            }
        }, function () {
            if ($(this).width() < 60) {
                layer.tips($(this).text(), $(this), {
                    tips: [2, '#009688'],
                    time: 100
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
                complete: function (Xhttp) {
                    layer.closeAll('loading')
                    if (Xhttp.responseJSON, status == 400 && Xhttp.responseJSON.msg == '货源已成单') {
                        $('#popup_one .layui-none').html('货源已被接')
                    }else if(Xhttp.responseJSON, status == 400 && Xhttp.responseJSON.msg == '货源已删除'){
                         $('#popup .layui-none').html('货源已删除')
                    }
                }
            })
        })
    }
};
setTimeout(function () {
    common.menuSet();
    common.returnTop();
    common.periods();
    common.cookieSet();
    common.weather();
    common.init();
    common.setLink();
    common.ajaxSetting();
    common.showData('#show_hide', '.header > .header-right .dropdown-menu');
}, 10);
setInterval(function () {
    $('.header-content-main').fadeIn('normal').css({'display': 'inline-block'});
    $('#date_now').html('');
    $('#hour_now').html('');
    $('#date_now').html(common.dateNow()[0]);
    $('#hour_now').html(common.dateNow()[1]);
}, 1000);
