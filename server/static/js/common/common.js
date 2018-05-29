var common = {
    display: function (elem) {
        elem.css({'display': 'none'})
    },
    showData: function (elem, elem2) {
        $(elem).click(function () {
            if ($(elem2).is(':hidden')) {
                $(elem2).slideDown(100);
                $(elem).html('&#xe619;')
            } else {
                $(elem2).slideUp(100);
                $(elem).html('&#xe61a;');
                return false
            }
        })
    },
    init: function () {
        layui.use('layer', function () {
            var layer = layui.layer;
        });
        $('.main-content-right').addClass('animated fadeIn');
        var nav_menu = $('.icon-caidan');
        nav_menu.on('click', function (e) {
            if ($('.layui-nav-tree').width() == '176') {
                $('.layui-icon-right').animate({'opacity': 0});
                $('.nav-header >p span').css({'display': 'none'});
                $('.nav-header').animate({'width': '56px'});
                $('.layui-nav-tree').css({'margin-left': 0}).animate({'width': '50px'});
                $('.main-content-right').animate({'margin-left': '50px'});
                $(this).css({'transform': 'rotateZ(270deg)', 'transition': 'all 0.4s'});
                $('.layui-nav-item >a').animate({'width': '50px'});
                $('.nav-content span').fadeOut('10');
                $('.layui-nav-item > a > i:nth-child(1)').animate({'width': '50px'});
                return false
            } else if ($('.layui-nav-tree').width() == '50') {
                $('.layui-nav-tree').css({'margin-left': '12px'}).animate({'width': '176'});
                $('.layui-icon-right').animate({'opacity': 0});
                $('.main-content-right').animate({'margin-left': '200px'});
                setTimeout(function () {
                    $('.nav-content span').fadeIn('10');
                    $('.nav-header >p span').fadeIn('10');
                }, 300);
                $('.nav-header').animate({'width': '200px'});
                $(this).css({'transform': 'rotateZ(360deg)', 'transition': 'all 0.4s'});
                $('.layui-nav-item >a').animate({'width': '200px'});
                $('.layui-nav-item > a > i:nth-child(1)').animate({'width': '44px'});
                layer.closeAll('tips');
                return false

            } else
                console.log($('.layui-nav-tree').width());
        });
        $('.loginOut').click(function () {
            layer.confirm('您确定要退出登陆？', {
                btn: ['取消', '确定  '] //按钮
            }, function (index) {
                layer.close(index);
            }, function () {
                window.location.href = 'https://www.baidu.com'
            });
        })
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
        var this_ity;
        $.getScript('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js', function (_result) {
            this_ity = '广州';
            var myDate = new Date();
            var thisDate = myDate.getMonth() + 1;
            $.getScript('http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js', function (_result) {
                $.ajax({
                    type: "GET",
                    url: "http://wthrcdn.etouch.cn/weather_mini?city=" + this_ity,
                    dataType: "json",
                    success: function (res) {
                        $('#weather_now > u:nth-child(1)').html('城市：' + res.data.city);
                        $('#weather_now > u:nth-child(2)').html('日期:' + res.data.forecast[0].date);
                        $('#weather_now > u:nth-child(3)').html('实时温度：( ' + res.data.wendu + '℃ )&nbsp;&nbsp;&nbsp;热差:' + res.data.forecast[0].low + '~' + res.data.forecast[0].high)
                        $('#weather_now > u:nth-child(4)').html('天气: ' + res.data.forecast[0].type)
                    }
                });
            });
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
        date3.setTime(date3.getTime() - 8 * 24 * 60 * 60 * 1000);
        date2.setTime(date2.getTime() + 24 * 60 * 60 * 1000);
        date4.setTime(date4.getTime() - 24 * 60 * 60 * 1000);
        var seperator1 = "-";
        var month = date.getMonth() + 1;
        var strDate = date.getDate();
        var monthAnother = date2.getMonth() + 1;
        var month_3 = date3.getMonth() + 1;
        var dateAnother = date2.getDate();
        var date_3 = date3.getDate();
        var month_4 = date4.getMonth() + 1;
        var date_4 = date4.getDate();
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
        if (date_3 >= 0 && date_3 <= 9) {
            date_4 = "0" + date_4;
        }
        monthAnother > 10 ? monthAnother : "0" + monthAnother;
        dateAnother > 10 ? dateAnother : "0" + dateAnother;
        var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate;
        var tommorwdate = date2.getFullYear() + seperator1 + monthAnother + seperator1 + dateAnother;
        var defaultdate = date3.getFullYear() + seperator1 + month_3 + seperator1 + date_3;
        var yesterdaydate = date4.getFullYear() + seperator1 + month_4 + seperator1 + date_4;
        return [currentdate, tommorwdate, defaultdate, yesterdaydate];
    },
    dateInterval: function (num1, num2) {
        var date1 = new Date(num1.replace(/-/g, "/"));
        var date2 = new Date(num2.replace(/-/g, "/"));
        var days = date1.getTime() - date2.getTime();
        var time = parseInt(days / (1000 * 60 * 60 * 24));
        if (time < 7) {
            $("#week_methods").attr("disabled", "disabled");
            $("#month_methods").attr("disabled", "disabled");
        } else if (time > 7 && time < 31) {
            $("#month_methods").attr("disabled", "disabled");
        } else {
            $("#week_methods").removeAttr('disabled');
            $("#month_methods").removeAttr('disabled')
        }
        console.log(time)
    },
    setFavicon: function () {
        alert('test')
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
    setLink:function(){
        var link = $('<link rel="shortcut icon " type="images/x-icon" href="../static/images/favicon.ico">');
        var head=$('head')
        head.append(link)
    }
};
setTimeout(function () {
    common.cookieSet();
    common.weather();
    common.init();
    common.setLink();
    common.fullScreen();
    common.showData('#show_hide', '.header > .header-right .dropdown-menu');
}, 50);
setInterval(function () {
    $('.header-content-main').fadeIn('normal');
    $('#date_now').html('');
    $('#hour_now').html('');
    $('#date_now').html(common.dateNow()[0]);
    $('#hour_now').html(common.dateNow()[1]);

}, 1000);


