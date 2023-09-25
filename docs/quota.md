# 获取服务器配置信息

## 接口地址

GET 'http://127.0.0.1:5000/v1/quota'

## 属性

| 参数名称 | 参数说明            | 请求类型 | 是否必须 | 数据类型 | 备注     |
| -------- | ------------------- | -------- | -------- | -------- | -------- |
| edu      | 教育场景            | body     | false    | dict     |          |
| bus      | 办公场景            | body     | false    | dict     |          |
| weight   | 权重                |          | true     | int      | 0 普教 1轻载高教/日常办公 2 重载高教/重载办公          |
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
            "cpu": "CPU: 2 * Intel 6226R 32核 主频2.9 GHz",
            "disk": [
                "HDD: 1 * 8.0TB 3.5 7.2 KR 6 Gb/PM",
                "SSD: 1 * 0.96TB NVMe PCIe",
                "SSD: 1 * 3.84TB NVMe PCIe"
            ],
            "memory": "内存: 8 * 32GB DDR4 3200",
            "netcard": [
                "网卡: 1 * 双口千兆以太网卡"
            ],
            "number": 17,
            "power_source": "高效冗余电源",
            "raid_card": "1 * RAID 0, 1, 10",
            "vendor": "安擎"
        },
        {
            "cpu": "CPU: 2 * Intel 6248R 48核 主频3.0 GHz",
            "disk": [
                "HDD: 2 * 6.0TB 3.5 7.2 KR 6 Gb/PM",
                "SSD: 1 * 0.96TB NVMe PCIe",
                "SSD: 2 * 1.92TB NVMe PCIe"
            ],
            "memory": "内存: 13 * 32GB DDR4 3200",
            "netcard": [
                "网卡: 1 * 双口千兆以太网卡"
            ],
            "number": 12,
            "power_source": "高效冗余电源",
            "raid_card": "1 * RAID 0, 1, 10",
            "vendor": "安擎"
        },
        {
            "cpu": "CPU: 2 * Intel 6226R 32核 主频2.9 GHz",
            "disk": [
                "HDD: 1 * 8.0TB 3.5 7.2 KR 6 Gb/PM",
                "SSD: 1 * 0.96TB NVMe PCIe",
                "SSD: 1 * 3.84TB NVMe PCIe"
            ],
            "memory": "内存: 11 * 32GB DDR4 3200",
            "netcard": [
                "网卡: 1 * 双口千兆以太网卡"
            ],
            "number": 17,
            "power_source": "高效冗余电源",
            "raid_card": "1 * RAID 0, 1, 10",
            "vendor": "国鑫"
        },
        {
            "cpu": "CPU: 2 * Intel 6248R 48核 主频3.0 GHz",
            "disk": [
                "HDD: 2 * 6.0TB 3.5 7.2 KR 6 Gb/PM",
                "SSD: 1 * 0.96TB NVMe PCIe",
                "SSD: 2 * 1.92TB NVMe PCIe"
            ],
            "memory": "内存: 17 * 32GB DDR4 3200",
            "netcard": [
                "网卡: 1 * 双口千兆以太网卡"
            ],
            "number": 12,
            "power_source": "高效冗余电源",
            "raid_card": "1 * RAID 0, 1, 10",
            "vendor": "国鑫"
        }
    ],
    "message": "Request successful."
}
```
