import asyncio
import random as rd
import time

async def test():
    n = rd.randint(0,10)
    for i in range(n):
        d = rd.randint(0,3)
        await asyncio.sleep(3)
        print("Hello! {} {}/{}".format(d,i,n))

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(
        say_after(2, 'hello'))

    task2 = asyncio.create_task(
        say_after(1, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

if __name__ == "__main__":
    asyncio.run(main())
    print("ran test,...")
