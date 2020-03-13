from selenium.webdriver.common.by import By


class ElementSelector:
    """公共定位器"""
    confirm_btn_contais_text = '//div[contains(text(),"确定")]', '确定按钮'
    confirm_btn_equal_text = '//div[text()="确定"]', '确定按钮'
    succ_tip_loc = '//p[@class="el-message__content"]', '成功提示'

    """页面遮罩层"""
    loading_mask_loc = '//div[@class="el-loading-mask is-fullscreen"]'

    """页面所有元素"""
    all_loc = '//body', '页面所有元素'

    """登录页面"""
    username_input_loc = '//input[@id="normal_login_username"]', '用户名输入框'
    password_input_loc = '//input[@id="normal_login_password"]', '密码输入框'
    save_login_loc = '//input[@class="ant-radio-input"]', '记住账号'
    login_btn_loc = '//span[contains(text(),"登 录")]', '登录按钮'
    uni_teach_login_btn_loc = '//span[contains(text(),"登录")]/parent::button', '教学版登录按钮'

    class_manage_text_loc = '//div[@class="model-tips-word"]', '班级管理文本'

    wrong_login_tip_loc = '//div[@class="el-message el-message--error is-center"]/p', '登录错误提示'  # 待定
    wrong_username_tip_loc = \
        '//form[@class="el-form login-form el-form--label-left"]/div[1]/div/div[2]', '用户名错误提示'  # 待定
    wrong_password_tip_loc = \
        '//form[@class="el-form login-form el-form--label-left"]/div[2]/div/div[3]', '密码错误提示'  # 待定

    """导航栏"""
    bar_index_loc = '//span[contains(text(), "首页")]', '首页'
    bar_course_loc = '//span[text()="课程"]', '课程'
    bar_homework_loc = '//span[text()="作业"]', '作业'
    bar_creative_space_loc = '//span[contains(text(),"创作空间")]', '创作空间'
    bar_study_analysis_loc = '//span[contains(text(),"学情分析")]', '学情分析'
    bar_teach_center_loc = '//span[contains(text(),"教学中心")]', '教学中心'
    bar_test_field_loc = '//span[contains(text(),"进入试炼场")]', '进入试炼场'

    standard_course_btn_loc = '//span[contains(text(),"标准")]', '标准授课按钮'
    checkpoint_course_loc = '//span[contains(text(),"主题")]', '主题授课按钮'
    test_field_btn_loc = '//span[contains(text(),"试炼场")]', '试炼场按钮'
    creative_space_loc = '//span[contains(text(),"创作空间")]', '创作空间'
    ai_experience_loc = '//div[@class="picture-ai"]', 'AI体验'
    teach_management_btn_loc = '//span[contains(text(),"教学")]', '教学管理按钮'

    uni_teach_start_course_btn_loc = '//span[contains(text(),"上课")]', '高校版上课按钮'

    """首页文本"""
    index_teacher_name_loc = '//div[@class="main-right-name"]', '教师端首页用户名文本'
    index_student_name_loc = '//div[@class="person-nickname"]', '学生端首页用户名文本'

    index_added_course_loc = '//div[@class="boardCount_container__1vl-U"]/ul[1]/li[1]/div', '开设课程'
    index_added_homework_loc = '', '发布作业总数'  # 待定
    index_help_loc = '//span[contains(text(),"使用帮助")]', '使用帮助'

    """意见反馈"""
    fill_feedback_btn_loc = '', '填写反馈'  # 待定

    feedback_btn_loc = '//div[contains(text(),"意见")]', '意见反馈'
    content_textarea_loc = '//textarea[@class="el-textarea__inner"]', '内容输入框'
    feedback_upload_pic_loc = '//div[@class="el-upload el-upload--picture-card"]', '上传图片按钮'
    submit_btn_loc = '//span[contains(text(),"提交")]', '提交按钮'

    """头像下拉选项"""
    index_portrait_loc = '//span[@class="ant-dropdown-trigger ant-badge"]', '头像'
    index_portrait_name_loc = '//span[text()="Data中的名称"]', '头像下拉框用户名称'
    index_portrait_msg_loc = '//span[contains(text(),"消息")]', '消息'
    index_portrait_setup_loc = '//span[contains(text(),"设置")]', '设置'
    index_portrait_knowledge_base_loc = '//span[contains(text(),"知识库")]', '知识库'
    index_portrait_help_loc = '//span[contains(text(),"帮助")]', '帮助'
    index_portrait_logout_loc = '//span[contains(text(),"退出登录")]', '退出登录'
    index_portrait_switch_school_loc = '//span[contains(text(),"切换学校")]', '切换学校'
    index_portrait_switch_school_choose_loc = '', '切换学校下拉框'  # 待定

    index_portrait_msg_list_first_loc = '', '消息列表第一个'  # 待定
    index_portrait_msg_list_choose_loc = '', '消息列表勾选框'  # 待定
    index_portrait_msg_list_mark_read_loc = '', '消息列表标为已读'  # 待定
    index_portrait_msg_list_delete_loc = '', '消息列表删除'  # 待定
    index_portrait_msg_list_all_loc = '', '消息列表全部'  # 待定
    index_portrait_msg_list_read_loc = '', '消息列表已读'  # 待定
    index_portrait_msg_list_unread_loc = '', '消息列表未读'  # 待定
    index_portrait_msg_detail_return_loc = '', '消息详情返回'  # 待定

    """首页添加课件和作业"""
    index_keep_teach_loc = '//span[contains(text(),"继续上课")]', '继续上课'
    index_add_homework_btn_loc = '//span[contains(text(),"继续上课")]/ancestor::ul/li[2]/div', '首页发布作业按钮'
    index_course_resource_loc = '//span[contains(text(),"课程资源")]', '课程资源'

    """首页最近作业"""
    index_homework_more_loc = '//div[contains(text(),"最近作业")]/parent::div/div[2]/a/span', '最近作业更多'
    index_homework_status_loc = '//div[@class="ant-table-content"]/descendant::td[3]', '最近作业列表作业状态'
    teacher_index_homework_name_loc = '//div[@class="ant-table-content"]/descendant::td[1]', '教师首页最近作业列表作业名称'
    student_index_homework_name_loc = '', '学生首页最近作业列表作业名称'  # 待定
    student_index_homework_go_finish_loc = '', '学生最近作业去完成'  # 待定
    index_homework_look_loc = '//div[@class="ant-table-content"]/descendant::td[6]/span', '最近作业查看'

    # index_course_name_loc = \
    #     '//div[@class="home-stu-course-container clearfix"]/div[1]/div/div/div[1]', \
    #     '学生端首页最新课程课程名称'  # .home-stu-course-container.clearfix>div:nth-of-type(1)>div>div>div

    """首页我的课程"""
    index_course_more_loc = '//div[contains(text(),"我的课程")]/parent::div/div[2]/a/span', '我的课程更多'
    index_course_loc = '//div[@class="home_course-main__2BWf1"]/div[1]/div[1]', '我的课程第一个课程卡片'

    """学生动态"""
    index_dynamic_more_loc = '//div[contains(text(),"学生动态")]/parent::div/div[2]/a/span', '动态更多'
    index_dynamic_work_loc = '', '动态作品'  # 待定

    """作品推荐"""
    index_work_recommend_more_loc = '//div[contains(text(),"作品推荐")]/parent::div/div[2]/a/span', '作品推荐更多'
    index_wowk_recommend_loc = '', '作品推荐卡片'  # 待定

    """上课引导"""
    index_hidden_course_guide_loc = '//span[contains(text(),"上课引导")]/parent::div/span[2]/span', '上课引导隐藏'
    index_course_guide_add_class_loc = '//span[contains(text(),"上课引导")]/parent::div/parent::div/descendant::a[1]',\
                                       '上课引导创建班级'
    index_course_guide_add_course_loc = '//span[contains(text(),"上课引导")]/parent::div/parent::div/descendant::a[2]',\
                                        '上课引导发布课程'
    index_course_guide_add_homework_loc = '//span[contains(text(),"上课引导")]/parent::div/parent::div/descendant::a[3]',\
                                          '上课引导发布作业'
    index_course_guide_start_course_loc = '//span[contains(text(),"上课引导")]/parent::div/parent::div/descendant::a[4]',\
                                          '上课引导开始上课'

    """首页AI体验"""
    index_AI_experience_loc = '//div[@class="home_article__31HOp"]', '进入AI体验'

    """日期筛选、搜索功能"""
    ctsk_btn_loc = '//div[contains(text(),"标准授课")]', '传统授课按钮'
    student_homework_date_search_input_loc = '//div[@class="homework-filter clearfix"]' \
                                             '/div[3]/div/div/input[1]', '学生作业日期筛选输入框'
    teacher_homework_date_search_input_loc = '//div[@class="homework-filter clearfix"]' \
                                             '/div[2]/div/div/input[1]', '教师作业日期筛选输入框'
    student_course_date_search_input_loc = '//div[@class="course-filter clearfix"]' \
                                           '/div[3]/div/div/input[1]', '学生课件日期筛选输入框'
    teacher_course_date_search_input_loc = '//div[@class="course-filter clearfix"]' \
                                           '/div[2]/div/div/input[1]', '教师课件日期筛选输入框'
    today_loc = '//td[@class="available today"]', '日期筛选今天'
    today_end_loc = '//td[@class="available today in-range start-date end-date"]', '日期筛选今天结束'
    tomorrow_loc = '//td[@class="available today"]/following-sibling::td', '日期筛选明天'
    next_week_loc = '//td[@class="available today"]/parent::tr/following-sibling::tr[1]/td[1]', '下周第一天'
    tomorrow_end_loc = \
        '//td[@class="available today in-range start-date end-date"]/following-sibling::td', '日期筛选明天结束'
    next_week_end_loc = '//td[@class="available today in-range start-date end-date"]/parent::tr' \
                        '/following-sibling::tr[1]/td[1]', '下周第一天结束'
    date_clear_btn_loc = '//span[@class="el-range-separator"]/parent::div/i[2]', '日期筛选清除按钮'
    date_search_btn_loc = '//span[@class="el-range-separator"]/parent::div/i[2]', '日期筛选按钮'
    search_input_loc = '//div[@class="input-wrapper"]/div/input', '搜索输入框'
    search_btn_loc = '//div[@class="input-wrapper"]/div/span', '搜索放大镜按钮'
    course_list_loc = '//div[@class="course-container-gird"]/ul/li/div/div/div[2]/div[1]/div', '课件名称列表'
    homework_list_loc = \
        '//div[@class="homework-container-gird"]/ul/li/div/div/div[1]/div[1]/div[1]/div[1]', '作业名称列表'
    first_homework_loc = \
        '//div[@class="traditional_teach-container-gird"]/ul/li[1]/div/div/div/div[1]/div[1]/div', \
        '作业列表中第一个作业'

    """选择知识点"""
    s1_loc = '//div[@class="el-cascader-panel"]/div[1]/div[1]/ul/li', 'S系列列表所有系列'
    # .el-cascader-panel>div:nth-of-type(1)>div:nth-of-type(1)>ul>li:nth-of-type(2)
    level_two_loc = '//div[@class="el-cascader-panel"]/div[2]/div[1]/ul/li', '级菜单所有知识点'
    level_three_loc = '//div[@class="el-cascader-panel"]/div[3]/div[1]/ul/li', '三级菜单所有知识点'

    """课件列表"""
    course_list_add_course_loc = '//span[text()="发布课程"]', '发布课程'
    course_list_choose_class_loc = '//div[@class="course_nav-header__KaIKl"]/div[1]/div[1]/div', '班级筛选'
    course_list_choose_course_loc = '//div[@class="course_nav-header__KaIKl"]/div[1]/div[2]/div', '课程筛选'
    course_list_search_all_loc = '//span[contains(text(),"全部")]', '全部'
    course_list_search_ongoing_loc = '//span[contains(text(),"全部")]/parent::label/following-sibling::label[1]', '进行中'
    course_list_search_ended_loc = '//span[contains(text(),"全部")]/parent::label/following-sibling::label[2]', '已结束'
    course_list_card_mode_loc = '//div[@class="course_nav-header__KaIKl"]/div[2]/div[1]/div/label[1]', '卡片形式'
    course_list_list_mode_loc = '//div[@class="course_nav-header__KaIKl"]/div[2]/div[1]/div/label[2]', '列表形式'
    course_list_card_mode_first_course_loc = '//div[@class="course_card-main__OJhEN"]/div[1]/div[1]/div[1]', '课程卡片第一个'
    course_list_list_mode_first_course_loc = '//div[@class="ant-table-content"]/descendant::span[2]', '课程列表第一个'  # 待定
    course_list_card_mode_teacher_name_loc = '', '课程卡片发布教师'  # 待定
    course_list_card_mode_all_course_loc = '//div[@class="course_card-main__OJhEN"]/div', '所有课程卡片'
    course_list_list_mode_all_course_loc = '//div[@class="ant-table-content"]', '列表所有课程'  # 待定
    course_list_operation_loc = '//div[@class="course_card-main__OJhEN"]/div[1]/div[4]/span[2]', '课程列表操作'
    course_list_operation_end_course_loc = '//div[@class="ant-dropdown ant-dropdown-placement-bottomCenter "]' \
                                           '/ul/li[1]', '课程列表操作结束课程'
    course_list_operation_edit_course_loc = '//div[@class="ant-dropdown ant-dropdown-placement-bottomCenter "]' \
                                            '/ul/li[2]', '课程列表操作编辑'
    course_list_operation_delete_course_loc = '//div[@class="ant-dropdown ant-dropdown-placement-bottomCenter "]' \
                                              '/ul/li[4]', '课程列表操作删除'

    """添加课程"""
    add_course_choose_course_loc = '//form[@class="ant-form ant-form-horizontal ant-form-small ' \
                                   'courseCompile_form-items__3KJIT"]/div[1]/div[2]', '选择课程'
    add_course_choose_class_loc = '//div[@class="ant-select courseCompile_class-select__1CdH2 ant-select-lg ' \
                                  'ant-select-multiple ant-select-show-search"]', '发布班级'
    add_course_choose_first_course_loc = '//div[contains(text(),"S1")]', '选择下拉框第一个课程'  # 待定，后期加到操作代码
    add_course_choose_first_class_loc = '//div[contains(text(),"课程班153")]', '选择下拉框第一个班级'  # 待定，后期加到操作代码
    add_course_delete_first_class_loc = '//span[@class="anticon anticon-close"]', '删除列表第一个班级'
    add_course_preview_course_loc = '//span[contains(text(),"预览")]', '预览课程'
    add_course_course_plan_switch_loc = '//button[@class="ant-switch"]', '计划授课开关'
    add_course_course_plan_choose_date_loc = '//div[@class="ant-row"]/div[1]/label/span[1]/input', '计划授课日期选择'
    add_course_publish_course_loc = '//span[contains(text(),"发 布")]', '发布课程按钮'
    add_course_cancel_course_loc = '//span[contains(text(),"取 消")]', '发布课程取消按钮'
    add_course_publish_course_success_tip_loc = '', '发布课程成功文本'  # 待定
    add_course_publish_course_window_confirm_loc = '', '发布课程弹窗确定'  # 待定
    add_course_publish_course_fail_tip_loc = '', '发布课程失败文本'  # 待定

    first_course_in_list_loc = \
        '//div[@class="course-container-gird"]/ul/li[1]/div/div/div[2]/div[1]/div', '课件列表第一个课件'

    choice_teaching_package_loc = '//span[text()="叮当资源"]/parent::label/span[1]', '选择叮当资源'
    selKnow_loc = '//div[@class="cascader-bgc mar-cls"]/div/div/span/span', '选择知识点'
    choice_course_btn_loc = \
        '//div[@class="item-card-center"]/ul/li[1]/div/div/div[2]/div/div[2]/div[3]/label/span[1]/span', \
        '选择按钮'
    choice_cla = '//div[text()="发布班级"]', '发布班级按钮'
    choice_all = '//span[text()="全选"]', '全选按钮'
    choice_class_btn_loc = '//div[@class="class-select-container-gird"]/ul/li[1]', '选择第1个班级'
    del_class_btn_loc = '//div[@class="item-tags"]/div/span/i', '删除已选班级按钮'
    add_publish_btn = '//div[@class="set-course-bgc"]/div/div[2]/label/span/span', '添加并发布按钮'
    add_btn_loc = '//div[@class="add-course-submit-gird"]/button', '添加按钮'
    go_add_homework_btn_loc = '//span[contains(text(),"发布作业")]', '去发布作业按钮'
    go_on_btn_loc = '//span[contains(text(),"继续")]', '弹窗继续添加按钮'
    standard_course_crumb_loc = '//div[@class="el-breadcrumb"]/span[1]/span[1]', '标准授课面包屑'
    course_name_loc = '//div[@class="course-container-gird"]/ul/li[1]/div/div/div[2]/div/div', '课程名称'
    wrapper_elem = '//div[@class="el-scrollbar__wrap"]'

    """编辑课程"""
    course_edit_course_plan_switch_loc = '', '编辑课程计划授课开关'  # 待定
    course_edit_course_plan_choose_date_loc = '', '编辑课程计划授课选择日期'  # 待定
    course_edit_confirm_loc = '', '编辑课程确定'  # 待定
    course_edit_cancel_loc = '', '编辑课程取消'  # 待定

    """查看课程详情"""
    lookNumber_loc = '//div[@class="courseware-card-looknumber"]', '课程详情页面查看人数'
    crumbs_loc = '//div[@class="courseware-title"]/font[1]', '面包屑'

    course_detail_course_title_loc = '//div[@class="courseware-card-title-word elli_1 fl"]', '课程详情页面课程名称'  # 待定
    course_detail_directory_loc = '', '目录'  # 待定
    course_detail_ppt_loc = '', '课件tab'  # 待定
    course_detail_video_loc = '', '视频tab'  # 待定
    course_detail_notes_loc = '', '讲义tab'  # 待定
    course_detail_teach_plan_loc = '', '教案tab'  # 待定
    course_detail_practice_loc = '', '练习tab'  # 待定
    course_detail_ppt_next_btn_loc = '//span[@class="cui-toolbar-buttondock aligncenter"]/a[3]', '课件PPT下一页按钮'  # 待定
    course_detail_ppt_pages_num_loc = '//span[@class="cui-toolbar-buttondock aligncenter"]/a[2]', '课件页数'  # 待定
    course_detail_practice_list_problem_loc = '', '练习题目'  # 待定
    course_detail_practice_list_student_name_loc = '', '练习列表学生名字'  # 待定
    course_detail_practice_list_refresh_loc = '', '练习列表刷新'  # 待定

    course_detail_choose_chap_loc = '//span[contains(text(),"目录")]/parent::div/following-sibling::div/div', '选择章节'
    course_detail_choose_section_loc = '', '选择小节'  # 待定
    course_detail_full_screen_course_loc = '//span[contains(text(),"全屏")]', '全屏授课'
    course_detail_start_study_course_loc = '', '开始学习'  # 待定
    course_detail_full_screen_return_course_loc = '//span[contains(text(),"返回")]', '全屏模式返回课程'

    course_detail_start_course_edit_btn_loc = '//span[contains(text(),"返回")]/parent::button/following::button',\
                                              '精简试炼场弹出开关'
    course_detail_start_course_edit_cross_btn_loc = '', '精简试炼场横向模式'  # 待定
    course_detail_start_course_putback_btn_loc = '//span[contains(text(),"收起")]', '精简试炼场收起开关'  # 待定
    course_detail_start_course_edit_cursor_loc = '//div[@class=" ace_editor ace-cobalt ace_dark"]/textarea', \
                                                 '精简试炼场游标'  # 待定
    course_detail_start_course_text_output_btn_loc = '//div[contains(text()#"文本")]', '文本输出区按钮'  # 待定
    course_detail_start_course_text_output_area_loc = '//div[@class="simple-output-item"]', '文本输出'  # 待定
    course_detail_start_course_pic_output_btn_loc = '//div[contains(text(),"图形")]', '图形输出区按钮'  # 待定
    course_detail_start_course_pic_output_area_loc = '//div[@class="gird"]/img', '图形输出'  # 待定
    course_detail_start_course_course_run_code_btn_loc = '//span[contains(text(),"运行")]', '运行代码按钮'  # 待定
    course_detail_start_course_iframe_loc = '//div[@class="courseware-content-ware"]/iframe', '第一层iframe'  # 待定

    """作业列表"""
    homework_list_add_homework_btn_loc = '//div[@class="homework-bg-gird"]/div[1]/div[3]/button', '发布作业按钮'  # 待定
    homework_list_homework_name = \
        '//div[@class="homework-container-gird"]/ul/li[1]/div/div/div/div[1]/div[1]/div', '作业列表作业名称'  # 待定
    homework_list_wrong_statistic_loc = '//span[contains(text(),"错题统计")]', '错题统计'
    homework_list_student_list_username_loc = '', '学生列表学生学号'  # 待定
    homework_list_student_list_name_loc = '', '学生列表学生名字'  # 待定
    homework_list_student_list_completion_loc = '', '学生列表学生完成率'  # 待定
    homework_list_student_list_correct_loc = '', '学生列表正确率'  # 待定
    homework_list_student_list_score_loc = '', '学生得分'  # 待定
    homework_list_student_list_level_loc = '', '学生列表作业等级'  # 待定
    homework_list_student_list_look_loc = '', '学生列表查看按钮'  # 待定
    homework_list_student_list_resubmit_loc = '', '学生列表重交按钮'  # 待定
    homework_list_class_select_loc = '', '班级下拉框'  # 待定
    homework_list_search_all_loc = '', '筛选全部'  # 待定
    homework_list_search_ongoing_loc = '', '筛选进行中'  # 待定
    homework_list_search_ended_loc = '', '筛选已结束'  # 待定
    homework_list_date_search_loc = '', '日期筛选'  # 待定
    homework_list_search_input_loc = '', '搜索输入框'  # 待定
    homework_list_search_btn_loc = '', '搜索按钮'  # 待定
    homework_list_homework_card_loc = '', '作业卡片'  # 待定
    homework_list_operation_loc = '', '作业操作'  # 待定
    homework_list_operation_edit_loc = '', '重新编辑'  # 待定
    homework_list_operation_edit_keep_choose_problem_loc = '', '重新编辑继续选取题目'  # 待定
    homework_list_operation_edit_confirm_edit_loc = '', '重新编辑确认修改'  # 待定
    homework_list_operation_replacement_loc = '', '补发作业'  # 待定
    homework_list_operation_delete_loc = '', '删除'  # 待定
    homework_list_problem_analysis_loc = '', '题目分析'  # 待定
    homework_list_problem_analysis_go_explain_loc = '', '去讲解'  # 待定
    homework_list_problem_analysis_go_explain_student_choose_loc = '', '去讲解学生下拉框'  # 待定
    homework_list_problem_analysis_go_explain_student_choose_first_loc = '', '学生下拉框第一个'  # 待定
    homework_list_student_detail_go_answer_loc = '', '去作答'  # 待定
    homework_list_student_detail_look_loc = '', '查看'  # 待定
    homework_list_student_detail_student_name_loc = '', '学生姓名'  # 待定
    homework_list_student_detail_completion_loc = '', '完成率'  # 待定
    homework_list_student_detail_correct_loc = '', '正确率'  # 待定
    homework_list_student_detail_score_loc = '', '得分'  # 待定
    homework_list_student_detail_level_loc = '', '等级'  # 待定

    """发布作业"""
    add_homework_homework_name_input_loc = '//div[@class="container-box-item-0"]/div/input', '作业名称输入框'  # 待定
    add_homework_choice_point_id_loc = '//div[@class="container-box-item-1"]/button', '选取知识点按钮'  # 待定
    add_homework_choice_point_id_sel_know_loc = '//div[@class="dialog-inner-input clearfix"]/div[2]/div/div/span/span', \
                                                '选择知识点'  # 待定
    add_homework_choice_problem_loc = '//span[contains(text(),"选择")]', '选择题'  # 待定
    add_homework_operation_problem_loc = '//span[contains(text(),"操作")]', '操作题'  # 待定
    add_homework_choice_all_problem_loc = '//div[@class="check-box"]/label/span[1]/span', '全选按钮'  # 待定
    add_homework_choice_first_problem_loc = '//div[@class="el-row"]/div[1]/label/span[1]/span', '选题列表第一道题'  # 待定

    add_homework_confirm_problem_loc = '//div[@class="el-dialog__footer"]/span/button', '确定按钮'  # 待定
    add_homework_show_answer_loc = '//div[contains(text(),"参考答案")]/parent::div/div[2]/div/input', '显示参考答案下拉框'  # 待定
    add_homework_show_diff_loc = '', '显示难度'  # 待定
    add_homework_not_show_diff_loc = '', '不显示难度'  # 待定
    add_homework_end_time_input_loc = '//div[contains(text(),"截止时间")]/parent::div/div[2]/input', '截止时间输入'  # 待定
    add_homework_public_answer_loc = '//span[text()="立即公布"]/parent::li', '公布答案'  # 待定
    add_homework_timing_btn_loc = '//div[contains(text(),"定时发布")]/parent::div/div[2]/span', '定时发布按钮'  # 待定
    add_homework_timing_input_loc = '//div[contains(text(),"定时发布")]/parent::div/parent::div/div[4]/div[2]/input', \
                                    '定时时间输入'  # 待定
    add_homework_choose_homework_class_loc = '', '发布班级'  # 待定(如果和发布课程相同则去掉)
    add_homework_choose_first_class_loc = '', '发布班级选择第一个班级'  # 待定(如果和发布课程相同则去掉)
    add_homework_delete_first_class_loc = '', '发布班级删除第一个班级'  # 待定(如果和发布课程相同则去掉)
    add_homework_public_homework_btn_loc = '//span[text()="发布"]/parent::button', '立即发布'  # 待定
    add_homework_cancel_homework_loc = '', '发布作业取消按钮'  # 待定(如果和发布课程相同则去掉)
    add_homework_success_tip_loc = '', '发布作业成功提示'  # 待定(如果和发布课程相同则去掉)
    add_homework_publish_fail_tip_loc = '', '发布作业失败提示'  # 待定(如果和发布课程相同则去掉)
    add_homework_success_confirm_loc = '', '发布作业成功确定'  # 待定(如果和发布课程相同则去掉)

    """作业详情"""
    homework_detail_problem_list_loc = '//div[@class="data-back-single-title fl"]'  # , '题目列表'  # 待定
    homework_detail_answer_btn_loc = '//div[@class="el-tabs__nav is-top"]/div[2]', '参考答案按钮'  # 待定
    homework_detail_code_view_loc = '//div[@id="ueditor"]/textarea', '作答IDE光标'  # 待定
    homework_detail_run_code_loc = '', '运行'  # 待定
    homework_detail_save_run_btn_loc = '//div[contains(text(),"保存并评测")]', '保存并运行按钮'  # 待定
    homework_detail_choice_pass_result_text_loc = '', '选择题回答正确'  # 待定
    homework_detail_choice_unpass_result_text_loc = '', '选择题回答错误'  # 待定
    homework_detail_pass_result_text_loc = '//div[@class="result-text fl is-right"]', '评测通过文本'  # 待定
    homework_detail_unpass_result_text_loc = '//div[@class="result-text fl is-error"]', '评测不通过文本'  # 待定
    homework_detail_push_homework_btn_loc = '//div[text()="提交全部作业"]', '提交作业按钮'  # 待定
    homework_detail_push_homework_confirm_btn_loc = '//div[text()="确定"]', '确定按钮'  # 待定(如果与课程相同则去掉)

    """紧急挑战待定"""
    standard_emergency_challenge_btn_loc = '//span[contains(text(),"紧急")]', '紧急挑战按钮'
    standard_enm_problem_name_loc = '//div[@class="content-position-header"]/span', '紧急挑战题目名称'
    standard_enm_problem_name_loc_1 = '//div[@class="codeview-title"]/span[2]', '紧急挑战后续做题的题目名称'
    standard_challenge_run_btn_loc = '//div[contains(text(),"评测")]', '紧急挑战评测按钮'
    standard_challenge_result_tip_loc = '//div[@class="challenge-run-dialog-wrapper"]' \
                                        '/div[1]/div/div[2]/div/div[1]', '紧急挑战结果提示'
    standard_challenge_next_problem_btn_loc = '//div[text()="继续挑战"]/parent::div/div[2]', '下一道题按钮'
    standard_keep_challenge_btn_loc = '//div[@class="continue-btn"]/span', '继续挑战按钮'
    standard_problem_name_list_loc = '//div[@class="data-back-single-title fl"]', '题目列表名称'
    standard_change_problem_btn_loc = '//span[contains(text(),"换一题")]', '换一题按钮'

    homework_to_do_loc = \
        '//div[@class="homework-container-gird"]/ul/li[1]/div/div/div/div[1]/div[1]/div', '作业列表中第一个作业'
    homework_list_status_loc = \
        '//div[@class="homework-container-gird"]/ul/li[1]/div/div/div/div[2]/div[3]', '作业列表状态'
    homework_quality_loc = '//div[@class="viewcontainer"]/ul/li[2]/div/div[6]/div', '作业质量'
    homework_status_loc = '//div[@class="viewcontainer"]/ul/li[2]/div/div[7]/div', '作业状态'
    view_code_btn_loc = '//div[@class="view-cls"]/div/div[1]/div/a[1]', '去作答按钮'
    choice_btn_loc = '//span[text()="A"]/parent::span/preceding-sibling::span', '选择题选项A'
    answer_tab_code_loc = '//div[@class="tab-views"]/div[2]/div/div/textarea', '参考答案区域光标'
    commit_choice_btn_loc = '//div[contains(text(),"选择题")]', '提交选择题按钮'
    save_result_text_loc = '//div[@class="run-info-bgc-gird"]/div[2]/div[3]/div[2]', '已保存文本'

    """高校版做作业"""
    problem_id_loc = '//div[@class="codeview-left-title-gird"]/span', '题号文本'
    uni_teach_code_view_loc = '//div[@id="ueditor"]/textarea', '教学版作答IDE光标'
    uni_teach_result_text_loc = '//div[@class="code-result-des"]', '教学版运行结果'

    """AI体验"""
    image_identify_tab_loc = '//div[contains(text(),"图")]', '图像识别tab'  # 待定

    upload_pic_loc = '//div[@class="upload-tag"]/img', '上传图片按钮'  # 待定
    output_text_loc = '//div[@class="board-output-inner"]', '识别结果输出区'  # 待定
    car_pic_loc = '//div[@class="right-container fl"]/div/div[7]/div/img', '系统车牌图片'  # 待定

    word_input_loc = '//input[@class="el-input__inner"]', '主题词输入框'  # 待定
    generate_btn_loc = '//span[contains(text(),"生成")]', '生成按钮'  # 待定
    subject_word_loc = '//div[@class="el-row"]/div[5]/div', '系统主题词'  # 待定
    poetry_title_loc = '//div[@class="title"]', '古诗标题'  # 待定
    couples_title_loc = '//div[@class="center"]', '春联标题'  # 待定
    couples_text_loc = '//div[@class="couplet-background"]', '春联文本'  # 待定
    copy_btn_loc = '', '复制按钮'  # 待定

    """试炼场标准编辑"""
    draft_name_input_loc = '//div[@class="operate-save"]/div[1]/input', '草稿名称input框'  # 待定
    save_btn_loc = '//div[text()="保存"]', '保存按钮'  # 待定
    confirm_save_btn_loc = '//div[@class="footer"]', '弹框确定按钮'  # 待定
    ace_text_input_loc = '//div[@class="ace-box"]/div/div/div/textarea', '试炼场游标'  # 待定
    run_code_btn_loc = '//i[@class="iconfont iconpractice_icon_move"]', '试炼场运行代码按钮'  # 待定
    text_out_area_loc = '//div[@class="data-input-inner"]', '试炼场文本输出区'  # 待定
    pygame_canvas_loc = 'myPygameCanvas', 'pygame弹窗'  # 待定
    close_pygame_btn_loc = '//div[@class="pygame-wrap"]/div[1]/div/div/button', 'pygame弹窗关闭按钮'  # 待定
    save_confirm_btn_loc = '//div[@class="footer"]', '保存成功提示弹窗确定按钮'  # 待定
    add_file_btn_loc = '//i[@class="iconfont iconpractice_icon_add"]', '添加文件按钮'  # 待定
    create_file_input_loc = '//div[@class="file-input"]/div/input', '创建文件名称输入框'  # 待定
    add_file_confirm_btn_loc = '//div[@class="el-dialog dialogFile"]/div[3]/div/button[2]', '创建文件确定按钮'  # 待定
    main_file_tab_loc = '//span[contains(text(),"main")]', 'main文件tab'  # 待定
    head_file_loc = '//div[@class="file-choose"]/div/span', '顶部文件按钮'  # 待定
    my_draft_btn_loc = '//div[@class="my-draft"]', '草稿'  # 待定
    first_draft_loc = '//div[@class="draft-content"]/div[1]/div[1]/div[1]', '打开草稿列表第一个草稿名称'  # 待定
    type_choose_loc = '//div[@class="type-choose"]/div/span', '编辑模式选择'  # 待定

    """试炼场创客编辑"""
    ck_type_loc = '//li[contains(text(),"创客编辑")]', '创客编辑模式'  # 待定
    ck_type_output_loc = '//div[@id="example"]/canvas', '创客编辑输出'  # 待定
    robot_config_btn_loc = '//span[contains(text(),"机器人")]', '机器人配置按钮'  # 待定
    robot_box_loc = '//div[@class="robot-content-box"]/ul/li[1]/div[1]', '机器人选择'  # 待定
    connect_robot_btn_loc = '//div[@class="robot-content-box"]/ul/li[1]/div[1]/div/div', '连接机器人按钮'  # 待定
    close_robot_config_btn_loc = '//span[contains(text(),"配置机器人")]/following-sibling::button', '关闭配置机器人'  # 待定
    robot_img_loc = '//div[@class="el-image robot-img"]', '机器人画面'  # 待定

    """发布作品"""
    submit_work_btn_loc = '//span[contains(text(),"发布作品")]', '发布作品按钮'  # 待定
    work_name_input_loc = '//div[@class="el-input el-input--medium"]/input', '作品发布名称输入框'  # 待定

    """素材库"""
    tools_box_loc = 'div.head-right > div:nth-of-type(2) > div > span > i:nth-of-type(2)'  # , '工具箱'  # 待定
    material_lib_loc = '.zsi1.iconfont.iconpractic_icon_source'  # , '素材库'  # 待定
    add_classify_btn = '.my-meterial-add-btn', '我的素材添加分类按钮'  # 待定
    classify_name_input = '//div[@class="my-meterial-list"]/div[2]/div/input', '添加素材名称输入框'  # 待定
    confirm_classify_btn = '//div[@class="my-meterial-list"]/div[2]/span[1]', '添加素材确定按钮'  # 待定
    upload_material_btn_loc = '//div[contains(text(),"上传")]', '上传素材按钮'  # 待定
    edit_name_btn_loc = '//div[@class="my-meterial-container"]/div/div/div[1]/div[2]/div[1]/i', '编辑名称按钮'  # 待定
    delete_material_btn_loc = '//div[@class="my-meterial-container"]/div[1]/div[1]/div[1]/div[2]/i', '删除素材按钮'  # 待定
    material_name_input_loc = '//div[@class="el-row"]/div[1]/div[1]/div[2]/div[2]/div/input', '素材名称输入框'  # 待定
    upload_confirm_btn_loc = '//div[@class="el-message-box__btns"]/button[2]', '确定按钮'  # 待定
    material_img_loc = 'div.my-meterial-container > div > div:nth-of-type(1) > div:nth-of-type(1) > ' \
                       'div:nth-of-type(1) > div'  # 素材图片  # 待定
    material_name_loc = '//div[@class="my-meterial-container"]/div/div/div[1]/div[2]'  # , '素材名称'  # 待定
    classify_handle_loc = '.handle-meterial-type'  # 素材分类操作  # 待定

    """创作空间学生提交作品"""
    my_draft_tab_loc = '', '我的草稿tab'
    draft_btn_loc = '//div[text()="草稿"]', '草稿按钮'  # 待定
    publish_draft_btn_loc = '//div[@class="el-row"]/div[1]/div/div/div[1]/div/div[3]/div[2]/span', '草稿发布按钮'  # 待定
    my_works_tab_loc = '//li[contains(text(),"我的作品")]', '我的作品tab'  # 待定
    public_work_btn_loc = '//span[contains(text(),"发布")]', '发布作品按钮'
    my_work_name_input_loc = '//label[contains(text(),"作品名称")]/parent::div/div/div/input', '作品名称输入框'  # 待定
    work_introduction_input_loc = '//label[contains(text(),"作品简介")]/parent::div/div/div/textarea', '作品简介输入框'  # 待定

    add_work_cursor_loc = '//textarea[@class="ace_text-input"]', '发布作品编辑器游标'
    add_work_picture_btn_loc = '//form[@class="el-form el-form--label-left"]' \
                               '/div[4]/div/div/div/div/div[1]/div', '添加作品图示按钮'
    add_author_picture_btn_loc = '//form[@class="el-form el-form--label-left"]' \
                                 '/div[8]/div/div/div/div/div[1]/div', '添加作者风采按钮'
    sel_class_loc = '//form/div[5]/div/div/div/span/span/i', '作者班级下拉框'
    first_class_loc = '//div[@class="el-select-dropdown el-popper"]/div/div/ul/li[1]/span', '下拉框第一个班级'
    sel_audit_teacher_loc = '//form/div[10]/div/div/div/div/div/span/span', '审核教师下拉框'
    sel_teacher_input_loc = '//form/div[10]/div/div/div/div/div/input', '审核老师input'
    submit_audit_btn_loc = '//div[contains(text(),"提交审核")]', '提交审核按钮'
    # succ_tip_loc = '//p[@class="el-message__content"]'#'提交成功提示'

    """教师审核作品"""
    student_work_tab_loc = '//li[contains(text(),"学生")]', '学生作品tab按钮'
    screening_tab_loc = '//div[text()="审核中"]', '筛选待审核'
    direct_release_btn_loc = '//div[@class="examine-cls"]/button[1]', '直接发布'
    detailed_review_btn_loc = '//div[@class="examine-cls"]/button[2]', '详细审核'
    pass_review_btn_loc = '//div[@class="button-box clearfix"]/div[2]', '通过审核'
    reject_btn_loc = '//div[@class="button-box clearfix"]/div[1]', '驳回'
    works_hall_list_loc = '//div[@class="con-header"]', '作品大厅'

    """教师管理"""
    teacher_manage_tab_loc = '//li[contains(text(),"教师")]', '教师管理tab'
    add_teacher_btn_loc = '//span[text()="添加教师"]', '添加教师按钮'
    add_input_loc = '//input[@class="el-input__inner"]'  # , '创建页面表单所有输入框'
    gender_input_loc = '//span[@class="el-radio__inner"]'  # , '性别选择单选框'
    return_management_btn_loc = '//div[@class="dia-back"]', '返回教师管理、班级管理按钮'

    """班级管理"""
    class_manage_tab_loc = '//li[contains(text(),"班级")]', '班级管理tab'
    add_class_btn_loc = '//span[text()="创建班级"]', '创建班级按钮'
    add_pro_class_btn_loc = '//span[text()="创建课程"]', '创建课程按钮'
    sel_teacher_loc = '//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li[1]', '选择列表第1个老师'
    admin_class_list_first_loc = \
        '//div[@class="con-wrapper"]/div[2]/div[1]/div/div[1]/div[1]', '行政班列表第1个卡片'
    add_student_btn_loc = '//span[text()="添加学生"]', '添加学生按钮'
    operation_btn_loc = \
        '//div[@class="con-wrapper"]/div[2]/div[1]/div/div/div[2]/div/div[3]/div/span', '第1个行政班操作按钮'
    create_course_btn_loc = '//body/ul[2]/li[1]', '生成课程按钮'

    """学生管理"""
    course_manage_tab_loc = '//li[contains(text(),"学生")]', '学生管理tab'  # 待定
    program_class_btn_loc = '//div[text()="课程班"]', '课程班切换按钮'
    class_img_loc = '//li[@class="add-li fl"]', '班级配图'
    pro_class_list_first_loc = \
        '//div[@class="con-wrapper"]/div[2]/div[1]/div/div/div[1]', '课程班列表第1个卡片'
    sel_admin_class_loc = '//ul[@class="left-list"]/li[1]/i', '添加学生选择第1个行政班'
    sel_all_student_loc = '//ul[@class="left-list"]/li[1]/span[2]', '全选按钮'
    confirm_sel_btn_loc = '//span[text()="确 定"]', '选择学生确定按钮'
    add_success_tip_loc = '//p[@class="el-message__content"]', '课程班学生添加成功提示'
    success_tip_loc = '//div[@class="dia-wra"]/h2', '添加成功弹窗成功提示'

    """资源管理"""
    resource_manage_tab_loc = '//li[contains(text(),"资源")]', '资源管理tab'
    resource_type_sel_loc = '//div[@class="el-select el-select--medium"]/div[1]/span', '资源类型下拉框'
    school_resource_btn_loc = '//span[contains(text(),"校本")]', '校本资源选项'
    school_resource_tab_loc = '//div[@class="goclass-menu-gird"]/ul/li[2]', '校本资源tab'
    want_publish_btn_loc = '//span[text()="我要上传"]', '我要上传按钮'
    resource_name_input_loc = '//div[@class="add-class-bg-gird"]/div[2]/div[1]/div[2]/div/input', '资源标题'
    resource_img_loc = '//div[@class="add-li-wra"]'  # , '课件封面'
    course_describe_loc = '//div[@class="el-textarea el-input--medium el-input--suffix"]/textarea', '课件描述'
    upload_file_btn_loc = \
        '//div[@class="add-class-bg-gird"]/div[2]/div[5]/div[2]/div/div/div/div[1]/span', '上传课件'
    upload_file_btns_loc = '//span[contains(text(),"上传文件")]'  # , '所有上传课件按钮'
    continue_to_upload_loc = '//span[contains(text(),"继续上传")]'  # , '所有继续上传按钮'
    visibility_sel_loc = '//div[text()="可见性"]/parent::div/div[2]/div/div[1]', '可见性选择'
    publish_btn_loc = '//span[text()="发布"]', '发布按钮'
    # succ_tip_loc = '//h2[@class="dia-header"]'#'发布成功提示框'
    back_button_loc = '//div[@class="dia-back"]', '提示框返回按钮'
