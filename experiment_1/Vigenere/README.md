# __Vigenere密码__
---
> 维吉尼亚密码（又译维热纳尔密码）是使用一系列凯撒密码组成密码字母表的加密算法，属于多表密码的一种简单形式。

这里使用python进行编写
[维吉尼亚密码在线解密](https://www.kidclark.com/vigener/)
### __模块使用方法__
下载本模块到本地，解压为``Vigenere``文件夹
在文件夹所在目录下进行代码编写

```python
from .Vigenere import vigenere
```

使用上面的指令导入该模块

### __加解 & 解密（有密钥）__

#### __创建对象__

```python
t = vigenere.vigenere(key)
```

使用``vigenere.vigenere(key)``建立``vigenere``对象

+ 注: ``key``的类型为``list``，如
```python
key = [4, 7, 2, 3]
```

####__加密 & 解密__

```python
ciphertext = t.encode(plaintext)
```

使用``encode``方法进行加密，返回值为字符串``str``类型

```python
plaintext = t.decode(ciphertext)
```

使用``decode``方法进行解密，返回值为字符串``str``类型

### __解密（无密钥）__

```python
t = vigenere.vigenere(key=‘’)
```

当``key=‘’``时，转变为使用无密钥解密方法

```python
t.try_to_decode(ciphertext)
```
使用``try_to_decode``方法进行无密钥解密

### __其他__

```python
vigenere.test()
```

运行模块中原有的一组测试

```python
vigenere.display(str, number=50)
```

输出明文或者密文，默认按照每行50个字符输出