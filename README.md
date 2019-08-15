
【用途】
通过eip找出关联的uhost和udisk，并一起续费。



【安装】

【windows】：

已封装成EXE可以直接使用，下载地址：

renew（续费）：http://duoyun.cn-bj.ufileos.com/renew.7z

check_account(对账)：http://duoyun.cn-bj.ufileos.com/check_account.7z

【linux】

1、首先安装ucloud sdk。

  方式1（推荐）：pip install ucloud-sdk-python3 
  
  方式2（需要把renew放到该目录下）：
  
  clone https://github.com/ucloud/ucloud-sdk-python3.git
  cd ucloud-sdk-python3
  python setup.py install

【如何使用】

1、打开config.ini文件，从UCloud控制台上找到自己的公钥、私钥和项目id等信息，renew 是开关，填YES则会真实续费，填其他则只打印要续费的关联id。

2、将eip填写到eip.txt文件里，每行一个。

3、对账运行check_account即可。
  
注意：需要用主账号，方可执行续费权限，子账号不行

运行结果截图：
![image](https://github.com/lious68/renew/blob/master/images/check.png)
