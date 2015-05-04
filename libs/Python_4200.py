import matplotlib.pyplot as plt
from decimal import Decimal
from time import sleep
import csv
import serial
import visa

class cap_test(object):
    """
    ---------------------------------------------------------------------------
    INPUTS: None
    ---------------------------------------------------------------------------
    Contains general methods that can be used to set up any of the three types
    of capacitance tests. Is the parent class for the more specific CV, CF, and
    CT classes defined below
    ---------------------------------------------------------------------------
    """
    test_setup = False
    instrument_setup = False
    def __init__(self, label, mode, model, speed, acv, length, dcvsoak):
        self.mode = mode
        self.label = label
        self.model = model
        self.speed = speed
        self.acv = acv
        self.length = length
        self.dcvsoak = dcvsoak

    def set_name(self, label = None):

        if type(label) == str:
            self.label = label
        else:
            while True:
                try:
                    self.label = str(input("Enter test label: "))
                    break
                except:
                    print("Enter a valid label...")

    def set_mode(self, mode = None):

        modes = ["cv", "cf", "ct"]
        if mode in modes:
            self.mode = modes.index(mode.lower())
        else:
            while True:
                try:
                    response = str(input("Choose mode (cv, ct, or cf): ")).lower()
                    if response not in modes:
                        raise ValueError
                    else:
                        self.mode = response
                        break
                except:
                    print("Please choose a valid test mode...")

    def set_model(self, model = None):

        models = ["z-theta", "r+jx", "cp-gp", "cs-rs", "cp-d", "cs-d"]
        try:
            if model in models:
                self.model = models.index(model)
            elif int(model) in range(6):
                self.model = int(model)
        except:
            while True:
                try:
                    response = input("Choose model\n0: z-theta\n1: r+jx\n2: cp-gp\n3: cs-rs\n4: cp-d\n5: cs-d\n")
                    if response in models:
                        self.model = models.index(response)
                        break
                    elif int(response) in range(6):
                        self.model = int(response)
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter a valid selection")
        self.model

    def set_speed(self, speed = None):

        if speed in range(3):
            self.speed = speed
        elif speed == 4:
            pass
        else:
            while True:
                try:
                    response = int(input("Select integration speed: "))
                    if response in range(3):
                        self.speed = response
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter a correct value: ")

    def set_acv(self, acv = None):

        if acv in range(0,101):
            self.acv = acv/1000
        else:
            while True:
                try:
                    response = int(input("Enter ac ripple in millivolts: "))
                    if response in range(0,101):
                        self.acv = response/1000
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter a valid voltage")
    
    def set_length(self, length = None):

        lengths = ["0", "1.5", "3"]
        if str(length) in lengths:
            self.length = str(length)
        else:
            while True:
                try:
                    response = input("Enter cable length: ")
                    if response in lengths:
                        self.length = response
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter valid length")

    def set_dcvsoak(self, dcvsoak=None):
        
        if dcvsoak in range(-30, 30):
            self.dcvsoak = dcvsoak
        else:
            while True:
                try:
                    response = float(input("Enter DC Soak voltage: "))
                    if response in range(-30, 30):
                        self.dcvsoak = response
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter valid voltage")

    def set_delay(self, delay=None):
        if 0 < delay < 999:
            self.delay = delay
        else:
            while True:
                try:
                    delay = float(input("Enter delay time: "))
                    if 0 < delay < 999:
                        self.delay = delay
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter valid delay")

    def set_intrument(self):
        if not self.instrument_setup:
            rm = visa.ResourceManager()
            self.instr = rm.open_resource("GPIB0::17::INSTR")
        self.instrument_setup = True


