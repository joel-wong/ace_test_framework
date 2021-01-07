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
# TR_PINNAME_L1V8 e.g. TR_REF_IN_L1V8:
# An analog input pin (maximum 1.8V) on the BBB
# With the BNC card signal conditioning board, this is connected to a voltage
# divider used for a termination resistance sensing circuit
#
# I2C_LINENAME e.g. BNC1_500HM_EN
# The hex value of the I2C register in the IO Expander corresponding to the
# given line name in the BNC schematic. Must be one byte in length.
# The hex value will always be a power of two, e.g. 0x10

# REF_IN:
# BNC Connector: BNC1
# Pin Header Number: 3
B_REF_IN_L3V3 = "Placeholder"
P_REF_IN_L3V3 = "Placeholder"
TR_REF_IN_1V8 = "Placeholder"
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
TR_USER2_L1V8 = "Placeholder"
I2C_BNC7_USER2_NIN_OUT = "0x40"
I2C_BNC7_500_HM_EN = "0x10"

ANALOG_LOW_MAXIMUM = 0.01
ANALOG_HIGH_MINIMUM = 0.99
