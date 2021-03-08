# Naming convention:
#
# B_PINNAME_TO_EUT_L3V3 e.g. B_REF_IN_TO_EUT_L3V3:
# A digital I/O pin on the BBB with a maximum of 3.3V.
# With the BNC card signal conditioning board, this pin is connected on the
# 3.3V side of 3.3V to 5V level shifter. This is always an output on the BBB
# and connects to a BNC connector expecting an input on the BNC Card
#
# B_PINNAME_TO_BBB_L3V3 e.g. B_REF_OUT_TO_BBB_L3V3:
# A digital I/O pin on the BBB with a maximum of 3.3V.
# With the BNC card signal conditioning board, this pin is connected on the
# 3.3V side of 3.3V to 5V level shifter
# This is always an input on the BBB and connects to a BNC connector expecting
# and output on the BNC Card
#
# B_PINNAME_BI_DIR_L3V3 e.g. B_REF_OUT_TO_BBB_L3V3:
# A digital I/O pin on the BBB with a maximum of 3.3V.
# With the BNC card signal conditioning board, this pin is connected on the
# 3.3V side of 3.3V to 5V level shifter
# This can be either an input or output on the BBB and the BNC connector on the
# BNC card that it is connected to
#
# P_PINNAME_TO_BBB e.g. P_REF_IN_TO_BBB:
# A digital I/O pin on the BBB with a maximum of 3.3V.
# With the BNC card signal conditioning board, this pin is connected on the
# 3.3V side of 3.3V to 5V level shifter
# This is always an input on the BBB and an output on the BNC Card pin header
#
# P_PINNAME_TO_LD e.g. P_REF_OUT_TO_LD:
# A digital I/O pin on the BBB with a maximum of 3.3V.
# With the BNC card signal conditioning board, this pin is connected to an
# input of a line driver, and the output of that line driver is connected
# to an input on the 20 pin header
# This is always an output on the BBB and an input on the BNC Card pin header
#
# TR_PINNAME_TO_AIN e.g. TR_REF_IN_TO_AIN:
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
B_REF_IN_TO_EUT_L3V3 = "P9_27"
P_REF_IN_TO_BBB = "P8_16"
TR_REF_IN_TO_AIN = "P9_37"
I2C_BNC1_500HM_EN = "0x01"

# REF_OUT:
# BNC Connector: BNC2
# Pin Header Number: 5
B_REF_OUT_TO_BBB_L3V3 = "P9_24"
P_REF_OUT_TO_LD = "P8_17"

# TDC_OUT:
# BNC Connector: BNC3
# Pin Header Number: 7
B_TDC_OUT_TO_BBB_L3V3 = "P9_26"
P_TDC_OUT_TO_LD = "P8_9"

# VETO_OUT:
# BNC Connector: BNC4
# Pin Header Number: 9
B_VETO_OUT_TO_BBB_L3V3 = "P9_16"
P_VETO_OUT_TO_LD = "P8_19"
I2C_BNC4_VETO_OUT_OC = "0x80"

# SYNC_OUT:
# BNC Connector: BNC5
# Pin Header Number: 11
B_SYNC_OUT_TO_BBB_L3V3 = "P9_30"
P_SYNC_OUT_TO_LD = "P8_7"

# SYNC_IN:
# BNC Connector: BNC6
# Pin Header Number: 13
B_SYNC_IN_TO_EUT_L3V3 = "P9_25"
P_SYNC_IN_TO_BBB = "P8_14"
TR_SYNC_IN_TO_AIN = "P9_39"
I2C_BNC6_500HM_EN = "0x02"

# USER1_IO
# BNC Connector: BNC8
# Pin Header Numbers:
# - Output: 12
# - Input: 8
B_USER1_BI_DIR_L3V3 = "P9_11"
P_USER1_OUT_TO_LD = "P8_15"
P_USER1_IN_TO_BBB = "P8_12"
TR_USER1_TO_AIN = "P9_38"
I2C_BNC8_USER1_NIN_OUT = "0x20"
I2C_BNC8_500_HM_EN = "0x04"

# USER2_IO
# BNC Connector: BNC7
# Pin Header Numbers:
# - Output: 10
# - Input: 6
B_USER2_BI_DIR_L3V3 = "P9_13"
P_USER2_OUT_TO_LD = "P8_11"
P_USER2_IN_TO_BBB = "P8_10"
TR_USER2_TO_AIN = "P9_40"
I2C_BNC7_USER2_NIN_OUT = "0x40"
I2C_BNC7_500_HM_EN = "0x10"

# TDC_LED
# Pin header: 16
# Drive low to turn on the TDC (green) LED
# drive high to turn off the TDC (green) LED
P_TDC_LED_TO_LD = "P8_13"
# P_TDC_LED_TO_LD must be low in order to turn on the red LED.
# Turning on the red LED also requires two additional commands:
# 1) i2cset 2 0x27 0x03 0xf7
# 2) i2cset 2 0x27 0x01 0x00
# Turning off the red LED requires only one command:
# 1) i2cset 2 0x27 0x03 0xff
# Note that the RLED is active low and is pulled high by default
I2C_RLED = "0x08"

# Enable for all level shifters - output low to turn on
OE_LS = "P9_14"
# Enable for all line drivers - output low to turn on
OE_LD = "P8_26"
# Direction of level shifting for level shifter 3
# output high to shift from 3.3V to 5V
# output low to shift from 5V to 3.3V
DIR_L3 = "P9_23"

TERMINATION_RESISTOR_ENABLED_ANALOG_MAXIMUM = 0.076
TERMINATION_RESISTOR_DISABLED_ANALOG_MINIMUM = 0.623
TERMINATION_RESISTOR_DISABLED_ANALOG_MAXIMUM = 0.723

# The I2C bus to which the IO Expander is connected
I2C_IO_EXPANDER_I2CBUS = "2"

# The chip address f the IO Expander
I2C_IO_EXPANDER_CHIP_ADDRESS = "0x27"

# The data address of an 8 bit register that configures the output value for
# output pins on the IO Expander. The pins must be configured to outputs before
# being given a value
I2C_IO_EXPANDER_OUTPUT_REGISTER = "0x01"

# The data address of an 8 bit register that configures whether each IO on the
# IO Expander is an input or an output
I2C_IO_EXPANDER_CONFIG_REGISTER = "0x03"

# 5V Current sensing input to ADC
# note that this is named 5V_C_SENSE_TO_AIN on the signal conditioning
# board, but we cannot start a variable name with a number in Python
ADC_5V_C_SENSE_TO_AIN = "P9_33"
ADC_5V_C_SENSE_ANALOG_MAXIMUM = 0.800

# 3.3V Current sensing input to ADC
# note that this is named 3V3_C_SENSE_TO_AIN on the signal conditioning
# board, but we cannot start a variable name with a number in Python
ADC_3V3_C_SENSE_TO_AIN = "P9_35"
ADC_3V3_C_SENSE_ANALOG_MAXIMUM = 0.778

# 5V voltage sensing input to ADC
VDD_5V_TO_AIN = "P9_36"
VDD_5V_ANALOG_MINIMUM = 0.660
VDD_5V_ANALOG_MAXIMUM = 0.729
