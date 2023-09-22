# 获取服务器配置信息

## 接口地址

GET 'http://127.0.0.1:5000/v1/quota'

## 属性

| 参数名称 | 参数说明            | 请求类型 | 是否必须 | 数据类型 | 备注     |
| -------- | ------------------- | -------- | -------- | -------- | -------- |
| edu      | 教育场景            | body     | false    | dict     |          |
| bus      | 办公场景            | body     | false    | dict     |          |
| weight   | 权重                |          | true     | int      |          |
| number   | 点数                |          | true     | int      |          |
| flavor   | 类型                |          | true     | dict     |          |
| vcpu     | 单个虚拟机 CPU 核数 |          | true     | int      |          |
| memory   | 单个虚拟机内存大小  |          | true     | int      | 单位：GB |
| storage  | 单个虚拟机存储大小  |          | true     | int      | 单位：GB |

## 示例

请求命令：

```console
curl --location --request GET 'http://127.0.0.1:5000/v1/quota' \
    --header 'Content-Type: application/json' \
    --data-raw '<body data here>'
```

请求参数：

```json
{
  "edu": {
    "weight": 1,
    "number": 300,
    "flavor": {
      "vcpu": 4,
      "memory": 8,
      "storage": 100
    }
  },
  "bus": {
    "weight": 1,
    "number": 100,
    "flavor": {
      "vcpu": 4,
      "memory": 8,
      "storage": 500
    }
  }
}
```

返回参数：

```json
{
    "data": [
        {
            "disk": {
                "bus_disk": {
                    "nvme_capacity_gb": 960.0,
                    "nvme_num": 1,
                    "sata_capacity_gb": 8000.0,
                    "sata_num": 1
                },
                "edu_disk": {
                    "nvme_capacity_gb": 3840.0,
                    "nvme_num": 1,
                    "sata_capacity_gb": 0,
                    "sata_num": 0
                }
            },
            "memory": {
                "mem_info": {
                    "mem_frequency": 3200,
                    "mem_version": "DDR4",
                    "size": 32,
                    "vendor": "SAMSUNG"
                },
                "number": 8
            },
            "number": 17,
            "vendor": {
                "cpu_model": "Intel 6226R",
                "max_mem": 16,
                "vendor": "安擎"
            }
        },
        ...
    ],
    "message": "Request successful."
}
```
