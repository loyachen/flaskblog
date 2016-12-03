## Loyachen's Blog Powered By Flask.

这是一个用 Python Flask 框架写的个人博客。基本实现了文章展示，以及一个包含导航分类管理文章发布与管理的后台，同时引用了多说评论。

基于 Python 3.5.2 、Mysql 5.6

初始管理员是:

```
email='qingkang1993@163.com', username='loya', password='loya'
```



**git clone后，通过如下步骤启动：**

1.使用 virtualenv 创建虚拟环境

2.pip install -r requirements.txt 安装依赖

3.在 config.py 中设置mysql路径

4.python manage deploy

5.python manage.py runserver --host 0.0.0.0



**示例：**

登录：

https://raw.githubusercontent.com/loyachen/flaskblog/dev/Readme_images/login.jpg

