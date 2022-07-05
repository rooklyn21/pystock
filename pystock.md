## vscode远端开发

```bash
1) 安装插件
Remote-SSH
Remote-Containers

2) 配置远程登录
创建公钥免密登录C:\Users\admin\.ssh
ssh-keygen -t rsa -b 2048
不要设密码


ssh-copy-id lynxluu@127.0.0.1 -p9043 # linux

vi ~/.ssh/authorized_keys
将 Windows 电脑 id_rsa.pub里的文本，拷贝到虚拟机 authorized_keys 里

3) 确认权限
chmod 600 .ssh/authorized_keys
chmod 700 .ssh

在.ssh config里配置
Host centos7a
        HostName 127.0.0.1
        User lynxluu
        Port 9043
        IdentityFile "C:\Users\admin\.ssh\id_rsa.pub"
```



## 安装Anaconda3
wget --no-check-certificate https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.3.1-Linux-x86_64.sh 

bash Anaconda3-5.3.1-Linux-x86_64.sh

1） 报错处理
Anaconda3-5.3.1-Linux-x86_64.sh: line 353: bunzip2: command not found
yum install bzip2

2） 环境变量
source /home/lynxluu/anaconda3/etc/profile.d/conda.sh
conda list

3) 选择远程环境
当打开一个py文件之后，会自动搜索python interpreter，可以直接点击它进行修改。
如果没有显示的话，还可以使用shift+ctrl+p打开命令面板，搜索python:select interpreter进行修改

## 安装docker
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install docker-ce

systemctl start docker
systemctl enable docker

# 配置非root用户使用docker，添加当前用户到docker组，当前用户退出系统后，重新登陆，进行验证：
sudo groupadd docker
sudo gpasswd -a ${USER} docker / sudo usermod -a -G docker $USER
sudo systemctl restart docker
logout && login

# 检查
grep docker /etc/group
docker ps -a

# docker pull 出现 connection reset by peer
当访问 registry-1.docker.io 的时候，DNS 解析到的 ip 当前不可用
yum install bind-utils
dig auth.docker.io

# vscode 配置
打开一个dockefile，在vscode中ctrl+shift+p,出现命令行，之后attach to running container。



## 传输文件
windows 7zip打包为 pystock.tar.gz
sftp put pystock.tar.gz
目标服务器解压
tar -zxvf pystock.tar.gz


## 启动pystock项目 
mkdir -p /data/mariadb/data
docker pull pythonstock/pythonstock:latest
docker pull mariadb:latest

docker run --name mariadb -v /home/lynxluu/pystock/data/mariadb/data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=mariadb -p 3306:3306 -d mariadb:latest

docker run -itd --link=mariadb --network pystock_default --name stock  \
    -v /home/lynxluu/pystock/data/notebooks:/data/notebooks \
    -p 8888:8888 \
    -p 9999:9999 \
    pythonstock/pythonstock:latest
    
 docker run -itd --link=mariadb --network pystock_default --name stock1  \
    -v /home/lynxluu/pystock/data/notebooks:/data/notebooks \
    -p 8881:8881 \
    -p 9991:9991 \
    pythonstock/pythonstock:1.00
    

docker-compose up -d
# --build重新打包
docker-compose up --build -d
# --force-recreate 重新创建容器
docker-compose up  --force-recreate stock1 -d

## 修改代码后，要重建镜像并启动容器，

```bash
1）因为 docker-compose.yaml文件里是从docker-hub拉取的pystock，所以无法使用本地变更的代码。需要改一下
有时候报错要先删除
docker ps -a
docker rm xxx xxx xxx


2） 改用用dockerfile打包本地镜像 pythonstock/pythonstock:1.00
docker build -t pythonstock/pythonstock:1.00 .

bash build.sh
shell脚本 $'\r': command not found
是因为编写的 shell脚本 是在win下编写的，编辑器默认的行尾是 \r\n，而在Unix中认为行尾是 \n，所以把之前的 \r当成命令了。
sed -i 's/\r$//' filename

3）debug 容器启动失败
docker logs stock  没有显示任何信息
docker inspect 44bc360b06a6

4) 修改挂载路径后
docker: Error response from daemon: Cannot link to /mariadb, as it does not belong to the default network.

docker inspect mariadb
查看NetworkSettings--NetworkID：4e37c1ff628846b

5）查看所有容器Networks信息
docker network ls
4e37c1ff6288   pystock_default   bridge    local

启动参数里加  --link=mariadb --network pystock_default

6） docker-compose.yaml 缩进不对
docker-compose up -d
services.volumes must be a mapping

7） 改了stock1的端口，报错：应该内外端口统一改
Bind for 0.0.0.0:9999 failed: port is already allocated.

## 运行代码
docker exec -it stock bash
cd /data/stock/jobs
python 18h_daily_job.py

报错，缺少数据表，是因为没有初始化数据
[2326 rows x 17 columns]
insert sql: DELETE FROM `stock_zh_ah_name` where `date` = '20220614' 
error : (1146, "Table 'stock_data.stock_zh_ah_name' doesn't exist")


[221 rows x 8 columns]
insert sql: DELETE FROM `stock_sina_lhb_ggtj` where `date` = '20220614' 
error : (1146, "Table 'stock_data.stock_sina_lhb_ggtj' doesn't exist")
['code', 'name', 'ranking_times', 'sum_buy', 'sum_sell', 'net_amount', 'buy_seat', 'sell_seat', 'date']
################ tmp_datetime : 2022-06-14
```


### 磁盘扩容
关闭虚拟机，然后调整大小
cd D:\app\VirtualBox

VBoxManage modifyhd “D:\vms\CentOS7\CentOS7.vdi” –-resize 51200
VBoxManage modifyhd “D:\vms\CentOS7a\CentOS7a.vdi” –-resize 51200


1) 创建分区
fdisk /dev/sda
n-p-3-enter-enter-p-w
fdisk -l
reboot

2) 改分区类型为linux LVM,改ext4
fdisk /dev/sda
m-t-3-L-8e-w
mkfs.ext4 /dev/sda3

3) 扩展磁盘
pvcreate /dev/sda3
pvdisplay #根据sda1的VG Name确定下一步的VG Name
vgextend centos /dev/sda3

Couldn't create temporary archive name
存储使用100%，无法挂载，删掉部分文件即可

4) 扩容1
lvresize -l +100%FREE /dev/mapper/centos-root
lvs

5) 扩容2
xfs_growfs /dev/mapper/centos-root
df -h
 
centos系统磁盘扩容 1.查看磁盘空间大小，使用df -h 命令。 
2. 增加磁盘空间，例如下图使用VM虚拟机增加的方式。 物理机直接安装挂载上去。 
3. 使用 fdisk /dev/sda, 创建新分区。 
4.重启Linux操作系统，使用 reboot 命令。 
5.创建物理卷 使用 pvcreate /dev/sda3 命令。 
6.查看物理卷信息使用 pvdisplay 命令。 
7.将新增加的分区 /dev/sda3 加入到根目录分区centos中:使用 vgextend centos /dev/sda3 命令。 
8.查看卷组信息，使用 vgdisplay 命令。 
9.增加centos大小，增加100G。 使用 lvresize -L +100G /dev/mapper/centos-root 命令。

-L + ：表示增加多少空间，如 -L +15G ，单位有bBsSkKmMgGtTpPeE
-l +100%FREE	：表示增加vg的全部可用空间