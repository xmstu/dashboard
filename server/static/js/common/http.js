var http = {};
http.ajax = {};
http.ajax.CONTENT_TYPE_1 = "application/x-www-form-urlencoded;charset=utf-8";
http.ajax.CONTENT_TYPE_2 = "application/json;charset=utf-8";
http.ajax.get = function(async, cache, url, data, contentType, callback) {
    $.ajax({
        async: async,
        cache: cache,
        type: "GET",
        url: url,
        data: data,
        contentType: contentType,
        dataType: "json",
        beforeSend: function() {
            layer.load(0, {
                shade: false,
                offset: ["55%", "50%"]
            })
        },
        complete: function(response) {
            if (response.status == 400) {
                layer.msg("请检查您输入的的数据");
                layer.closeAll("loading");
                return false
            }
            if (response.status == 500) {
                layer.msg("服务器内部错误！");
                layer.closeAll("loading");
                return false
            } else {
                layer.closeAll("loading")
            }
        },
        success: function(result) {
            if (typeof callback == "function") {
                callback(result)
            }
        }
    })
};
http.ajax.get_no_loading = function(async, cache, url, data, contentType, callback) {
    $.ajax({
        async: async,
        cache: cache,
        type: "GET",
        url: url,
        data: data,
        contentType: contentType,
        dataType: "json",
        complete: function(response) {},
        success: function(result) {
            if (typeof callback == "function") {
                callback(result);
                return
            }
        }
    })
};
http.ajax.post = function(async, cache, url, data, contentType, callback,cb) {
    $.ajax({
        async: async,
        cache: cache,
        type: "POST",
        url: url,
        data: data,
        contentType: contentType,
        dataType: "json",
        beforeSend: function() {
            layer.load(0, {
                shade: false,
                offset: ["55%", "50%"]
            })
        },
        complete: function(response) {
           if(typeof cb=='function'){
               cb(response);
               layer.closeAll('loading')
               return
           }
        },
        success: function(result) {
            if (typeof callback == "function") {
                callback(result);
                return false
            } else {
                if (result.msg != null && result != "") {
                    layer.msg("服务器异常" + result.msg)
                }
            }
        }
    })
};
http.ajax.post_no_loading = function(async, cache, url, data, contentType, callback,cb) {
    $.ajax({
        async: async,
        cache: cache,
        type: "POST",
        url: url,
        data: data,
        contentType: contentType,
        dataType: "json",
        success: function(result) {
            if (typeof callback == "function") {
                callback(result);
                return
            }
        },
        complete:function(response){
            if(typeof cb=='function'){
                cb(response)
                return
            }
        }
    })
};
http.ajax.patch = function(async, cache, url, data, contentType, callback) {
    $.ajax({
        async: async,
        cache: cache,
        type: "PATCH",
        url: url,
        data: data,
        contentType: contentType,
        dataType: "json",
        beforeSend: function() {
            layer.load(2, {
                offset: ["55%", "50%"]
            })
        },
        complete: function() {
            layer.closeAll("loading")
        },
        success: function(result) {
            if (typeof callback == "function") {
                if (result.success) {
                    callback(result);
                    return
                }
                if (result.msg != null && result != "") {
                    layer.msg(result.msg);
                    return
                }
                layer.msg("服务器异常")
            }
        }
    })
};
http.ajax.put = function(async, cache, url, data, contentType, callback) {
    $.ajax({
        async: async,
        cache: cache,
        type: "PUT",
        url: url,
        data: data,
        contentType: contentType,
        dataType: "json",
        beforeSend: function() {
            layer.load(0, {
                shade: false,
                offset: ["55%", "50%"]
            })
        },
        complete: function(response) {
            if (response.status == 400) {
                layer.msg("请检查您输入的的数据");
                layer.closeAll("loading");
                return false
            }
            if (response.status == 500) {
                layer.msg("服务器内部错误！");
                layer.closeAll("loading");
                return false
            } else {
                layer.closeAll("loading")
            }
        },
        success: function(result) {
            if (typeof callback == "function") {
                callback(result);
                return false
            }
        }
    })
};
http.ajax.put_no_loading = function(async, cache, url, data, contentType, callback,cb) {
    $.ajax({
        async: async,
        cache: cache,
        type: "PUT",
        url: url,
        data: data,
        contentType: contentType,
        dataType: "json",
        complete: function(response) {
            if(typeof cb=='function'){
                cb(response)
                return
            }
        },
        success: function(result) {
            if (typeof callback == "function") {
                callback(result);
                return
            }
        }
    })
};