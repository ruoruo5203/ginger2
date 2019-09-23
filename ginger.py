"""

"""
from werkzeug.exceptions import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError


# 调用creat_app
app = create_app()

#全局 异常处理
@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 是否调试模式，是否显示全部信息
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e

# 判断当前文件是否为入口文件
if __name__ == '__main__':
    # 使用run方法，启动服务器，打开调试模式
    app.run(debug=True)