class cv_test(cap_test):
    """
    ---------------------------------------------------------------------------

    ---------------------------------------------------------------------------

    ---------------------------------------------------------------------------
    """
    wrange_set = False
    vrange_set = False
    def __init__(self, label, model=2, speed=1, acv=30, length=1.5, dcvsoak=0, delay=0, mono = None):
        self.label = label
        self.model = model
        self.speed = speed
        self.acv = acv/1000
        self.lenth = length
        self.dcvsoak = dcvsoak
        self.delay = delay
        self.mono = mono
        cap_test.__init__(self,label=label,mode="CV",model=model,speed=speed,acv=acv/1000,length=length,dcvsoak=dcvsoak)

    def step_check(self,start, end, step):

        if step > abs(end - start):
            raise ValueError
        elif (end - start < 0 and step > 0) or (end - start > 0 and step < 0):
            step = - step
            return [start, end, step]
        else:
            return [start, end, step]


    def set_vrange(self, vstart=None, vend=None, vstep=None):
        
        if (type(vstart) is float or int) and (type(vend) is float or int) and (type(vstep) is float or int):
            try:
                self.vstart, self.vend, self.vstep = self.step_check(vstart, vend, vstep)
            except:
                print("Invalid variables entered")
        else:
            while True:
                try:
                    vstart = float(input("Enter start voltage: "))
                    vend = float(input("Enter end voltage: "))
                    vstep = float(input("Enter step size: "))
                    self.vstart, self.vend, self.vstep = self.step_check(vstart, vend, vstep)
                    break
                except ValueError:
                    print("Please enter vald voltages...")
        self.vrange_set = True

    def set_wavelengths(self, wstart=None, wend=None, wstep=None):

        if type(wstart) is int and type(wend) is int and type(wstep) is int:
            try:
                self.wstart, self.wend, self.wstep = self.step_check(wstart, wend, wstep)
            except:
                print("Invalid variables entered")
        else:
            while True:
                try:
                    wstart = int(input("Enter start wavelength: "))
                    wend = int(input("Enter end wavelength: "))
                    wstep = int(input("Enter step size: "))
                    self.wstart, self.wend, self.wstep = self.step_check(wstart, wend, wstep)
                except ValueError:
                    print("Please enter vald wavelengths...")
        self.wrange_set = True

    def setup_test(self):
        self.commands = [":CVU:RESET",
                     ":CVU:MODE 1",
                     ":CVU:MODEL " + str(self.model),
                     ":CVU:SPEED " + str(self.speed),
                     ":CVU:ACV " + str(self.acv),
                     ":CVU:FREQ 1E+6",
                     ":CVU:DCV " + str(self.dcvsoak),
                     ":CVU:ACZ:RANGE 0",
                     ":CVU:CORRECT 0,0,0,",
                     ":CVU:LENGTH " + str(self.length),
                     ":CVU:SWEEP:DCV " + str(self.vstart) + "," + str(self.vend) + "," + str(self.vstep),
                     ":CVU:DELAY:SWEEP " + str(self.delay)]

        for c in self.commands:
            print(c)

    def run_test(self):
        if not self.test_setup:
            self.setup_test()

        if self.wrange_set:
            cm = setup_cm110(self.mono)
            for w in range(self.wstart, self.wend, self.wstep):
                command(cm, "goto", w)
                print(":CVU:TEST:RUN")
                sleep(.5)

        else:
            print(":CVU:TEST:RUN")



def CV_output_san(values):
    """
    ---------------------------------------------------------------------------
    FUNCTION: CV_output_san
    INPUTS: values (str)
    RETURNS: prim, sec (list float)
    DEPENDENCIES: none
    ---------------------------------------------------------------------------
    Takes data string as proudced by KXCI command :CVU:OUTPUT:Z? and returns
    two arrays of decimal numbers representing the pairs of values receieved
    ---------------------------------------------------------------------------
    """
    values = (values.replace(";", ",").split(","))
    prim = [float(Decimal(values[i])) for i in range(0, len(values), 2)]
    sec = [float(values[i]) for i in range(1, len(values), 2)]
    return prim, sec


