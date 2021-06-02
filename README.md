# ceph_pressure_test
> **本工具为C/S架构模式，由Client端向Server端发送fio压测请求，Server端生成相关的压测事务，并在各个节点执行，执行完毕返回压测报告。**

# 历史

```tex
# 2017-12
 	支持多虚拟机磁盘压测
# 2018-8
	支持rbd块测试
# 2019-9
	支持自动分析
```

# 依赖：

- Server端需要安装dsh库，本库主要用来做批量处理，在项目目录base_lib中附带。

```bash
# dsh 库手动编译步骤
wget http://www.netfort.gr.jp/~dancer/software/downloads/libdshconfig-0.20.9.tar.gz
tar zxvf libdshconfig-0.20.9.tar.gz
cd libdshconfig-0.20.9
./configure
make && make install

wget http://www.netfort.gr.jp/~dancer/software/downloads/dsh-0.25.9.tar.gz
tar zxvf dsh-0.25.9.tar.gz
cd dsh-0.25.9
./configure --prefix=/usr/
make && make install
ln -s /usr/local/lib/libdshconfig.so.1 /lib64/
```

- 自动分析依赖python xlwt, chartdir库。
- 每个【虚拟机】或者【rbd client】上需要支持fio，请自行编译安装。目前作者使用的是fio-3.2。 自行下载源码安装，注意fio版本须在3.2及以上。若使用fio.img创建的虚拟机，则无需安装fio 。

- 请配置Server端到各个【虚拟机】或者【rbd client】之间的ssh无密码访问。

# #使用说明：

## #压测工具服务端【Server】：

### 服务端请执行
```python
 python CephPressureTestServer.py
```

### 功能：

- Server端为接收Client发送的压测任务，并根据计划安排相关数量的【虚拟机】或者【rbd client】跑fio命令；
- 当一次压测任务执行完毕之后，Server会收集每个【虚拟机】或者【rbd client】上的fio结果；

### 配置说明：

Server运行配置在 PressureTest.json 中【server】域

```json
"Server": {
	"ListenIP": "127.0.0.1", # 服务端监听IP  
    "ListenPORT": 7706,      # 服务端监听端口  
    "RbdPool": "rbd",        # 若为RBD块测试，请在此配置相关的pool，虚拟机测试请忽略此参数  
    "EveryRbdTestVolumeSize": 10240, # 若为RBD块测试，此参数配置每个RBD块大小（单位M），虚拟机测试请                                      # 忽略此参数
    "OneNodeRbdClients": 1,   #  若为RBD块测试，此参数配置每个【rbd client】上跑的fio数量，虚拟机测								#  试请忽略参数
    "PutEveryClientFioResultFileTo": "./client/", # 每个【虚拟机】或者【rbd client】上fio运行结                                                   # 果被Server回收后放的位置
    "AnalysisFioResult": true  #  扩展参数，暂时无用，请忽略 
  }
```

## #压测工具客户端【Client】：        

### 客户端请执行 
```python
python CephPressureTestClient.py
```

#### 功能：

- Client端运行后会向Server端发送压测任务;
- 收集Ceph集群IO数据，若非Ceph存储而进行的虚拟机测试，请配置不收集）
- 从Server端获取压测结果（fio执行的结果）
- 分析测试结果

### 配置说明：

配置文件为PressureTest.json中【Client】域

```json
  "Client": {
    "PressureTestServer": "127.0.0.1",   # Server 地址
    "PressureTestPort": 7706,    # Server 端口  
    "FioEngine": "libaio",     # 压测引擎，若为【虚拟机】测试则选libaio，若为RBD测试则选rbd  
    "IsCephPressTest": 0,     # 是否是Ceph压测，第三方存储压测(或无法获取ceph集群数据)，请配置0  
    "CephIO": "ceph -w",     # Ceph IO收集是ceph -w(Luminuous之前用法)还是 ceph -s(Luminous及之后的版本)
    "PutCephIoResultFileTo": "./ceph/",  # Ceph IO数据收集后所放的位置
    "AnalysisCephResult": true,          # 是否需要分析压测结果  
    "ClientList": [    # 将执行fio命令的【虚拟机】或者【rbd client】 
                      # 请注意需要配置Server端到ClientList中对象的SSH无密码访问                 
      "sm1",  # 主机名或者IP
      "sm2",
      "sm3",
      "sm4",
      "sm5",
      "sm6",
      "sm7",
      "sm8"
    ],
    "ClientPressTestTarget": [  # 【虚拟机】压测时，每台虚拟上被压测的设备，请于上面虚机一一对应，RBD                                 # 压测请忽略此选项
      "vdb",
      "vdb",
      "vdb",
      "vdc",
      "vdb",
      "vdb",
      "vdb",
      "vdb"
    ],

    "FioPlan": [  # 压测计划（任务），此处可以根据自己的需要添加
      {
        "rw_type": "randrw", # 读写类型{randrw：随机读写，randwrite：随机写，randread：随机读,
                             #          write: 顺序写，read：顺序读，readwrite(rw)：顺序读写}
        "run_time": 600,     # 测试时间，单位秒 
        "block_size": "4k",  # 压测块大小  
        "total_size": "30G", # 总压测的数据量(单个fio所读写的总量)  
        "numjobs": 16,       # 线程数量  
        "iodepth": 16,       # io深度  
        "client_nums": 8     # 此次计划所选择的【虚拟机】或者【rbd client】数量
      },
      {
        "rw_type": "readwrite", # 读写类型
        "run_time": 600,        # 测试时间，单位秒
        "block_size": "512k",   # 压测块大小  
        "total_size": "100G",   # 总压测的数据量(单个fio所读写的总量)
        "numjobs": 16,          # 线程数量  
        "iodepth": 16,          # io深度  
        "client_nums": 8        # 此次计划所选择的【虚拟机】或者【rbd client】数量
      }
    ]
```
