
x = []
numbers = [15.0, 69.9, 6.5, 22.4, 28.4, 65.9, 19.4, 198.7, 38.8, 138.2]

def mean(x):
    sum = 0
    for i in range(len(x)):
        sum += x[i]
    return sum/len(x)

print("Mean:", round(mean(numbers),2))

def sdev(x):
    sum = 0
    mn = mean(x)
    for i in range(len(x)):
        sum += (x[i]-mn)**2
        sum = round(sum,4)
        a = (sum/(len(x)-1))**(1/2)
        a = round(a,2)
    return a

print("Standard Deviation:", sdev(numbers))
