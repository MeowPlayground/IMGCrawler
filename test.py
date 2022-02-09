from threading import Thread



def b(a):
    Thread(
        target=a
    ).start()

def c(x):
    b(x)

def d():
    print("sad")

c(d)