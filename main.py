from time import sleep

from uilts.converter import Converter
from uilts.downloader import Downloader

downloadFile = "files/download.txt"
outputFile = "files/starrail.dict.yaml"

print("开始获取信息")
downloader = Downloader(downloadFile)
downloader.getAll()
info = {
    "name": "starrail",
    "version": "2025-04-08",
    "sort": "by_weight"
}
print(info)
print("开始转换")
converter = Converter(downloadFile, outputFile, info)
converter.generate()
