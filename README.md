# renew
通过eip找出关联的uhost和udisk，并一起续费。

一、安装
1、首先安装ucloud sdk。
  方式1（推荐）：pip install ucloud-sdk-python3 
  方式2（需要把renew放到该目录下）：
  clone https://github.com/ucloud/ucloud-sdk-python3.git
  cd ucloud-sdk-python3
  python setup.py install

二、使用
1、更新config.py文件，从UCloud控制台上找到自己的公钥、私钥和项目id等信息。
2、在main.py目录下，注释掉84行的#，注释后这样的：

	#把每个id取出来，并续费。
	for list in total_renew:
		for resourceId in list:
			print(resourceId)
			create_renew(resourceId) #

if __name__=='__main__':
	main()
  
  
注意：需要用主账号，方可执行续费权限，子账号不行。
