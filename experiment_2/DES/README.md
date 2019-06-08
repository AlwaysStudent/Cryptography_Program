# __DES加密算法__

---

> **数据加密标准**（英语：Data Encryption Standard，缩写为 DES）是一种对称密钥加密算法，1976年被美国联邦政府的国家标准局确定为联邦资料处理标准（FIPS），随后在国际上广泛流传开来。它基于使用56位密钥的对称算法。

[在线DES加密/解密](https://www.sojson.com/encrypt_des.html "在线DES加密/解密")

### __模块使用方法__

下载本模块到本地，解压为`DES`文件夹

在文件夹所在目录下进行代码编写

```python
from DES import des
```

### __创建对象__

```python
d = des.des(key)
```

使用`des.des(key)`建立一个`des`对象

- `key`是一个由16位十六进制数组成的密钥，其中每8位中最后一位为奇偶校验位

- 你可以使用`des.create_des_key()`来随机的生成一个符合条件的`des`密钥

### __加密 & 解密__

```python
crypt_text = d.encrypt(plain_text)
```

使用`d.encrypt(plain_text)`对明文字符串`plain_text`进行加密，返回加密后的密文字符串

```python
plain_text = d.decrypt(crypt_text)
```

使用`d.decrypt(crypt_text)`对明文字符串`crypt_text`进行解密，返回解密后的明文字符串

- 明文字符串由ASCII码表中的字符组成

- 密文字符串则以十六进制的字符串形式给出




