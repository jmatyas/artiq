from migen import *
import unittest

from artiq.gateware.szservo.spi2 import SPI2, SPIParams
from artiq.language.units import us, ns


AD53XX_CMD_OFFSET = 2 << 22
AD53XX_SPECIAL_OFS0 = 2 << 16

start_delay = 4

class TB(Module):
    def __init__(self, params):
        self.sclk = Signal()
        self.sdi = Signal()

        self.syncr = Signal(reset=1)
        self.ldac = Signal()

class SPISim(SPI2):
    def __init__(self):
        self.spi_p = spi_p = SPIParams(channels=2, data_width = 24, 
            clk_width = 2)

        # +3 in t_cycle is needed to delay driving SYNCR line low - it needs to be at least 20 ns wide
        # which with 8 ns of Kasli clock is 3 clock cycles. To ensure that IC accepts SYNCR, it is driven high
        # for 4 clock cycles - 32 ns
        t_cycle =  (spi_p.data_width*2*spi_p.clk_width + 1) + 3 
        self.submodules.spi_tb = TB(spi_p)
        
        self.submodules.spi = SPI2(self.spi_tb, spi_p)
        
        self.sim_start = Signal()

        cnt_done = Signal()
        cnt = Signal(max=t_cycle)
        load_cnt = Signal()
        
        assert start_delay <= 50
        start_cnt = Signal(max=50 + 1, reset = start_delay)
        start_done = Signal()
        
        self.comb += cnt_done.eq(cnt == 0), start_done.eq(start_cnt == 0)
        self.sync += [
            If(cnt_done,
                If(load_cnt,
                    cnt.eq(t_cycle - 1)
                )
            ).Else(
                cnt.eq(cnt - 1)
            ),
            If(~start_done,
                start_cnt.eq(start_cnt - 1)
            )
        ]
        self.comb += self.spi.spi_start.eq(cnt_done & start_done), load_cnt.eq(self.spi.spi_start)

    def test(self):
        dut = self.spi

        yield dut.dataSPI.eq(0xF009)
        for i in range(start_delay + 3):
            yield
        yield dut.dataSPI.eq(0xA79)

        while not (yield dut.spi_ready):
            yield
        for i in range(200):
           yield
        yield  

def main():
    spi = SPISim()
    run_simulation(spi, spi.test(), vcd_name="test_results/spi.vcd")


class SPITest(unittest.TestCase):
    def test_run(self):
        main()
    
    
if __name__ == "__main__":
    main()