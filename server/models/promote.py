# -*- coding: utf-8 -*-


class PromoteEffetList(object):
    @staticmethod
    def get_promote_effet_list(cursor, page, limit, params):

        # 查询字段
        fileds = """
            -- 名字
            shu_user_profiles.user_name,
            -- 手机号
            shu_users.mobile,
            -- 推荐人数
            -- 唤醒人数
            -- 发货数
            -- 发货人数
            -- 完成数
            -- 货源金额
            -- 完成金额
        """

        command = """
                SELECT
                    %s
                FROM
                    shu_users
                    LEFT JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
                    LEFT JOIN shu_user_stats ON shu_users.id = shu_user_stats.user_id 
                WHERE
                    shu_users.is_deleted = 0
                -- 	ANd shu_user_profiles.user_name = '猫大'
                -- 	AND shu_users.mobile = 15917907641
                    -- 所属地区
                    -- 推荐角色
                    -- 货源类型
                    -- 是否活跃
                    -- 贴车贴
                    -- AND shu_user_profiles.trust_member_type = 2 AND ad_expired_time > UNIX_TIMESTAMP()
                    -- AND shu_user_profiles.trust_member_type != 2
                    -- 注册日期
        """

        # TODO 语句需要优化

        promote_counts = cursor.query_one(command % "COUNT(*) AS promote_counts")['promote_counts']

        # 分页
        command += """ LIMIT %s, %s """ % ((page - 1) * limit, limit)

        promote_effet_detail = cursor.query(command)

        promote_effet_list = {
            'promote_effet_detail': promote_effet_detail if promote_effet_detail else [],
            'count': promote_counts if promote_counts else 0,
        }

        return promote_effet_list if promote_effet_list else None
