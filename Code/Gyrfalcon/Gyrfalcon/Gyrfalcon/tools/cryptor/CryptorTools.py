#-*- coding: utf-8
__author__ = 'yuyang'

from Gyrfalcon.Globals import *
from Gyrfalcon.configure.GlobalConfigure import *
from Gyrfalcon.tools.tool.cryptor.BMCryptor import *

cryptor_types = {
    "base64":"00",
    "des":"01",
    "xxtea":"02",
    "aes":"03",
    "rsa":"04",
    "md5":"05",
}

class BMCryptorType:

    base64 = "base64"
    des = "des"
    xxtea = "xxtea"
    aes = "aes"
    rsa = "rsa"
    md5 = "md5"

    def cryptorPrefix(cryptorType):
        if cryptorType in list(cryptor_types.keys()):
            return cryptor_types[cryptorType]
        else:
            return "0"

class BMCryptorTool:

    def desBase64_B64EncodeText(b64Text):

        if len(b64Text) > 0:
            desEncodeText = BMCryptor.desEncode(BMCryptor.base64Decode(b64Text), desPassword)
            return BMCryptor.desEncodeText
        else:
            return ""

    def desBase64_B64DecodeText(b64Text):

        if len(b64Text) > 0:
            desDecodeText = BMCryptor.desDecode(BMCryptor.base64Decode(b64Text), desPassword)
            return BMCryptor.desDecodeText
        else:
            return ""

    def desBase64_TextEncodeB64(text):

        if len(text) > 0:
            desEncodeText = BMCryptor.desEncode(text, desPassword)
            return BMCryptor.base64Encode(desEncodeText)
        else:
            return ""

    def desBase64_TextDecodeB64(text):

        if len(text) > 0:
            desDecodeText = BMCryptor.desDecode(text, desPassword)
            return BMCryptor.base64Encode(desDecodeText)
        else:
            return ""

    def desBase64_B64EncodeB64(b64Text):

        if len(b64Text) > 0:
            desEncodeText = BMCryptor.desEncode(BMCryptor.base64Decode(b64Text), desPassword)
            return BMCryptor.base64Encode(desEncodeText)
        else:
            return ""

    def desBase64_B64DecodeB64(b64Text):

        if len(b64Text) > 0:
            desDecodeText = BMCryptor.desDecode(BMCryptor.base64Decode(b64Text), desPassword)
            return BMCryptor.base64Encode(desDecodeText)
        else:
            return ""

    def getB64DecryptText(text):

        if type(text) == type(b''):
            cryptor_type = str(text[:2])[2:-1]
        else:
            cryptor_type = text[:2]

        cryptor_text = text[2:]
        decryptBytes = BMCryptor.base64Decode(cryptor_text)
        if cryptor_type == cryptor_types[BMCryptorType.base64]:
            decryptBytes = BMCryptor.base64Decode(cryptor_text)
        elif cryptor_type == cryptor_types[BMCryptorType.des]:
            decryptBytes = BMCryptorTool.desBase64_B64DecodeText(cryptor_text)
        elif cryptor_type == cryptor_types[BMCryptorType.xxtea]:
            decryptBytes = BMCryptorTool.desBase64_B64DecodeText(cryptor_text)
        elif cryptor_type == cryptor_types[BMCryptorType.aes]:
            decryptBytes = BMCryptorTool.desBase64_B64DecodeText(cryptor_text)
        elif cryptor_type == cryptor_types[BMCryptorType.rsa]:
            decryptBytes = BMCryptorTool.desBase64_B64DecodeText(cryptor_text)
        elif cryptor_type == cryptor_types[BMCryptorType.md5]:
            decryptBytes = BMCryptorTool.desBase64_B64DecodeText(cryptor_text)
        else:
            decryptBytes = b''

        return bytesToString(decryptBytes)

    def getTextEncryptB64(text, cryptror_type):

        if cryptror_type not in cryptor_types.keys():
            return ""

        prefix = cryptor_types[cryptror_type]
        gflog(prefix)
        encryptBytes = b''
        if cryptror_type == BMCryptorType.base64:
            encryptBytes = bytes(prefix,"utf-8")+BMCryptor.base64Encode(text)
        elif cryptror_type == BMCryptorType.des:
            encryptBytes = bytes(prefix,"utf-8")+BMCryptorManager.desBase64_TextEncodeB64(text)
        elif cryptror_type == BMCryptorType.xxtea:
            encryptBytes = bytes(prefix,"utf-8")+BMCryptorManager.desBase64_TextEncodeB64(text)
        elif cryptror_type == BMCryptorType.aes:
            encryptBytes = bytes(prefix,"utf-8")+BMCryptorManager.desBase64_TextEncodeB64(text)
        elif cryptror_type == BMCryptorType.rsa:
            encryptBytes = bytes(prefix,"utf-8")+BMCryptorManager.desBase64_TextEncodeB64(text)
        elif cryptror_type == BMCryptorType.md5:
            encryptBytes = bytes(prefix,"utf-8")+BMCryptorManager.desBase64_TextEncodeB64(text)
        else:
            encryptBytes = b''

        return BMCryptorManager.bytesToString(encryptBytes)

    def bytesToString(bytesString):
        return bytesString.decode("utf-8")
