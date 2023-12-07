#!/bin/bash

set -e

riscv_toolchain=$1
riscv_bin=${riscv_toolchain}/bin
riscv_lib=${riscv_toolchain}/riscv32-unknown-elf/lib
riscv_lib2=${riscv_toolchain}/lib/gcc/riscv32-unknown-elf/13.2.0
sources=$2
dist=$3

${riscv_bin}/riscv32-unknown-elf-gcc -o "${dist}/test.o" -c ${sources} -O2 -march=rv32i -mabi=ilp32 >/dev/null 2>/dev/null
${riscv_bin}/riscv32-unknown-elf-ld -T memory.ld rom.o "${dist}/test.o" -L ${riscv_lib} -L ${riscv_lib2} -lc -lgcc -lm -lnosys -o "${dist}/test.om" >/dev/null 2>/dev/null
${riscv_bin}/riscv32-unknown-elf-objcopy -O verilog "${dist}/test.om" "${dist}/test.data" >/dev/null
${riscv_bin}/riscv32-unknown-elf-objdump -D "${dist}/test.om" > "${dist}/test.dump"
rm "${dist}/test.om" "${dist}/test.o"
