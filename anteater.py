#!/usr/bin/python3
# @Мартин.
import re,time,json,sys,textwrap,argparse,os
from loguru import logger
version = "@Мартин. Anteater V1.0.0"
title = '''
************************************************************************************
<免责声明>:本工具仅供学习实验使用,请勿用于非法用途,否则自行承担相应的法律责任
<Disclaimer>:This tool is onl y for learning and experiment. Do not use it for illegal purposes, 
or you will bear corresponding legal responsibilities
************************************************************************************'''
logo = f'''                                                                    
    _      _   _     _____  U _____ u    _       _____  U _____ u   ____     
U  /"\  u | \ |"|   |_ " _| \| ___"|/U  /"\  u  |_ " _| \| ___"|/U |  _"\ u  
 \/ _ \/ <|  \| |>    | |    |  _|"   \/ _ \/     | |    |  _|"   \| |_) |/  
 / ___ \ U| |\  |u   /| |\   | |___   / ___ \    /| |\   | |___    |  _ <    
/_/   \_\ |_| \_|   u |_|U   |_____| /_/   \_\  u |_|U   |_____|   |_| \_\   
 \\    >> ||   \\,-._// \\_  <<   >>  \\    >>  _// \\_  <<   >>   //   \\_  
(__)  (__)(_")  (_/(__) (__)(__) (__)(__)  (__)(__) (__)(__) (__) (__)  (__) 
                Github==>https://github.com/MartinxMax
                                                {version}'''

def init_loger():
    logger.remove()
    logger.add(
        sink=sys.stdout,
        format="<green>[{time:HH:mm:ss}]</green><level>[{level}]</level> -> <level>{message}</level>",
        level="INFO"
    )

class Main():

    def __init__(self, args):
        self.__TIME = str(time.time())
        self.__RELIST = [
            r'[1-9]\d{5}[1-9]\d{3}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])\d{3}[\dX]$',
            r'1[3456789]\d{9}$',
            r'(http|https):\/\/([\w_-]+(?:(?:\.|\:)\w{2,})+)(?:\/[\w_\/\.]*(?:\?\S+)?)?',
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            r'((?!00)\d{1,3}|0{0,2}\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])(\.((?!00)\d{1,3}|0{0,2}\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])){3}$',
                         ]
        self.__RELISTI = ['ID Card','Phone Number','Website','Email','IP']
        if args.dir:
            if self.__check_dir(args.dir):
                for root, dirs, files in os.walk(args.dir):
                    for file in files:
                        path = os.path.join(root, file)
                        data = self.__read_files(path)
                        if data :
                            self.__check_data(path,data)
            logger.warning(f"All log information has been saved to {self.__TIME}.log")
        else:
            logger.error(f"Please use the [-d] parameter to specify the directory")

    def __check_dir(self,dir):
        return  (True if os.path.isdir(dir) else False)


    def __check_data(self,file,data):
        datas = data.split('\r\n') if '\r\n' in data else data.split('\n')
        for num,reexp in enumerate(self.__RELIST):
            for line,linesdata in enumerate(datas):
                if re.search(reexp,linesdata):
                    message = f"Path:<{file}> Content<[{linesdata.strip()}> Line:{line+1} Leakage:[{self.__RELISTI[num]}]"
                    logger.info(message)
                    self.__save_log(message)
        return False


    def __read_files(self,dir):
        try:
            with open(dir,'r',encoding='utf-8')as f:
                data = f.read()
        except:
                return False
        return data


    def __save_log(self,data):
        try:
            with open(self.__TIME+'.log','a+')as f:
                f.write(data+'\r\n')
        except:
            pass


if __name__ == '__main__':
    init_loger()
    print(logo,title)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
            Example:
                author-Github==>https://github.com/MartinxMax
            Basic usage:
                python3 {at} -d ./text # Specify the identification directory for files
                '''.format(at=sys.argv[0]
                           )))
    parser.add_argument('-d', '--dir',default="", help='Directory')
    args = parser.parse_args()
    Main(args)