def select_device(rm):
    """
    ---------------------------------------------------------------------------
    FUNCTION: select_device
    INPUTS: rm (visa.ResourceManager)
    RETURNS: devices[selection] (str)
    DEPENDENCIES: pyvisa/visa
    ---------------------------------------------------------------------------
    Takes a resource manager as an argument and lists available visa devices
    The user is then queried as to which device they would like to open
    ---------------------------------------------------------------------------
    """
    devices = rm.list_resources()

    print("Found the following ", len(devices), " devices")
    for i in range(len(devices)):
        print(i, ") ", devices[i])

    selection = None
    while not selection:
        try:
            selection = int(input("Please select device address: "))
        except ValueError:
            print("Invalid Number")

    return(devices[selection])


def csv_writer(prim, sec, ter, name):
    """
    ---------------------------------------------------------------------------
    FUNCTION: csv_writer
    INPUTS: prim, sec, ter (float list)
            name (str)
    RETURNS: nothing
    DEPENDENCIES: csv
    ---------------------------------------------------------------------------
    Takes three arrays of values and writes them to two columns in a csv file
    called "name". The columns have headers "X1", "Y1", and "Y2"
    ---------------------------------------------------------------------------
    """
    rows = zip(ter, prim, sec)
    try:
        with open(name + '.csv', 'w', newline='') as csvfile:
            reswrite = csv.writer(csvfile)
            reswrite.writerow(["X1", "Y1", "Y2"])
            for row in rows:
                reswrite.writerow(row)
    except:
        raise SystemExit("Could not open file to write!")


def dual_plot(x, x_label, y1, y1_label, y2, y2_label, x_min, x_max, log):
    """
    ---------------------------------------------------------------------------
    FUNCTION: dual_plot
    INPUTS: x, y1, y2 (float array)
            x_min, x_max (int)
            x_label, y1_label, y2_label (str)
            log (bool)
    RETURNS: nothing
    DEPENDENCIES: matplotlib.pyplot
    ---------------------------------------------------------------------------
    Takes three arrays of floats and their respective names. y1 and y2 are
    plotted against x over the range x_min to x_max. Setting log to true
    results in a semilogx plot whereas false is a simple linear plot.
    ---------------------------------------------------------------------------
    """
    fig, ax1 = plt.subplots()

    if log:
        ax1.semilogx(x, y1, 'b')
    else:
        ax1.plot(x, y1, 'b')

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color='b')

    for tl in ax1.get_yticklabels():
        tl.set_color('b')

    ax2 = ax1.twinx()

    if log:
        ax2.semilogx(x, y2, 'r')
    else:
        ax2.plot(x, y2, 'r')
    ax2.set_ylabel(y2_label, color='r')

    for tl in ax2.get_yticklabels():
        tl.set_color('r')

    plt.xlim([x_min, x_max])
    plt.grid(True)
    plt.show(block=False)


def test_type():
    """
    ---------------------------------------------------------------------------
    FUNCTION: test_type
    INPUTS: none
    RETURNS: t_type (int)
    DEPENDENCIES: none
    ---------------------------------------------------------------------------
    Queries the user on which test they wish to perform, selecting an incorrect
    value results in an error message and a prompt to choose again.
    ---------------------------------------------------------------------------
    """
    print("Test 0: CV sweep\n",
          "Test 1: CF sweep\n",
          "Test 2: CT sweep")

    while True:
        try:
            t_type = int(input("Please select a test: "))
            if t_type != 0 and t_type != 1 and t_type != 2:
                raise ValueError("Please enter 2, 1, or 0")
            else:
                return t_type
        except ValueError:
            print("Invalid selection")


