#encoding=utf-8
# 基于python3
import math
import os

# 用:分割数据
def FenGe(data,fuhao):
    try:
        right= data.split(fuhao)[1]
        left = data.split(fuhao)[0]
        return (left,right)
    except Exception as e:
        print ("FenGe函数报错：",e)
        input("程序运行失败，按任意键退出")

# 用=分割数据
def FenGe2(data2):
    global KeyLeft, KeyCenter
    try:
        data2 = data2.strip()
        if "Hz=" in data2:
            KeyLeft = data2.split("Hz=")[0].replace(",","")
            KeyCenter = "Hz"
        elif "V=" in data2:
            KeyLeft = data2.split("V=")[0].replace(",","")
            KeyCenter = "V"
        elif "Dist=" in data2:
            KeyLeft = data2.split("Dist=")[0].replace(",","")
            KeyCenter = "Dist"
        KeyRight = data2.split("=")[1]
        return (KeyLeft,KeyCenter,KeyRight)
    except Exception as e:
        print ("FenGe2函数报错：",e)
        input("程序运行失败，按任意键退出")

def zhuanhua(data3,dist):
    """
    1、小数按照公式进行换算，角度->弧度
    举例：89.0408199 公式：Π/180*(89+4/60+8.199/3600)
    2、计算sin值
    dist*sin(Π/180*(89+4/60+8.199/3600))
    """
    try:
        z = data3.split(".")[0]
        y = data3.split(".")[1]
        resu = float(z) + float(y[0:2])/60+float(y[2:4]+"."+y[4:len(y)+1])/3600
        # 结果截取小数点后前6位，符合四舍五入
        # resu2 = '%.6f' % float(float(dist)*math.sin(math.pi/180*resu))
        resu2 = float(float(dist) * math.sin(math.pi / 180 * resu))
        return (resu2)
    except Exception as e:
        print ("zhuanhua函数报错：",e)
        input("程序运行失败，按任意键退出哈哈哈")

def TestMain(path):
    file = open(path, 'r')
    filename = os.path.basename(path).split(".")[0]
    repath = os.path.split(path)[0]+"/" + filename + ".msm"
    resultfile = open(repath, 'w+')
    resultfile.write("<<")
    resultfile.write("\n")
    resultfile.write("\n")
    resultfile.write("<<")
    resultfile.write("\n")
    dic = ""
    for a in file.readlines():
        a = a.replace("\t", "").replace("\n", "*").lstrip("*")
        dic = dic + a
    k = dic.lstrip("------------------------------------*").rstrip("*------------------------------------").split(
        "*------------------------------------*")
    try:
        for i in range(0, len(k)):
            kk = ""
            # 将每个Station ID下的数据分割开来，循环每个Station ID下的数据
            ever = k[i].split("*")
            # 判断数据里面有几组Hz V Dist
            num = int((len(ever) - 1) / 3) + 1
            # 循环每组Hz V Dist
            for j in range(0, num):
                left = FenGe(ever[j], ":")[0]
                right = FenGe(ever[j], ":")[1]
                # 如果是Station ID，写入txt
                if left == "Station ID":
                    kk = right.strip()
                # 如果是Point ID，进行分割处理数据
                elif left == "Point ID":
                    (keyleft, keycenter, keyright) = FenGe2(right)
                    # 循环遍历，找到第一组Hz这行数据对应的V和Dist
                    for p in range(num, len(ever)):
                        right1 = ever[p].split(":")[1]
                        (keyleft1, keycenter1, keyright1) = FenGe2(right1)
                        if keyleft == keyleft1 and keycenter1[-1] == "V":
                            V = keyright1
                        elif keyleft == keyleft1 and keycenter1[-4:] == "Dist":
                            dist = keyright1
                    # 调用zhuanhua()函数，将v和dist做相应的计算
                    sinnum = zhuanhua(V, dist)
                    if j == 1:
                        result1 = kk + " " + keyleft + " " + "c0" + " " + keyright
                    else:
                        result1 = "        " + keyleft + " " + "c0" + " " + keyright
                    result2 = "        " + keyleft + " " + "d0" + " " + str(sinnum)
                    resultfile.write(result1)
                    resultfile.write("\n")
                    resultfile.write(result2)
                    resultfile.write("\n")
            resultfile.write("\n")
        print("数据处理完成，处理后的文件位置：%s 下的 %s.msm文件" % (os.path.split(path)[0],filename))
        resultfile.close()
        input("程序运行成功，按任意键退出")
    except Exception as e:
        print ("TestMain函数运行报错：",e)
        input("程序运行失败，按任意键退出")

if __name__ == '__main__':
    path = input("请输入文件路径（格式：L:/top/2C200901.txt）或者拖动文件到cmd窗口：")
    TestMain(path)
