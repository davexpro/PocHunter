# PocHunter

一个适配器模块，用于调用市面上流行的PoC框架(Beebeeto/PocSuite/TangScan/KsPoc)下的PoC。

本模块仅适用于 **Python 2.7** 

*注：基于[PocScan](https://github.com/erevus-cn/pocscan)中的动态兼容执行模块，在此特别感谢！*

## Usage

参照主目录下的hunter.py文件，按照其格式调用。

```
pl = PocLauncher()
pl.verify('http://127.0.0.1/', 'beebeeto', 'discuz_x3_0_xss.py')
pl.verify(TARGET_URL, POC_PLATFORM, POC_FILE_NAME)
```

大家也可以基于这个模块造自己的轮子，内部使用，若有建议或意见欢迎提issue！

## Folder Structure

```
PocHunter/
├── frame  框架调用适配器模块
├── lib 	   执行模块核心库(内含调用接口)
├── plugins 插件 - 其他PoC框架存放位置
│   ├── beebeeto
│   ├── data
│   ├── kspoc
│   ├── pocsuite
│   └── tangscan
└── pocs   PoC文件存放位置
    ├── beebeeto
    ├── kspoc
    ├── pocsuite
    └── tangscan

```

