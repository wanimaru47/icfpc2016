# -*- coding: utf-8 -*-
import requests;
import json;
import time;
import copy;

def euclidean(a,b):
    if a < b:
        a,b = b,a
    while b != 0:
        if a < b:
            a,b = b,a
        a,b = b,a%b
    return a

def reduction(a):
    a1 = a.split("/")
    euc = euclidean(abs(long(a1[0])),long(a1[1]))
    a1[0] = str(long(a1[0])/euc)
    a1[1] = str(long(a1[1])/euc)
    if long(a1[1]) == 1:
        return a1[0]
    else:
        return "/".join(a1)

def nmax(a):
    maxi = None
    for b in a:
        if maxi is None:
            maxi = b
        else:
            if long(sub(maxi,b).split("/")[0]) < 0:
                maxi = b
    return maxi

def nmin(a):
    mini = None
    for b in a:
        if mini is None:
            mini = b
        else:
            if long(sub(mini,b).split("/")[0]) > 0:
                mini = b
    return mini

def add(a,b):
    a1 = a.split("/")
    b1 = b.split("/")
    if len(a1) < 2:
        a1.append("1")
    if len(b1) < 2:
        b1.append("1")
    return reduction(str((int(a1[0])*int(b1[1]) + int(b1[0])*int(a1[1]))) + "/" + str(int(a1[1])*int(b1[1])))

def sub(a,b):
    a1 = a.split("/")
    b1 = b.split("/")
    if len(a1) < 2:
        a1.append("1")
    if len(b1) < 2:
        b1.append("1")
    return reduction(str((int(a1[0])*int(b1[1]) - int(b1[0])*int(a1[1]))) + "/" + str(int(a1[1])*int(b1[1])))


def solver(spec):
    ans = ""
    try:
        lines = spec.split("\n")
        def cin():
            ret = lines[0]
            lines.pop(0)
            return ret

        x = []
        y = []

        n = cin()
        for j in range(1,int(n)+1):
            k = cin()
            for l in range(1,int(k)+1):
                coor = cin().split(",")
                x.append(coor[0])
                y.append(coor[1])
        print(x)
        x_min=nmin(x)
        x_max=nmax(x)
        diff = sub(x_max, x_min).split("/")
        if long(diff[0]) > 1 and long(diff[0]) - long(diff[1]) > 0:
            x_max = add(x_min,"1")

        y_min=nmin(y)
        y_max=nmax(y)
        diff =sub(y_max, y_min).split("/")
        if long(diff[0]) > 1 and long(diff[0]) - long(diff[1]) > 0:
            y_max = add(y_min,"1")
     
        print("x_min:" + x_min)
        print("x_max:" + x_max)
        print("y_min:" + y_min)
        print("y_max:" + y_max)

        x_size = sub(x_max, x_min)
        y_size = sub(y_max, y_min)

        remain_x = "1"
        remain_y = "1"

        xaxis = ["0"]
        while long(sub(remain_x, x_size).split("/")[0]) > 0:
            remain_x = sub(remain_x,x_size)
            x1 = sub("1",remain_x)
            if x1 not in xaxis:
                xaxis.append(x1)
        if long(sub(remain_x,x_size).split("/")[0]) == 0:
            remain_x = "0"
        xaxis.append("1")

        print(xaxis)

        yaxis = ["0"]
        while long(sub(remain_y, y_size).split("/")[0]) > 0:
            remain_y = sub(remain_y,y_size)
            y1 = sub("1",remain_y)
            if y1 not in yaxis:
                yaxis.append(y1)
        if long(sub(remain_y,y_size).split("/")[0]) == 0:
            remain_y = "0"
        yaxis.append("1")

        print(yaxis)

        print("remain_x: " + remain_x)
        print("remain_y: " + remain_y)

        # source position
        ans = str(len(xaxis)*len(yaxis)) + "\n"
        for y1 in yaxis:
            for x1 in xaxis:
                ans += str(x1) + "," + str(y1) + "\n"

        # polygon
        ans += str(int(len(xaxis)-1)*int(len(yaxis)-1)) + "\n"
        for y1 in range(0,len(yaxis)-1):
            for x1 in range(0,len(xaxis)-1):
                ans += "4 "
                ans += str(x1+y1*len(xaxis)) + " "
                ans += str(x1+y1*len(xaxis)+1) + " "
                ans += str(x1+(y1+1)*len(xaxis)+1) + " "
                ans += str(x1+(y1+1)*len(xaxis)) + "\n"
        
        # destination position
        for ky,y1 in zip(range(0,int(len(yaxis))),yaxis):
            for kx,x1 in zip(range(0,int(len(xaxis))),xaxis):

                if kx == len(xaxis)-1 and long(remain_x.split("/")[0]) != 0:
                    if len(xaxis)%2 == 0:
                        ans += remain_x
                    else:
                        ans += add(sub(x_size, remain_x),x_min)
                else:
                    if kx % 2 == 0:
                        ans += str(x_min)
                    else:
                        ans += str(x_max)
                
                ans += ","
                
                if ky == len(yaxis)-1 and long(remain_y.split("/")[0]) != 0:
                    if len(yaxis)%2 == 0:
                        ans += remain_y
                    else:
                        ans += add(sub(y_size,remain_y),y_min)
                else:
                    if ky % 2 == 0:
                        ans += str(y_min)
                    else:
                        ans += str(y_max)

                ans += "\n"
    except Exception as e:
        print(e)
    return ans


headers = {'X-API-Key':'264-49475a5b483c08577b6602f79a2aee54'}
r1 = requests.get('http://2016sv.icfpcontest.org/api/blob/2550c0c7636c177c5e50fb1e224a32c59ab404ee',headers=headers)
print(r1.status_code)
while r1.status_code != requests.codes.ok:
    time.sleep(3)
    r1 = requests.get('http://2016sv.icfpcontest.org/api/blob/2550c0c7636c177c5e50fb1e224a32c59ab404ee',headers=headers)
data1 = json.loads(r1.text)
data1['problems'].reverse()
for v in data1['problems']:
    time.sleep(3)
    print("#Problem " + str(v['problem_id']))
    r2 = requests.get('http://2016sv.icfpcontest.org/api/blob/' + v['problem_spec_hash'],headers=headers)
    print(r2.status_code)
    print(r2.text)
    while r2.status_code != requests.codes.ok:
        time.sleep(3)
        r2 = requests.get('http://2016sv.icfpcontest.org/api/blob/' + v['problem_spec_hash'],headers=headers)
    ans = solver(r2.text)
    print("")
    print("#Answer")
    print(ans)
    print()
    time.sleep(3)
    data = {
        'problem_id':v['problem_id'],
        'solution_spec':ans
    }
    r3 = requests.post('http://2016sv.icfpcontest.org/api/solution/submit',data=data,headers=headers)
    print(r3.text)
    data3 = json.loads(r3.text)
    while data3.has_key("error") and data3['error'] == "Rate limit exceeded (per-second limit).":
        time.sleep(3)
        r3 = requests.post('http://2016sv.icfpcontest.org/api/solution/submit',data=data,headers=headers)
        data3 = json.loads(r3.text)
        print(r3.text)
