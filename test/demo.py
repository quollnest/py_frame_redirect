from redirect import redirect, reenter

def demo_fn(v):
    redirect()
    return v

src, x = demo_fn(5)
print(x)
v = reenter(src)
print(v)
