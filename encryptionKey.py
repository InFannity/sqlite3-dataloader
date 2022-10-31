import sys
import os

PRESERVE_BYTE_OFFSET = 0
SECRET_KEY = b'SbBr.5Hatf!Bv8DHa2yMGZ.*RvGnQkNw'

# 傳入兩組byte array逐byte作xor
# s : byte array
# t : byte array
def xor_bytes(s, t):
    return bytes([a ^ b for a, b in zip(s, t)])


# 輸入一檔案位置產生加密檔案
# input_path : input file path
# output_path : output file path
# secret_key : XOR key
def encryptionKey(input_path, output_path=None, secret_key=SECRET_KEY):
    if not os.path.exists(input_path):
        print('File %s not found!' % input_path)
        return False

    nByteKey = len(secret_key)
    if nByteKey <= 0:
        print('Invalid key!')
        return False
    # 判斷檔案大小, maxIter計算此大小為SECRET_KEY的幾倍
    fileSize = os.path.getsize(input_path)
    # 前PRESERVE_BYTE_OFFSET個bytes不加密
    maxIter = int((fileSize - PRESERVE_BYTE_OFFSET) / nByteKey)
    if maxIter <= 0:
        print('invalid file size %d' % int(fileSize))
        return False

    with open(input_path, 'rb') as f:
        data = f.read()
        encode_data = bytearray(data)
        for it in range(0, maxIter):
            startIdx = it * nByteKey + PRESERVE_BYTE_OFFSET
            endIdx = (it + 1) * nByteKey + PRESERVE_BYTE_OFFSET
            encode_data[startIdx:endIdx] = xor_bytes(data[startIdx:endIdx], secret_key)

    if output_path is None:
        target_file_name = os.path.basename(input_path)
        target_file_name = target_file_name + '.tmp'
        target_file_path = os.path.join(os.path.dirname(input_path), target_file_name)
    else:
        target_file_path = output_path
    with open(target_file_path, 'wb') as f:
        f.write(encode_data)