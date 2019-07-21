# CentOS7.2安装Python3.6教程

新购买的腾讯云服务器安装的是CentOS7.2 64位系统，发现系统自带Python2.7环境，我们需要在上面安装Python3.6环境，并且不能影响自带的Python2.7环境，这里我们准备采用自己编译源码的方式进行安装。

具体步骤如下：

1. 安装好编译Python3.7解释器所需要的工具和依赖的各种库；

   ```
   yum -y groupinstall "Development tools"
   
   yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel expat-devel libffi-devel
   ```

2. 下载Python3.6解释器源码包；

   ```
   wget -c https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
   ```

3. 解压源码包；

   ```
   tar -Jxvf Python-3.7.0.tar.xz
   ```

4. 编译并安装；

   ```
   cd Python-3.7.0  # 切换到源码文件夹下
   
   ./configure --prefix=/usr/local/python3  # 配置编译安装选项（这里指定了安装路径为/usr/local/python3）
   
   make  # 编译
   
   make install  # 安装
   ```

5. 配置Python3环境；

   ```
   ln -s /usr/local/python3/bin/python3 /usr/bin/python3  # 给python3程序创建软链接
   
   ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3        # 给pip程序创建软链接
   ```

6. 大功告成，检查下是否安装配置成功。

   ```
   python3 -V  # 如果执行结果为“Python 3.7.0”，说明Python3环境已经成功安装
   ```

   