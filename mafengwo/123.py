def main():
    ab = 'http://www.mafengwo.cn/travel-scenic-spot/mafengwo/10065.html'
    a = [i for i in ab.split('/')][-1]
    b = a.split('.')[0]
    print(b)

if __name__ == '__main__':
    main()