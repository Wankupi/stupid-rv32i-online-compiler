PWD := $(CURDIR)

# riscv 工具链前缀
RISCV_TOOLCHAIN ?= riscv64-elf-

# compile tools
AS := $(RISCV_TOOLCHAIN)as
CC := $(RISCV_TOOLCHAIN)gcc
CXX := $(RISCV_TOOLCHAIN)g++
LD := $(RISCV_TOOLCHAIN)ld
OBJCOPY := $(RISCV_TOOLCHAIN)objcopy
OBJDUMP := $(RISCV_TOOLCHAIN)objdump

# compile options
# Link library least support: [ rv32i rv32iac rv32im rv32imac rv32imafc rv64imac rv64imafdc ] if use the given dockerfile(archlinux with riscv64-elf-newlib)
# other option such as _zicsr might be available as well
MARCH_STRING ?= rv32ic
ABI_STRING := ilp32

OPT_LEVEL ?= 2

AS_FLAGS := -march=$(MARCH_STRING)
C_FLAGS := -I . -O$(OPT_LEVEL) -march=$(MARCH_STRING) -mabi=$(ABI_STRING) -g -std=c17
CPP_FLAGS := -I . -O$(OPT_LEVEL) -march=$(MARCH_STRING) -mabi=$(ABI_STRING) -g -std=c++17
OBJCOPY_FLAGS := 

SRC_FILE ?= src/src.cpp
TARGET ?= sim

# change flags according to target
ifeq ($(TARGET), fpga)
    OBJCOPY_FLAGS += -O binary
else ifeq ($(TARGET), sim)
    OBJCOPY_FLAGS += -O verilog
    C_FLAGS += -DSIM
    CPP_FLAGS += -DSIM
else
  $(error "Unsupported target: $(TARGET)")
endif

VERSION_STRING := $(TARGET)-$(MARCH_STRING)-O$(OPT_LEVEL)

OBJ_FILE := src/$(VERSION_STRING).o
ELF_FILE := src/$(VERSION_STRING).elf
DATA_FILE := src/$(VERSION_STRING).data
DUMP_FILE := src/$(VERSION_STRING).dump

all: $(DATA_FILE) $(DUMP_FILE)

%.dump: %.elf
	$(OBJDUMP) -D $< > $@

%.data: %.elf
	$(OBJCOPY) $(OBJCOPY_FLAGS) $< $@

$(ELF_FILE): rom.o $(SRC_FILE).$(VERSION_STRING).o
	$(CC) $(C_FLAGS) -T memory.ld $^ -o $@ -nostdlib -lc -lm -lgcc -Wl,--no-warn-rwx-segments

%.c.$(VERSION_STRING).o: %.c
	$(CC) -c $< -o $@ $(C_FLAGS)

%.cpp.$(VERSION_STRING).o: %.cpp
	$(CXX) -c $< -o $@ $(CPP_FLAGS)

%.S.$(VERSION_STRING).o: %.S
	$(AS) $(AS_FLAGS) -c $< -o $@

rom.o: rom.s
	$(AS) $(AS_FLAGS) -c $< -o $@

clean:
	find -L . -type f \( -name "*.dump" -o -name "*.data" -o -name "*.elf" -o -name "*.o" \) -delete

.PHONY: all clean
