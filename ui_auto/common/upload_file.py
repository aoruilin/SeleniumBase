import subprocess

from ui_auto.common.get_cwd import get_absolute_path


def upload_file_by_auto_it(file_type):
    project_cwd = get_absolute_path('ui_auto')
    upload_file_cmd = project_cwd.joinpath(f'common\\upload_file\\upload_{file_type}.exe').as_posix()
    proc = subprocess.Popen(upload_file_cmd)
    out, err = proc.communicate()
    print(f'运行上传文件输出：{out}，报错：{err}')
