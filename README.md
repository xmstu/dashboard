*   [原型设计](#原型设计)
*   [功能配置](#功能配置)
    *   [登录](#登录)
    *   [修改密码](#修改密码)
    *   [用户统计](#用户统计)
    *   [推广统计](#推广统计)
    *   [货源统计](#货源统计)
*   [备注](#备注)
*   [相关配置](#相关配置)
    *   [zookeeper](#zookeeper)
        *   [可视化GUI-zkui](#可视化GUI-zkui)
    *   [redis](#redis)
        *   [可视化GUI-Redis Desktop Manager](#可视化GUI-Redis Desktop Manager)
    *   [mysql](#mysql)
        *   [测试](#测试)
    *   [mongodb](#mongodb)
    *   [可视化GUI-Robo 3T](#可视化GUI-Robo 3T)
    *   [github](#github)

# 原型设计
[修改密码](/doc/citymanager/0_修改密码.html)

[用户统计](/doc/citymanager/2_用户统计.html)

[推广统计](/doc/citymanager/3_推广统计.html)

[货源统计](/doc/citymanager/5_货源统计.html)

# 功能配置
## 登录
* 路由
`GET /login/`

* 返回页面
`/login/login.html`

* 登录接口
`POST /login/`

| 请求参数 | 变量名 |
| ------------ | ------------ |
| 用户名 | user_name |
| 密码 | password |

* 退出登录
`DELETE /login/`

## 修改密码
* 路由
```
用户修改密码功能放置用户类下，后期如需添加修改用户信息之类的功能，可在此路由下追加子路由
```

`GET /admin/`

* 返回页面
`/admin/home.html`

* 修改密码接口
`PUT /admin/opration/`

| 请求参数 | 变量名 |
| ------------ | ------------ |
| 用户id | user_id |
| 新密码 | password |
| 原密码 | password_old |

## 用户统计
* 路由
`GET /user/`

* 返回页面
```
开始、结束日期验证
结束日期至今天之前，今天及之后的日期添加disabled属性
选择日期天数小于7天，按周、按月按钮添加disabled属性
选择日期天数小于31天，按月按钮添加disabled属性
```
`/user/user-statistics.html`

* 用户变化趋势接口
`GET /user/statistic/`

| 请求参数 | 变量名 | 说明 |
| ------------ | ------------ | ------------ |
| 开始日期(时间戳) | start_time | 默认:8天前 |
| 结束日期(时间戳) | end_time | 默认:昨天 |
| 时间周期 | periods | 2:日，3:周，4:月，默认:2 |
| 用户类型 | user_type | 0:全部,1:新增用户,2:累计用户,默认:0 |
| 角色类型 | role_type | 0:全部,1:货主,2:司机,3:物流公司,默认:0 |
| 地区id | region_id | 0:全部,其他地区用行政代码(模板写入),默认:0 |
| 认证 | is_auth | 0:全部,1:认证,2:非认证,默认:0 |

* 用户列表接口
`GET /user/list/`

| 请求参数 | 变量名 | 说明 |
| ------------ | ------------ | ------------ |
| 用户名 | user_name | 默认:空 |
| 手机号 | mobile | 默认:空 |
| 推荐人手机 | reference_mobile | 默认:空 |
| 下载渠道 | download_channel | 默认:空 |
| 注册渠道 | from_channel | 默认:空 |
| 推荐注册 | is_referenced | 0:全部,1:有,2:无,默认:0 |
| 常驻地 | home_station_id | 0:全部,其他地区用行政代码,默认:0 |
| 注册角色 | role_type | 0:全部,1:货主,2:司机,3:物流公司,默认:0 |
| 认证角色 | role_auth | 0:全部,1:货主,2:司机,3:物流公司,默认:0 |
| 是否活跃 | is_actived | 0:全部,1:活跃,2:一般,3:即将沉睡,4:沉睡,默认:0 |
| 操作过 | is_used | 0:全部,1:发布货源,2:接单,3:完成订单,默认:0 |
| 贴车贴 | is_car_sticker | 0:全部,1:有,2:无,默认:0 |
| 页数 | index | 默认:1 |
| 条数 | count | 默认:10 |

## 推广统计
* 路由
`GET /promote/`

* 返回页面
```
开始、结束日期验证
结束日期至今天之前，今天及之后的日期添加disabled属性
选择日期天数小于7天，按周、按月按钮添加disabled属性
选择日期天数小于31天，按月按钮添加disabled属性
```
`/promote/promote-statistics.html`

* 推荐人质量统计接口
`GET /promote/quality/`

| 请求参数 | 变量名 | 说明 |
| ------------ | ------------ | ------------ |
| 开始日期(时间戳) | start_time | 默认:8天前 |
| 结束日期(时间戳) | end_time | 默认:昨天 |
| 时间周期 | periods | 2:日，3:周，4:月，默认:2 |
| 统计维度 | dimension | 1:拉新,2:用户行为,3:金额,默认:1 |
| 数据类型 | type | 1:新增,2:累计,默认:1 |
| 地区代码 | region_id | 0:全部,其他地区用行政代码(模板写入),默认:0 |

* 新增推广人员
`POST /promote/add/`

| 请求参数 | 变量名 |
| ------------ | ------------ |
| 手机号 | mobile |

* 推荐人员效果统计
`GET /promote/effect/`

| 请求参数 | 变量名 | 说明 |
| ------------ | ------------ | ------------ |
| 用户名 | user_name | 默认:空 |
| 手机号 | mobile | 默认:空 |
| 所属地区 | region_id | 0:全部,其他地区用行政代码(模板写入),默认:0 |
| 推荐角色 | role_type | 0:全部,1:货主,2:司机,3:物流公司,默认:0 |
| 货源类型 | goods_type | 0:全部,1:同城,2:跨城定价,3:跨城议价,4:零担,默认:0 |
| 活跃 | is_actived | 0:全部,1:活跃,2:一般,3:即将沉睡,4:沉睡,默认:0 |
| 贴车贴 | is_car_sticker | 0:全部,1:有,2:无,默认:0 |
| 开始日期(时间戳) | start_time | 默认:空 |
| 结束日期(时间戳) | end_time | 默认:空 |
| 页数 | index | 默认:1 |
| 条数 | count | 默认:10 |

## 货源统计
* 路由
`GET /goods/`

* 返回页面
```
开始、结束日期验证
结束日期至今天之前，今天及之后的日期添加disabled属性
选择日期天数小于7天，按周、按月按钮添加disabled属性
选择日期天数小于31天，按月按钮添加disabled属性
```
`/goods/goods-statistics.html`

* 货源漏斗接口
`GET /goods/resources/`

| 请求参数 | 变量名 | 说明 |
| ------------ | ------------ | ------------ |
| 开始日期(时间戳) | start_time | 默认:8天前 |
| 结束日期(时间戳) | end_time | 默认:昨天 |
| 时间周期 | periods | 2:日，3:周，4:月，默认:2 |
| 货源类型 | goods_type | 0:全部,1:同城,2:跨城,默认:0 |
| 数据类型 | type | 1:数量,2:金额,默认:1 |
| 地区代码 | region_id | 0:全部,其他地区用行政代码(模板写入),默认:0 |

* 发货/接单率趋势接口
`GET /goods/ratio/`

| 请求参数 | 变量名 | 说明 |
| ------------ | ------------ | ------------ |
| 开始日期(时间戳) | start_time | 默认:8天前 |
| 结束日期(时间戳) | end_time | 默认:昨天 |
| 时间周期 | periods | 2:日，3:周，4:月，默认:2 |
| 货源类型 | goods_type | 0:全部,1:同城,2:跨城,默认:0 |
| 地区代码 | region_id | 0:全部,其他地区用行政代码(模板写入),默认:0 |
| 发货率 | goods_ratio | 0:非选中,1:选中,默认:1 |
| 接单率 | order_ratio | 0:非选中,1:选中,默认:1 |

* 货源列表
`GET /goods/list/`

| 请求参数 | 变量名 | 说明 |
| ------------ | ------------ | ------------ |
| 货源id | goods_id | 默认:空 |
| 货主手机 | mobile | 默认:空 |
| 发出地 | from_region_id | 默认:空 |
| 目的地 | to_region_id | 默认:空 |
| 货源类型 | goods_type | 0:全部,1:同城,2:跨城定价,3:跨城议价,4:零担,默认:0 |
| 货源状态 | goods_status | 0:全部,2:待接单,3:已接单,4:已过期,-1:已取消,默认:0 |
| 是否通话 | is_called | 0:全部,1:是,2:否,3:大于10次,默认:0 |
| 车长要求 | vehicle_length | 0:全部,其他车长用车长id(模板写入),默认:0 |
| 车型要求 | vehicle_type | 0:全部,其他车型用车型id(模板写入),默认:0 |
| 所属网点 | node_id | 0:全部,其他网点用网点id(模板写入),默认:0 |
| 初次下单 | new_goods_type | 0:全部,1:同城,2:跨城定价,3:跨城议价,4:零担,默认:0 |
| 急需处理 | urgent_goods | 0:全部,1:5分钟内,2:5-10分钟,3:10分钟以上,默认:0 |
| 是否加价 | is_addition | 0:全部,1:是,2:否,默认:0 |
| 发布开始日期(时间戳) | create_start_time | 默认:空 |
| 发布结束日期(时间戳) | create_end_time | 默认:空 |
| 装货开始日期(时间戳) | load_start_time | 默认:空 |
| 装货结束日期(时间戳) | load_end_time | 默认:空 |

# 备注
```
一定要写代码注释
api接口文档要写
get,post,put,delete请求方式一般用于查、增、改、删
```

# 相关配置
## zookeeper

`
192.168.10.139:31081,192.168.10.139:31082,192.168.10.139:31083`

### 可视化GUI-zkui

https://github.com/echoma/zkui/wiki/Download

## redis

`192.168.10.172:6380`
### 可视化GUI-Redis Desktop Manager
https://redisdesktop.com/

## mysql

### 测试

huitouche2.mysql.rds.aliyuncs.com
port: 3306
user: sshtc_user
password: htctita337
database: bi

## mongodb

host: 192.168.10.139
port: 31001
## 可视化GUI-Robo 3T
https://robomongo.org/

## github

ssh://git@192.168.10.174:10022/sshtc/BI-dashboard.git