def read_4200_x(read_command, instrument):
    """
    ---------------------------------------------------------------------------
    FUNCTION: read_4200_x
    INPUTS: read_command (str)
    RETURNS: x (float list)
    DEPENDENCIES: pyvisa/visa
    ---------------------------------------------------------------------------
    Takes an appropriate CVU read command as an argument and sends it to a
    4200-SCS. Then reads the raw returned data and formats it into an list of
    floats. Acceptable read commands are:
    :CVU:DATA:VOLT?
    :CVU:DATA:FREQ?
    :CVU:DATA:STATUS?
    :CVU:DATA:TSTAMP?
    ---------------------------------------------------------------------------
    """
    ok_commands = [':CVU:DATA:VOLT?', ':CVU:DATA:FREQ?',
                   ':CVU:DATA:STATUS?', ':CVU:DATA:TSTAMP?']
    if read_command not in ok_commands:
        raise ValueError('Incorrect read command passed')

    instrument.write(read_command)
    data = str(instrument.read_raw()).replace("b'", "").rstrip("'")
    data = data[:-5].split(",")
    x = [float(d) for d in data]
    return x

def rpm_switch(channel, mode, instrument):
    """
    ---------------------------------------------------------------------------
    FUNCTION: rpm_switch
    INPUTS: channel, mode (int)
    RETURNS: nothing
    DEPENDENCIES: pyvisa/visa
    ---------------------------------------------------------------------------
    Sends a command to the 4225 RPM modules of the 4200-SCS to set a given
    channel to a given mode (see below).
    0 = Pulsing
    1 = 2 Wire CVU
    2 = 4 Wire CVU
    3 = SMU
    ---------------------------------------------------------------------------
    """
    try:
        # run script to switch RPM1 to CVU mode
        instrument.write('EX pmuulib kxci_rpm_switch(' + str(channel) + ',' + str(mode) + ')')
        # wait for script to complete
        instrument.wait_for_srq()
        print("Configured PMU", channel)
    except:
        raise RuntimeError("Service Request timed out")

def init_4200(mode, instrument):
    """
    ---------------------------------------------------------------------------
    FUNCTION: init_4200
    INPUTS: mode, instrument (int)
    RETURNS: nothing
    DEPENDENCIES: pyvisa/visa
    ---------------------------------------------------------------------------
    Sets up the 4200-SCS to recieve measurement commands and respond correctly
    when RPM modules are attached. See function above for RPM modes.
    ---------------------------------------------------------------------------
    """
    # clear the visa resource buffers
    instrument.clear()
    # send srq when finished with task
    instrument.write('DR1')
    # access the user library page
    instrument.write('UL')
    rpm_switch(1, mode, instrument)
    rpm_switch(2, mode, instrument)
    # clear the buffer
    instrument.write('BC')

def setup_cm110(com_port):
    cm = serial.Serial(
            port=com_port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
            )
    return cm

def command(mono, operation, x=None, y=None):

    commands = {"calibrate": 18, "dec": 1, "echo": 27, "goto": 16, "inc": 7,
                "order": 51, "query": 56, "reset": 255, "scan": 12, "select": 26,
                "size": 55, "speed": 13, "step": 54, "units": 50, "zero": 52
                }

    c = commands[operation.lower()]

    if c in [51, 56, 26, 55, 50]:
        mono.write(chr(c).encode())
        mono.write(chr(x).encode())

    elif c in [18, 16, 13]:
        high, low = divmod(x, 0x100)

        mono.write(chr(c).encode())

        mono.write(chr(high).encode())
        mono.write(chr(low).encode())

    elif c in [1, 27, 7, 54, 57]:
        mono.write(chr(c).encode())

    elif c is 255:
        for i in range(3):
            mono.write(chr(255).encode())

    elif c is 12:
        s_high, s_low = divmod(x, 0x100)
        e_high, e_low = divmod(x, 0x100)

        mono.write(chr(c).encode())

        mono.write(chr(s_high).encode())
        mono.write(chr(s_low).encode())

        mono.write(chr(e_high).encode())
        mono.write(chr(e_low).encode())

# If running this library, print docstring for all functions
if __name__ == "__main__":
    
    print(CV_output_san.__doc__, '\n',
          select_device.__doc__, '\n',
          csv_writer.__doc__,    '\n',
          dual_plot.__doc__,     '\n',
          test_type.__doc__,     '\n',
          read_4200_x.__doc__,   '\n',
          rpm_switch.__doc__,    '\n',
          init_4200.__doc__,     '\n')
