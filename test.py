from plugins.blueArchiveGacha import gacha

if __name__ == '__main__':
    file_object = open("./mylog.log")
    try:
        all_the_text = file_object.read()
    finally:
        file_object.close()
    print(all_the_text)