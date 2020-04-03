# 数据库吧code拿出来
import pymysql


def get_code(problem_id, problem_name, challenge=False):
    if challenge:
        sql = "SELECT pc.code from problem_code pc join problem  p WHERE  p.id = pc.problem_id and p.title=%s"
    else:
        sql = "SELECT code_python FROM dim_subject_problem WHERE id=%s"
    tup_code = execute_sql(sql, problem_id, problem_name, challenge)
    try:
        code = tup_code[0][0]
    except IndexError:
        code = '没有查询到题目代码'
    except Exception as e:
        code = f'{e}, 查询代码异常'

    return code


def get_choice(problem_id, problem_name, challenge=False):
    sql = "SELECT answer from dim_subject_choice WHERE id=%s"
    tup_choice = execute_sql(sql, problem_id, problem_name, challenge)
    try:
        choice = tup_choice[0][0]
    except IndexError:
        choice = '没有查询到答案'
    except BaseException as e:
        choice = f'{e},查询答案异常'

    return choice


def execute_sql(sql, problem_id, problem_name, challenge):
    db = pymysql.connect('sh-cdb-9emlkgqw.sql.tencentcdb.com', 'root', 'zsyl@2020', 'pt_edu3', 61227)
    cursor = db.cursor()
    if challenge:
        cursor.execute(sql, (problem_name,))
    else:
        cursor.execute(sql, (problem_id,))
    data = cursor.fetchall()
    db.close()

    return data


# print(get_code(problem_id=9317, problem_name=None, challenge=False))
# print(get_choice(problem_id=438, problem_name=None, challenge=False))
