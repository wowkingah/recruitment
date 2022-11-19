# 基于已经构建好的 base 构建，
# 事先使用 Dockerfile-base 构建 wowkingah/django-recruitment-base:0.1 镜像
# 或者从 docker.io pull 0.1 版本的 base镜像，这个镜像中有完整的 python/django 包
FROM wowkingah/django-recruitment-base:0.1
WORKDIR /data/recruitment
ENV server_params=
COPY . .
EXPOSE 8000
CMD ["/bin/sh", "/data/recruitment/start_docker_local.sh"]