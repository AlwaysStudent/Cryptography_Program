# __RSA加密算法__

---

> **RSA加密算法**是一种非对称加密算法，在公开密钥加密和电子商业中被广泛使用。RSA是1977年由罗纳德·李维斯特（Ron Rivest）、阿迪·萨莫尔（Adi Shamir）和伦纳德·阿德曼（Leonard Adleman）一起提出的。当时他们三人都在麻省理工学院工作。
> 
> RSA就是他们三人姓氏开头字母拼在一起组成的。

这里使用python3进行编写

[RSA加密算法维基百科](https://zh.wikipedia.org/wiki/RSA%E5%8A%A0%E5%AF%86%E6%BC%94%E7%AE%97%E6%B3%95 "RSA加密算法")

### __模块使用方法__

下载本模块到本地，解压为`RSA`文件夹

在文件夹所在目录下进行代码编写

```python
from RSA import rsa
```

#### __创建对象__

```python
r = rsa.rsa(bit_length, flag=0)
```

使用`RSA.rsa(bit_length, flag=0)`建立`rsa`对象

* `bit_length`用于生成指定长度的`p`和`q`，公钥中`n`的位数为`2 × bit_length`

* `flag`用于指定密钥由系统自动生成还是由用户自行输入
  
  `flag = 0`时，密钥由系统自动生成
  
  `flag = 1`时，密钥由用户自行输入

#### __查看公钥和密钥__

```python
n, e = r.create_public_key()
```

使用`create_public_key()`方法，返回当前`rsa`对象的公钥对，返回类型为`tuple`

```python
n, d = r.create_private_key()
```

使用`create_private_key()`方法，返回当前`rsa`对象的私钥对，返回类型为`tuple`

#### __加密 & 解密__

- __当密钥由系统自动生成时__

```python
crypt_text = r.encrypt(plain_text)
```

可直接使用`encrypt(palin_text)`的方法对明文字符串`plain_text`进行加密，返回类型为`str`

```python
plain_text = r.decrypt(crypt_text)
```

使用`decrypt(crypt_text)`的方法对密文字符串`crypt_text`进行加密，返回类型为`str`

- __当密钥由用户自行输入时__

```python
r.add_public_key(public_key)
r.add_private_key(private_key)
```

首先，需要根据加密或者解密，使用`add_public_key(public_key)`或者`add_private_key(private_key)`来添加公钥对或者私钥对

- 其中，公钥对`public_key`和私钥对`private_key`的类型均为`tuple`

之后加解密过程同上
