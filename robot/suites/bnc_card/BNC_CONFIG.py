# Naming convention:
#
# B_PINNAME_L3V3 e.g. B_REF_IN_L3V3:
# A digital I/O pin on the BBB with a maximum of 3.3V.
# With the BNC card signal conditioning board, this pin is connected on the
# 3.3V side of 3.3V to 5V level shifter with the 5V side of the level shifter
# connected to the PINNAME BNC connector
#
# P_PINNAME_L3V3 e.g. P_REF_IN_L3V3:
# A digital I/O pin on the BBB with a maximum of 3.3V.
# With the BNC card signal conditioning board, this pin is connected on the
# 3.3V side of 3.3V to 5V level shifter with the 5V side of the level shifter
# connected to the PINNAME pin header
#
# SW_PINNAME_L3V3 e.g. SW_REF_IN_L3V3:
# A digital I/O pin on the BBB with a maximum of 3.3V
# With the BNC card signal conditioning board, this pin is connected to a relay
# that controls whether a resistor is in series with the output of a BNC
# connector
# A digital high value indicates that a 300 ohm resistor is in series with the
# BNC connector
# A digital low or high impedance value indicates that there is no resistor
# in series with the BNC connector
#
# TR_PINNAME_L1V8 e.g. TR_REF_IN_L1V8:
# An analog input pin (maximum 1.8V) on the BBB
# With the BNC card signal conditioning board, this is connected to a voltage
# divider used for a termination resistance sensing circuit
#
# I2C_LINENAME e.g. I2C_BNC1_500HM_EN
# The hex value of the I2C register in the IO Expander corresponding to the
# given line name in the BNC schematic. Must be one byte in length.
# The hex value will always be a power of two, e.g. 0x10

# REF_IN:
# BNC Connector: BNC1
# Pin Header Number: 3
B_REF_IN_L3V3 = "Placeholder"
P_REF_IN_L3V3 = "Placeholder"
SW_REF_IN_L3V3 = "Placeholder"
TR_REF_IN_L1V8 = "Placeholder"
I2C_BNC1_500HM_EN = "0x01"

# REF_OUT:
# BNC Connector: BNC2
# Pin Header Number: 5
B_REF_OUT_L3V3 = "Placeholder"
P_REF_OUT_L3V3 = "Placeholder"

# TDC_OUT:
# BNC Connector: BNC3
# Pin Header Number: 7
B_TDC_OUT_L3V3 = "Placeholder"
P_TDC_OUT_L3V3 = "Placeholder"

# VETO_OUT:
# BNC Connector: BNC4
# Pin Header Number: 9
B_VETO_OUT_L3V3 = "Placeholder"
P_VETO_OUT_L3V3 = "Placeholder"
I2C_BNC4_VETO_OUT_OC = "0x80"

# SYNC_OUT:
# BNC Connector: BNC5
# Pin Header Number: 11
B_SYNC_OUT_L3V3 = "Placeholder"
P_SYNC_OUT_L3V3 = "Placeholder"

# SYNC_IN:
# BNC Connector: BNC6
# Pin Header Number: 13
B_SYNC_IN_L3V3 = "Placeholder"
P_SYNC_IN_L3V3 = "Placeholder"
SW_SYNC_IN_L3V3 = "Placeholder"
TR_SYNC_IN_L1V8 = "Placeholder"
I2C_BNC6_500HM_EN = "0x02"

# USER1_IO
# BNC Connector: BNC8
# Pin Header Numbers:
# - Output: 12
# - Input: 8
B_USER1_L3V3 = "Placeholder"
P_USER1_OUT_L3V3 = "Placeholder"
P_USER1_IN_L3V3 = "Placeholder"
SW_USER1_IN_L3V3 = "Placeholder"
TR_USER1_L1V8 = "Placeholder"
I2C_BNC8_USER1_NIN_OUT = "0x20"
I2C_BNC8_500_HM_EN = "0x04"

# USER2_IO
# BNC Connector: BNC8
# Pin Header Numbers:
# - Output: 10
# - Input: 6
B_USER2_L3V3 = "Placeholder"
P_USER2_OUT_L3V3 = "Placeholder"
P_USER2_IN_L3V3 = "Placeholder"
SW_USER2_IN_L3V3 = "Placeholder"
TR_USER2_L1V8 = "Placeholder"
I2C_BNC7_USER2_NIN_OUT = "0x40"
I2C_BNC7_500_HM_EN = "0x10"

# TDC_LED
# Pin header: 16
# Drive low to turn on the TDC (green) LED
# drive high to turn off the TDC (green) LED
P_TDC_LED_L3V3 = "Placeholder"
# P_TDC_LED_L3V3 must be low in order to turn on the red LED.
# Turning on the red LED also requires two additional commands:
# 1) i2cset 2 0x27 0x03 0xf7
# 2) i2cset 2 0x27 0x01 0x00
#
# And then to turn off:
# i2cset 2 0x27 0x03 0xff

# Enable for level shifters 1 and 2 - output low to turn on
OE_EN1_L1L2 = "Placeholder"
# Enable for level shifter 3 - output low to turn on
OE_EN2_L3 = "Placeholder"
# Direction of level shifting for level shifter 3
# output high to shift from 3.3V to 5V
# output low to shift from 5V to 3.3V
DIR_L3 = "Placeholder"

ANALOG_LOW_MAXIMUM = 0.01
ANALOG_HIGH_MINIMUM = 0.99
