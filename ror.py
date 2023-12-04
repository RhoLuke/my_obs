# %%
import threading
import time


# %%
class rorDevice:
    # # Singleton pattern
    # def __new__(cls, master:bool = False):
    #     if not hasattr(cls, "instance"):
    #         cls.instance = super(rorDevice, cls).__new__(cls)
    #         cls.master = master
    #     return cls.instance

    def __init__(self, master: bool = False) -> None:
        self.event = threading.Event()
        self.master = master

        # shared attributes
        self.__class__.name = "RoR Device class"
        self.__class__.is_moving = False
        self.__class__.main_lock = threading.Lock()
        self.__class__.sensor = [False, False, False, True]
        self.__class__.state = self.__class__.sensor.index(True)
        self.__class__.master_operating = False

    def read_sensor(self):
        res = self.__class__.sensor.index(True)
        return res

    def simulate_movement(self, direction):
        if direction == "open":
            for _ in range(self.__class__.state, len(self.__class__.sensor) - 1, 1):
                if self.__class__.master_operating and not self.master:
                    print("1.Master take over, stop for slave(sim_ev).")
                    return

                self.__class__.main_lock.acquire()

                time.sleep(3)

                if self.__class__.master_operating and not self.master:
                    print("2.Master take over, stop for slave(sim_ev).")
                    return

                self.__class__.sensor.pop(self.__class__.state)
                self.__class__.sensor.insert(self.__class__.state + 1, True)

                self.__class__.state = self.read_sensor()
                print(f"Shutter State({self.master}):", self.__class__.state)

                self.__class__.main_lock.release()

        else:
            for _ in range(self.__class__.state, 0, -1):
                if self.__class__.master_operating and not self.master:
                    print("1.Master take over, stop for slave(sim_ev).")
                    return

                self.__class__.main_lock.acquire()

                time.sleep(3)

                if self.__class__.master_operating and not self.master:
                    print("2.Master take over, stop for slave(sim_ev).")
                    return

                self.__class__.sensor.pop(self.__class__.state)
                self.__class__.sensor.insert(self.__class__.state - 1, True)

                self.__class__.state = self.read_sensor()
                print(f"Shutter State({self.master}):", self.__class__.state)

                self.__class__.main_lock.release()

        return self.event.set()

    def move_roof(self, direction, thread):
        # print('Thread sim_mov alive:', thread.is_alive())
        if self.master and thread.is_alive():
            print("Master waiting until slave thread ends.")
            while thread.is_alive():
                time.sleep(0.1)

        if direction == "open":
            if self.__class__.state == 3:
                print("Shutter already open")
                return
            else:
                print("Shutter opening")

        else:
            if self.__class__.state == 0:
                print("Shutter already closed")
                return
            else:
                print("Shutter closing")

        while not self.event.is_set():
            if self.__class__.master_operating and not self.master:
                print("1.Master take over, stop for slave(move_roof).")
                return
            time.sleep(0.1)

        if self.__class__.master_operating and not self.master:
            print("2.Master take over, stop for slave(move_roof).")
            return

        print("Stop movement, current state:", self.__class__.state)
        self.event.clear()

    def start(self, direction):
        print("Current roof state:", self.__class__.state)

        if self.master:
            print("I'm the master, I take over whenever I want!")

            if self.__class__.main_lock.locked():
                self.__class__.main_lock.release()
            self.__class__.master_operating = True

        else:
            if self.__class__.main_lock.locked():
                time.sleep(1.0)
                self.start(direction, lock)

            else:
                print("Slave ready to run the method")

        thread2 = threading.Thread(
            target=self.simulate_movement, name="simulate_movement", args=(direction,)
        )
        thread1 = threading.Thread(
            target=self.move_roof,
            name="move_roof",
            kwargs={"direction": direction, "thread": thread2},
        )

        thread1.start()
        thread2.start()


ror1 = rorDevice(master=True)
ror2 = rorDevice(master=False)

lock = threading.Lock()
direction = "open"

ror2.start(direction="close")
time.sleep(8.0)
ror1.start(direction="open")


# %%
