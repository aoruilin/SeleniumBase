from selenium.webdriver.common.by import By


class ElementSelector:
    """页面遮罩层"""
    loading_mask_loc = '//div[@class="el-loading-mask is-fullscreen"]'

    """页面所有元素"""
    all_loc = '//body', '页面所有元素'

    """登录页面"""
    username_input_loc = '//input[@name="username"]', '用户名输入框'
    password_input_loc = '//input[@name="password"]', '密码输入框'
    save_login_loc = '//span[@class="el-checkbox__inner"]', '保存登录信息选项'
    login_btn_loc = '//span[text()="登录"]', '登录按钮'
    uni_teach_login_btn_loc = '//span[contains(text(),"登录")]/parent::button', '教学版登录按钮'

    class_manage_text_loc = '//div[@class="model-tips-word"]', '班级管理文本'

    wrong_login_tip_loc = '//div[@class="el-message el-message--error is-center"]/p', '登录错误提示'
    wrong_username_tip_loc = \
        '//form[@class="el-form login-form el-form--label-left"]/div[1]/div/div[2]', '用户名错误提示'
    wrong_password_tip_loc = \
        '//form[@class="el-form login-form el-form--label-left"]/div[2]/div/div[3]', '密码错误提示'

    """导航栏"""
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

    """意见反馈"""
    feedback_btn_loc = '//div[contains(text(),"意见")]', '意见反馈'
    content_textarea_loc = '//textarea[@class="el-textarea__inner"]', '内容输入框'
    feedback_upload_pic_loc = '//div[@class="el-upload el-upload--picture-card"]', '上传图片按钮'
    submit_btn_loc = '//span[contains(text(),"提交")]', '提交按钮'

    """头像下拉选项"""
    head_portrait_loc = '//div[@class="navbar-container"]/div/div[2]/div[2]/div', '头像'
    logout_btn_loc = '//span[text()="退出"]', '退出按钮'
    edu_text_loc = '//div[@class="new-logobox"]/div[2]/span', '首页教育版文本'

    """首页添加课件和作业"""
    index_add_homework_btn_loc = '//span[text()="发布作业"]', '首页发布作业按钮'
    standard_mode_btn_loc = '//div[@class="course-hw"]/div[1]', '标准授课发布课件作业按钮'  # div[class="cou-hw-bg"]
    subject_mode_btn_loc = '//div[@class="course-hw"]/div[2]', '主题授课发布课件作业按钮'  # div[class="cou-hw-bg cou-hw-bg1"]

    """首页统计栏课件作业"""
    index_course_name_loc = \
        '//div[@class="home-stu-course-container clearfix"]/div[1]/div/div/div[1]', \
        '学生端首页最新课程课程名称'  # .home-stu-course-container.clearfix>div:nth-of-type(1)>div>div>div

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
    add_course_loc = '//span[text()="添加课件"]', '添加课件'
    first_course_loc = \
        '//div[@class="course-container-gird"]/ul/li[1]/div/div/div[2]/div[1]/div', '课件列表第一个课件'
    homework_btn_loc = '//div[@class="goclass-menu-gird"]/ul/li[2]', '课件列表顶部作业按钮'

    """作业列表"""
    add_homework_btn_loc = '//div[@class="homework-bg-gird"]/div[1]/div[3]/button', '发布作业按钮'
    homework_list_name = \
        '//div[@class="homework-container-gird"]/ul/li[1]/div/div/div/div[1]/div[1]/div', '作业列表作业名称'

    """主题授课首页"""
    start_discover_btn_loc = '//span[contains(text(),"探索")]', '探索按钮'
    index_course_btn_loc = '//span[text()="课程"]', '首页课程按钮'
    index_homework_btn_loc = '//span[text()="作业"]', '闯关首页作业按钮'

    """主题授课中国地图"""
    map_s1_btn_loc = '//div[@class="level"]/div/span/img', '中国地图所有系列'

    """主题授课地图路径"""
    path_btn_loc = '//div[@class="level"]/div', '路径点'

    """主题授课关卡内按钮"""
    watch_course_btn_loc = '//span[text()="看课件"]', '看课件按钮'
    watch_homework_btn_loc = '//span[text()="看作业"]', '看作业按钮'
    kj_add_checkpoint_course_loc = '//div[@class="kj-img"]', '关卡内课件详情添加课件按钮'

    """主题授课作业列表"""
    add_checkpoint_homework_loc = '//span[text()="发布作业"]', '发布作业按钮'

    """主题授课课件列表"""
    add_checkpoint_course_loc = '//span[text()="发布课件"]', '发布课件按钮'
    first_course_name_loc = '//div[@class="dia-container clearfix"]/div[1]/div/div/div[2]', '第一个课件名称'

    """主题授课选择关卡"""
    choice_checkpoint_loc = '//div[text()="选择关卡"]/parent::div/div[2]/div/div[1]/span', '选择关卡'

    """标准授课添加课件"""
    choice_teaching_package_loc = '//span[text()="叮当资源"]/parent::label/span[1]', '选择叮当资源'
    selKnow_loc = '//div[@class="cascader-bgc mar-cls"]/div/div/span/span', '选择知识点'
    choice_course_btn_loc = \
        '//div[@class="item-card-center"]/ul/li[1]/div/div/div[2]/div/div[2]/div[3]/label/span[1]/span', \
        '选择按钮'
    choice_cla = '//div[text()="发布班级"]', '发布班级按钮'
    choice_all = '//span[text()="全选"]', '全选按钮'
    choice_class_btn_loc = '//div[@class="class-select-container-gird"]/ul/li[1]', '选择第1个班级'
    add_publish_btn = '//div[@class="set-course-bgc"]/div/div[2]/label/span/span', '添加并发布按钮'
    add_btn_loc = '//div[@class="add-course-submit-gird"]/button', '添加按钮'
    repeated_tip_confirm_loc = '//div[contains(text(),"确定")]', '重复提示确定按钮'
    succ_tip_loc = '//p[@class="el-message__content"]', '添加成功提示'
    go_add_homework_btn_loc = '//span[contains(text(),"发布作业")]', '去发布作业按钮'
    go_on_btn_loc = '//span[contains(text(),"继续")]', '弹窗继续添加按钮'
    standard_course_crumb_loc = '//div[@class="el-breadcrumb"]/span[1]/span[1]', '标准授课面包屑'
    course_name_loc = '//div[@class="course-container-gird"]/ul/li[1]/div/div/div[2]/div/div', '课程名称'
    wrapper_elem = '//div[@class="el-scrollbar__wrap"]'

    """主题授课添加课件"""
    checkpoint_choice_btn_loc = '//div[@class="item-card-center"]/ul/li[1]/div/div[4]/label/span[1]', '选择按钮'
    checkpoint_choice_class_btn_loc = '//div[text()="发布班级"]/parent::div/div[2]/div/label[1]/span[1]', '第一个班级'
    checkpoint_add_publish_btn = \
        '//div[@class="zs-dialog__wrapper"]/div/div[5]/div[2]/div/label[1]/span[1]', '添加并发布按钮'
    checkpoint_publish_btn_loc = '//span[text()="发布"]', '发布按钮'
    # check_point_course_name_loc = '//div[@class="dia-container clearfix"]/div[1]/div/div/div[2]'#'列表课件名称'
    check_point_course_name_loc = '//h1[@class="deco-header elli_1"]', '详情课件名称'

    """标准授课查看课件"""
    courseCard_tit_loc = '//div[@class="courseware-card-title-word elli_1 fl"]', '课程详情页面课程名称'
    lookNumber_loc = '//div[@class="courseware-card-looknumber"]', '课程详情页面查看人数'
    ppt_next_btn_loc = '//span[@class="cui-toolbar-buttondock aligncenter"]/a[3]', '课件PPT下一页按钮'
    ppt_pages_num_loc = '//span[@class="cui-toolbar-buttondock aligncenter"]/a[2]', '课件页数'
    crumbs_loc = '//div[@class="courseware-title"]/font[1]', '面包屑'

    edit_btn_loc = '//div[@class="trigger-editer-icon"]', '精简试炼场弹出开关'
    putback_btn_loc = '//span[contains(text(),"收起")]', '精简试炼场收起开关'
    edit_cursor_loc = '//div[@class=" ace_editor ace-cobalt ace_dark"]/textarea', '精简试炼场游标'
    text_output_btn_loc = '//div[contains(text()#"文本")]', '文本输出区按钮'
    text_output_area_loc = '//div[@class="simple-output-item"]', '文本输出'
    pic_output_btn_loc = '//div[contains(text(),"图形")]', '图形输出区按钮'
    pic_output_area_loc = '//div[@class="gird"]/img', '图形输出'
    course_run_code_btn_loc = '//span[contains(text(),"运行")]', '运行代码按钮'
    iframe_loc = '//div[@class="courseware-content-ware"]/iframe', '第一层iframe'

    """主题授课查看课件"""
    first_go_to_checkpoint_btn = \
        '//div[@class="dia-container clearfix"]/div[1]/div/div/div[6]/div[2]', '前往关卡按钮'

    back_to_map_btn_loc = '//div[@class="backHome flex flex-pack-end"]/a[1]', '返回到中国地图'
    sub_course_back_btn_loc = '//div[@class="backHome flex flex-pack-end"]/a[2]', '返回按钮'
    back_to_home_btn_loc = '//div[@class="backHome flex flex-pack-end"]/a[3]', '返回闯关授课主页'
    checkpoint_course_name_loc = '//h1[@class="deco-header elli_1"]', '课件名称'
    first_in_course_loc = '//div[@class="el-tree zs-tree-node"]/div[1]/div[1]/div', '查看课件页面课件列表第一个'

    """标准授课发布作业"""

    homework_name_input_loc = '//div[@class="container-box-item-0"]/div/input', '作业名称输入框'
    choice_pointId_btn_loc = '//div[@class="container-box-item-1"]/button', '选取知识点按钮'
    sel_know_loc = '//div[@class="dialog-inner-input clearfix"]/div[2]/div/div/span/span', '选择知识点'
    choice_problem_loc = '//span[contains(text(),"选择")]', '选择题'
    operation_problem_loc = '//span[contains(text(),"操作")]', '操作题'
    problem_time_choice_loc = '//div[@class="minutes-select"]/div/label', '选择习题时间'
    choice_all_btn_loc = '//div[@class="check-box"]/label/span[1]/span', '全选按钮'
    choice_first_problem_loc = '//div[@class="el-row"]/div[1]/label/span[1]/span', '选题列表第一道题'
    confirm_publish_btn_loc = '//div[@class="el-dialog__footer"]/span/button', '确定按钮'
    show_answer_loc = '//div[contains(text(),"参考答案")]/parent::div/div[2]/div/input', '显示参考答案下拉框'
    show_result_loc = '//div[text()="显示运行结果"]/parent::div/div[2]/div/input', '显示运行结果下拉框'
    end_time_input_loc = '//div[contains(text(),"截止时间")]/parent::div/div[2]/input', '截止时间输入'
    public_answer_loc = '//span[text()="立即公布"]/parent::li', '公布答案'
    timing_btn_loc = '//div[contains(text(),"定时发布")]/parent::div/div[2]/span', '定时发布按钮'
    timing_input_loc = '//div[contains(text(),"定时发布")]/parent::div/parent::div/div[4]/div[2]/input', '定时时间输入'
    public_homework_btn_loc = '//span[text()="发布"]/parent::button', '发布按钮'

    """主题授课发布作业"""
    course_close_btn_loc = '//span[@class="zs-dialog__closer"]', '课件列表关闭按钮'
    checkpoint_homework_name_input_loc = '//div[text()="作业名称"]/parent::div/div[2]/div/input', '作业名称输入框'
    checkpoint_choice_problem_btn_loc = '//span[text()=" 选题"]', '选题按钮'
    checkpoint_choice_problem_loc = '', '选择题'
    checkpoint_operation_problem_loc = '', '操作题'
    checkpoint_choice_all_btn_loc = '//span[text()="全选"]/parent::label/span[1]', '全选按钮'
    checkpoint_confirm_problem_btn_loc = '//div[text()="确定"]', '选题确定按钮'
    checkpoint_show_answer_loc = '//div[text()="参考答案"]/parent::div/div[2]/div/div/span', '参考答案下拉框'
    checkpoint_public_answer_loc = '//span[text()="显示"]/parent::li', '显示答案选项'
    checkpoint_timing_btn_loc = '//div[text()="定时发布"]/parent::div/div[2]/div/div/span', '定时发布按钮'
    checkpoint_timing_input_loc = '//div[text()="定时发布"]/parent::div/div[2]/div[2]/div/input', '定时时间输入'
    checkpoint_end_time_input_loc = '//div[text()="截止提交时间"]/parent::div/div[2]/div/input', '截止时间输入框'
    checkpoint_homework_list_name = '//div[@class="items-gird"]/div[1]/div[1]/div[1]/div[1]', '闯关作业列表第一个作业'
    checkpoint_all_homework_name = '//div[@class="title fl"]', '作业列表所有作业名称'

    # succ_tip_loc = '//p[@class="el-message__content"]'#'添加成功提示'
    fail_tip_loc = '//div[@class="el-message el-message--error is-center"]/p', '添加失败提示'

    """标准授课做作业"""
    homework_to_do_loc = \
        '//div[@class="homework-container-gird"]/ul/li[1]/div/div/div/div[1]/div[1]/div', '作业列表中第一个作业'
    view_code_btn_loc = '//div[@class="view-cls"]/div/div[1]/div/a[1]', '去作答按钮'
    problem_list_loc = '//div[@class="data-back-single-title fl"]'  # , '题目列表'
    problem_id_loc = '//div[@class="codeview-left-title-gird"]/span', '题号文本'
    answer_btn_loc = '//div[@class="el-tabs__nav is-top"]/div[2]', '参考答案按钮'
    answer_tab_code_loc = '//div[@class="tab-views"]/div[2]/div/div/textarea', '参考答案区域光标'
    choice_btn_loc = '//span[text()="A"]/parent::span/preceding-sibling::span', '选择题选项A'
    code_view_loc = '//div[@id="ueditor"]/textarea', '作答IDE光标'
    commit_choice_btn_loc = '//div[contains(text(),"选择题")]', '提交选择题按钮'
    save_run_btn_loc = '//div[contains(text(),"保存并评测")]', '保存并运行按钮'
    pass_result_text_loc = '//div[@class="result-text fl is-right"]', '评测通过文本'
    unpass_result_text_loc = '//div[@class="result-text fl is-error"]', '评测不通过文本'
    save_result_text_loc = '//div[@class="run-info-bgc-gird"]/div[2]/div[3]/div[2]', '已保存文本'
    push_homework_btn_loc = '//div[text()="提交全部作业"]', '提交作业按钮'
    confirm_btn_loc = '//div[text()="确定"]', '确定按钮'
    homework_list_status_loc = \
        '//div[@class="homework-container-gird"]/ul/li[1]/div/div/div/div[2]/div[3]', '作业列表状态'
    homework_quality_loc = '//div[@class="viewcontainer"]/ul/li[2]/div/div[6]/div', '作业质量'
    homework_status_loc = '//div[@class="viewcontainer"]/ul/li[2]/div/div[7]/div', '作业状态'

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

    """主题授课做作业"""
    go_to_code_btn_loc = '//div[contains(text(),"去答题")]', '去答题按钮'
    homework_name_loc = '//div[@class="items-gird"]/div[1]/div[1]/div[1]/div[1]', '作业列表第一个作业名称'
    homework_analysis_btn_loc = '//div[@class="items-gird"]/div[1]/div[2]/div', '第一个作业的作业分析按钮'
    checkpoint_view_code_btn_loc = '//div[@class="container-body"]/div[1]/div[4]', '去作答按钮'
    checkpoint_problem_list_btn_loc = \
        '//div[@class="codeview-bg clearfix main-content"]/div[2]/div[1]/button', '题目列表按钮'
    checkpoint_save_run_btn_loc = '//span[text()="保存并评测"]', '保存并运行按钮'
    checkpoint_confirm_btn_loc = '//span[text()="确定"]', '运行结果弹框确定按钮'
    checkpoint_push_homework_btn_loc = '//span[text()="提交全部作业"]', '提交作业按钮'
    checkpoint_push_confirm_btn_loc = '//div[text()="确定"]', '确定提交按钮'
    result_tip_loc = \
        '//div[text()="作业分析"]/parent::div/parent::div/parent::div/parent::div/div[4]/span', '作业结果提示'
    analysis_btn_loc = '//div[text()="作业分析"]', '作业分析按钮'
    wrong_redo_btn_loc = '//div[contains(text(),"错题重做")]', '错题重做按钮'
    problem_list_name_loc = '//div[@class="el-row"]/div/div/div[2]'  # , '题目列表的名称'
    problem_name_loc_1 = '//div[@class="codeview-title"]/span[2]', '后续做题的题目名称'
    wrong_problem_name_loc = '//div[@class="el-row"]/div[1]', '错题重做题目列表第一个题'
    problem_name_loc = '//div[@class="codeview-title"]/span/span[2]', '页面顶部题目名称'
    checkpoint_homework_status_loc = '//div[@class="content-nav-header clearfix"]/div[1]/div[4]', '作业状态'
    close_btn_loc = '//span[@class="zs-dialog__closer"]', '关闭按钮'
    return_homework_btn_loc = '//span[text()="返回作业"]', '返回作业按钮'

    emergency_challenge_btn_loc = '//div[contains(text(),"紧急挑战")]', '紧急挑战按钮'
    enm_problem_name_loc = '//div[@class="codeview-title"]/span', '紧急挑战题目名称'
    enm_problem_name_loc_1 = '//div[@class="codeview-title"]/span[2]', '紧急挑战后续做题的题目名称'
    challenge_result_tip_loc = '//div[text()="继续挑战"]' \
                               '/parent::div/parent::div/parent::div/parent::div/div[3]/span', '紧急挑战结果提示'
    challenge_next_problem_btn_loc = '//div[text()="继续挑战"]/parent::div/div[2]', '下一道题按钮'
    keep_challenge_btn_loc = '//div[text()="继续挑战"]', '继续跳转按钮'
    problem_name_list_loc = '//div[@class="data-back-single-title fl"]', '题目列表名称'
    change_problem_btn_loc = '//span[contains(text(),"换一题")]', '换一题按钮'

    """高校版做作业"""
    uni_teach_code_view_loc = '//div[@id="ueditor"]/textarea', '教学版作答IDE光标'
    uni_teach_result_text_loc = '//div[@class="code-result-des"]', '教学版运行结果'

    """AI体验"""
    image_identify_tab_loc = '//div[contains(text(),"图")]', '图像识别tab'

    upload_pic_loc = '//div[@class="upload-tag"]/img', '上传图片按钮'
    output_text_loc = '//div[@class="board-output-inner"]', '识别结果输出区'
    car_pic_loc = '//div[@class="right-container fl"]/div/div[7]/div/img', '系统车牌图片'

    word_input_loc = '//input[@class="el-input__inner"]', '主题词输入框'
    generate_btn_loc = '//span[contains(text(),"生成")]', '生成按钮'
    subject_word_loc = '//div[@class="el-row"]/div[5]/div', '系统主题词'
    poetry_title_loc = '//div[@class="title"]', '古诗标题'
    couples_title_loc = '//div[@class="center"]', '春联标题'
    couples_text_loc = '//div[@class="couplet-background"]', '春联文本'
    copy_btn_loc = '', '复制按钮'

    """试炼场标准编辑"""
    draft_name_input_loc = '//div[@class="operate-save"]/div[1]/input', '草稿名称input框'
    save_btn_loc = '//div[text()="保存"]', '保存按钮'
    confirm_save_btn_loc = '//div[@class="footer"]', '弹框确定按钮'
    ace_text_input_loc = '//div[@class="ace-box"]/div/div/div/textarea', '试炼场游标'
    run_code_btn_loc = '//i[@class="iconfont iconpractice_icon_move"]', '试炼场运行代码按钮'
    text_out_area_loc = '//div[@class="data-input-inner"]', '试炼场文本输出区'
    pygame_canvas_loc = 'myPygameCanvas', 'pygame弹窗'
    close_pygame_btn_loc = '//div[@class="pygame-wrap"]/div[1]/div/div/button', 'pygame弹窗关闭按钮'
    save_confirm_btn_loc = '//div[@class="footer"]', '保存成功提示弹窗确定按钮'
    add_file_btn_loc = '//i[@class="iconfont iconpractice_icon_add"]', '添加文件按钮'
    create_file_input_loc = '//div[@class="file-input"]/div/input', '创建文件名称输入框'
    add_file_confirm_btn_loc = '//div[@class="el-dialog dialogFile"]/div[3]/div/button[2]', '创建文件确定按钮'
    main_file_tab_loc = '//span[contains(text(),"main")]', 'main文件tab'
    head_file_loc = '//div[@class="file-choose"]/div/span', '顶部文件按钮'
    my_draft_btn_loc = '//div[contains(text(),"我的草稿")]', '我的草稿'
    first_draft_loc = '//div[@class="draft-content"]/div[1]/div[1]/div[1]', '打开草稿列表第一个草稿名称'
    type_choose_loc = '//div[@class="type-choose"]/div/span', '编辑模式选择'

    """试炼场创客编辑"""
    ck_type_loc = '//li[contains(text(),"创客编辑")]', '创客编辑模式'
    ck_type_output_loc = '//div[@id="example"]/canvas', '创客编辑输出'
    robot_config_btn_loc = '//span[contains(text(),"机器人")]', '机器人配置按钮'
    robot_box_loc = '//div[@class="robot-content-box"]/ul/li[1]/div[1]', '机器人选择'
    connect_robot_btn_loc = '//div[@class="robot-content-box"]/ul/li[1]/div[1]/div/div', '连接机器人按钮'
    close_robot_config_btn_loc = '//span[contains(text(),"配置机器人")]/following-sibling::button', '关闭配置机器人'
    robot_img_loc = '//div[@class="el-image robot-img"]', '机器人画面'

    """发布作品"""
    submit_work_btn_loc = '//span[contains(text(),"发布作品")]', '发布作品按钮'
    work_name_input_loc = '//div[@class="el-input el-input--medium"]/input', '作品发布名称输入框'

    """素材库"""
    tools_box_loc = '//span[contains(text(),"工具箱")]', '工具箱'
    material_lib_loc = '//div[contains(text(),"素材库")]', '素材库'
    add_classify_btn = '.my-meterial-add-btn', '我的素材添加分类按钮'
    classify_name_input = '//div[@class="my-meterial-list"]/div[2]/div/input', '添加素材名称输入框'
    confirm_classify_btn = '//div[@class="my-meterial-list"]/div[2]/span[1]', '添加素材确定按钮'
    upload_material_btn_loc = '//div[contains(text(),"上传")]', '上传素材按钮'
    edit_name_btn_loc = '//div[@class="my-meterial-container"]/div[1]/div[1]/div[1]/div[2]/div[2]/div', '编辑名称按钮'
    delete_material_btn_loc = '//div[@class="my-meterial-container"]/div[1]/div[1]/div[1]/div[2]/i', '删除素材按钮'
    material_name_input_loc = '//div[@class="el-message-box__content"]/div/div[1]/input', '素材名称输入框'
    upload_confirm_btn_loc = '//div[@class="el-message-box__btns"]/button[2]', '确定按钮'
    material_name_loc = '//div[@class="my-meterial-container"]/div[1]/div[1]/div[2]/div', '素材名称'

    """创作空间学生提交作品"""
    my_works_tab_loc = '//li[contains(text(),"我的作品")]', '我的作品tab'
    public_work_btn_loc = '//span[contains(text(),"发布")]', '发布作品按钮'
    my_work_name_input_loc = '//label[contains(text(),"标题")]/parent::div/div/div[1]/div/div/input', '作品名称输入框'
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
