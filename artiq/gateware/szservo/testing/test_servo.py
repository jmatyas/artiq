import logging
import unittest

from math import log2, ceil


from migen import *
from migen.genlib import io

from artiq.gateware.szservo.testing import test_adc, test_dac, test_pgia
from artiq.gateware.szservo import servo

channels_no = 8

Kps = [1 for i in range(channels_no)]
Kis = [0 for i in range(channels_no)]


class ServoSim(servo.Servo):
    def __init__(self):
        adc_p = servo.ADCParams(width=16, channels=channels_no, lanes=int(channels_no/2),
                t_cnvh=4, t_conv=57 - 4, t_rtt=4 + 4)
        iir_p = servo.IIRWidths(state=25, coeff=18, adc=16, asf=14, word=16,
                accu=48, shift=11, channel=ceil(log2(adc_p.channels)), profile=1)
        self.dac_p = servo.DACParams(data_width = 24, clk_width = 2,
                channels=adc_p.channels)

        pgia_p = servo.PGIAParams(data_width = 16, clk_width = 2)
        self.submodules.adc_tb = test_adc.TB(adc_p)
        self.submodules.dac_tb = test_dac.TB(self.dac_p)

        self.submodules.pgia_tb = test_pgia.TB(pgia_p)

        servo.Servo.__init__(self, self.adc_tb, self.pgia_tb, self.dac_tb,
                adc_p, pgia_p, iir_p, self.dac_p, 0x5555, Kps, Kis)
        
                        
    def test(self):

        
        x0 = 0x0141
        x1 = 0x0743
        y1 = 0x1145
        yield from self.set_states(x0, x1, y1, 0, 0, 0)

        x3 = 0x0743
        y3 = 0x1145
        
        for i in range(1, self.dac_p.channels - 1):
            x0 = x0#+0x0020 + i*i*0x00A0
            x3 = 0x0743
            y3 = 0x1145

            yield from self.set_states(x0, x3, y3, i, i, 0)

        x0 = 0x7FFF
        yield from self.set_states(x0, x3, y3, self.dac_p.channels - 1, self.dac_p.channels - 1, 0)
        

        yield self.start.eq(1)
        yield
        while (yield self.done):
            yield
        yield
        yield
        while not (yield self.done):
            yield
        yield
        yield
        while (yield self.done):
            yield
        yield
        yield
        while not (yield self.done):
            yield
        yield
        yield


        # for i in range(1000):
        #     yield
        
    
    def set_states(self, x0, x1, y1, adc, channel, profile):
        
        yield self.adc_tb.data[-adc-1].eq(x0)
        yield from self.iir.set_state(adc, x1, coeff="x1")      # assigning x1 as a previous value of input
        yield from self.iir.set_state(channel, y1,              # assigning y1 as previous value of output
                profile=profile, coeff="y1")

    def servo_iter(self):
        while not (yield self.dac.dac_start):
            yield
        yield
        while not (yield self.done):
        # for i in range(self.dac_p.channels):
            while (yield self.dac_tb.syncr):
                    yield        
            
            while not (yield self.dac_tb.syncr):
                yield

            while not (yield self.dac.dac_ready):
                yield      
        

def main():
    servo = ServoSim()
    run_simulation(servo, servo.test(), vcd_name="test_results/servo_dac.vcd",
            clocks={
                "sys":   (8, 0),
                "adc":   (8, 0),
                "ret":   (8, 0),
                "async2": (2, 0),
            })


class ServoTest(unittest.TestCase):
    def test_run(self):
        main()


if __name__ == "__main__":
    main()
