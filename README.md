# PDF 压缩器

## 概述

PDF 压缩器是一个使用 Flask 和 Python 编写的简单 web 应用，它可以接收用户上传的 PDF 文件，然后将其压缩后返回给用户。

## 功能

- 接收用户上传的 PDF 文件
- 判断 PDF 文件类型（图片型或文本型）
- 压缩 PDF 文件
- 将压缩后的 PDF 文件返回给用户

## 部署方法

本应用使用 Flask 作为 web 框架，可以使用任何支持 WSGI 的 web 服务器进行部署，例如 Gunicorn、uWSGI 或 Apache。以下是一个使用 Gunicorn 的部署示例：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

这行命令会启动一个使用 4 个工作进程，监听 0.0.0.0:5000 地址的 Gunicorn 服务器。

## 依赖安装方法

```bash
apt install python3-pikepdf gunicorn
```

本应用的依赖列在 `requirements.txt` 文件中，可以使用以下命令安装：

```bash
pip install -r requirements.txt
```

这行命令会安装所有在 `requirements.txt` 文件中列出的依赖。

## Nginx 部署

Nginx 本身并不直接支持 WSGI，但它可以与其他支持 WSGI 的服务器，如 Gunicorn 或 uWSGI，配合使用。在这种配置中，Nginx 通常作为反向代理服务器，接收来自客户端的请求，然后将这些请求转发到后端的 WSGI 服务器。

以下是一个典型的 Nginx 与 Gunicorn 配合的配置示例：

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

在这个配置中，Nginx 监听 80 端口，接收来自 `yourdomain.com` 的请求。然后，Nginx 将这些请求转发到在 `127.0.0.1:8000` 运行的 Gunicorn 服务器。

这只是一个基本的配置，你可能需要根据你的具体需求来修改它。例如，你可能需要配置 SSL，添加访问控制，或者调整日志设置等。

另外，请注意，你需要在启动 Gunicorn 服务器时指定正确的 IP 地址和端口，确保它与 Nginx 的配置相匹配。例如，你可以使用以下命令启动 Gunicorn 服务器：

```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

在这个命令中，`-b 127.0.0.1:8000` 参数指定 Gunicorn 服务器监听 `127.0.0.1:8000` 地址。