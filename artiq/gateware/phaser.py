from migen.build.generic_platform import *


fmc_adapter_io = [
    ("ad9154_spi", 0,
        # AD9154 should give control of SPI to FMC when USB cable is unplugged,
        # It's the case, but the PIC18F24J50 is introducing noise on SPI SCK
        # (???) To workaround that, add 2 jumpers:
        # - on XP1, between pin 5 and 6 (will keep the PIC in reset)
        # - on JP3 (will force output enable on FXLA108)
        Subsignal("clk", Pins("HPC:LA03_P")),
        Subsignal("cs_n", Pins("HPC:LA04_N", "HPC:LA05_P")),
        Subsignal("mosi", Pins("HPC:LA03_N")),
        Subsignal("miso", Pins("HPC:LA04_P")),
        Subsignal("en", Pins("HPC:LA05_N")),
        IOStandard("LVTTL"),
    ),
    ("ad9154_txen", 0, Pins("HPC:LA07_P"), IOStandard("LVTTL")),
    ("ad9154_txen", 1, Pins("HPC:LA07_N"), IOStandard("LVTTL")),
    ("ad9154_refclk", 0,
        Subsignal("p", Pins("HPC:GBTCLK0_M2C_P")),
        Subsignal("n", Pins("HPC:GBTCLK0_M2C_N")),
    ),
    ("ad9154_sysref", 0,
        Subsignal("p", Pins("HPC:LA00_CC_P")),
        Subsignal("n", Pins("HPC:LA00_CC_N")),
        IOStandard("LVDS_25"),
    ),
    ("ad9154_sync", 0,
        Subsignal("p", Pins("HPC:LA01_CC_P")),
        Subsignal("n", Pins("HPC:LA01_CC_N")),
        IOStandard("LVDS_25"),
    ),
    ("ad9154_sync", 1,
        Subsignal("p", Pins("HPC:LA02_P")),
        Subsignal("n", Pins("HPC:LA02_N")),
        IOStandard("LVDS_25"),
    ),
    ("ad9154_jesd", 0, # AD9154's SERIND7
        Subsignal("txp", Pins("HPC:DP0_C2M_P")),
        Subsignal("txn", Pins("HPC:DP0_C2M_N"))
    ),
    ("ad9154_jesd", 1, # AD9154's SERIND6
        Subsignal("txp", Pins("HPC:DP1_C2M_P")),
        Subsignal("txn", Pins("HPC:DP1_C2M_N"))
    ),
    ("ad9154_jesd", 2, # AD9154's SERIND5
        Subsignal("txp", Pins("HPC:DP2_C2M_P")),
        Subsignal("txn", Pins("HPC:DP2_C2M_N"))
    ),
    ("ad9154_jesd", 3, # AD9154's SERIND4
        Subsignal("txp", Pins("HPC:DP3_C2M_P")),
        Subsignal("txn", Pins("HPC:DP3_C2M_N"))
    ),
    ("ad9154_jesd", 4, # AD9154's SERIND2
        Subsignal("txp", Pins("HPC:DP4_C2M_P")),
        Subsignal("txn", Pins("HPC:DP4_C2M_N"))
    ),
    ("ad9154_jesd", 5, # AD9154's SERIND0
        Subsignal("txp", Pins("HPC:DP5_C2M_P")),
        Subsignal("txn", Pins("HPC:DP5_C2M_N"))
    ),
    ("ad9154_jesd", 6, # AD9154's SERIND1
        Subsignal("txp", Pins("HPC:DP6_C2M_P")),
        Subsignal("txn", Pins("HPC:DP6_C2M_N"))
    ),
    ("ad9154_jesd", 7, # AD9154's SERIND3
        Subsignal("txp", Pins("HPC:DP7_C2M_P")),
        Subsignal("txn", Pins("HPC:DP7_C2M_N"))
    ),
]
