from typing import Union
from xxhash import xxh32_intdigest
import base64
import os
import logging
from zipfile import ZipFile

# set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# set up constants
BA_JP_TABLE_BUNDLES_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_table')
BA_JP_TABLE_BUNDLES_EXTRACETED_DIR = os.path.join(os.path.dirname(__file__), 'ba_jp_table_extracted')

# create directories
os.makedirs(BA_JP_TABLE_BUNDLES_DIR, exist_ok=True)
os.makedirs(BA_JP_TABLE_BUNDLES_EXTRACETED_DIR, exist_ok=True)

# https://github.com/K0lb3/Blue-Archive---Asset-Downloader/blob/main/lib/MersenneTwister.py start
# from _typeshed import Self
from typing import List
import time
from math import floor

double = float

_int = int


class uint(_int):
    def __new__(cls, value):
        return value & 0xFFFFFFFF


class MersenneTwister:
    # Class MersenneTwister generates random numbers
    # from a uniform distribution using the Mersenne
    # Twister algorithm.
    N: int = 624
    M: int = 397
    MATRIX_A: uint = 0x9908B0DF
    UPPER_MASK: uint = 0x80000000
    LOWER_MASK: uint = 0x7FFFFFFF
    MAX_RAND_INT: int = 0x7FFFFFFF
    mag01: List[uint] = [0x0, MATRIX_A]
    mt: List[uint] = [0] * N
    mti: int = N + 1

    def __init__(self, seed: int = None) -> None:
        if seed == None:
            seed = time.timens()
        self.init_genrand(uint(seed))

    # public MersenneTwister(int[] init)
    # {
    #     uint[] initArray = new uint[init.Length];
    #     for (int i = 0; i < init.Length; ++i)
    #         initArray[i] = (uint)init[i];
    #     init_by_array(initArray, (uint)initArray.Length);
    # }
    MaxRandomInt: int = 0x7FFFFFFF

    def Next(self, minValue: int = None, maxValue: int = None) -> int:
        if minValue == None:
            if maxValue == None:
                return self.genrand_int31()
            minValue = 0

        if minValue > maxValue:
            minValue, maxValue = maxValue, minValue
        return int(floor((maxValue - minValue + 1) * self.genrand_real1() + minValue))

    def NextFloat(self, includeOne: bool = False) -> float:
        if includeOne:
            return float(self.genrand_real1())
        return float(self.genrand_real2())

    def NextFloatPositive(self) -> float:
        return float(self.genrand_real3())

    def NextDouble(self, includeOne: bool = False) -> double:
        if includeOne:
            return self.genrand_real(1)
        return self.genrand_real2()

    def NextDoublePositive(self) -> double:
        return self.genrand_real3()

    def Next53BitRes(self):
        return self.genrand_res53()

    def NextBytes(self, length: int) -> bytes:
        return b"".join(
            self.genrand_int31().to_bytes(4, "little", signed=False)
            for _ in range(0, length, 4)
        )[:length]

    # public void Initialize()
    # { init_genrand((uint)DateTime.Now.Millisecond); }
    # public void Initialize(int seed)
    # { init_genrand((uint)seed); }
    # public void Initialize(int[] init)
    # {
    #     uint[] initArray = new uint[init.Length];
    #     for (int i = 0; i < init.Length; ++i)
    #         initArray[i] = (uint)init[i];
    #     init_by_array(initArray, (uint)initArray.Length);
    # }
    def init_genrand(self, s: uint) -> None:
        self.mt[0] = s & 0xFFFFFFFF
        for mti in range(1, self.N):
            self.mt[mti] = (
                uint(1812433253 * (self.mt[mti - 1] ^ (self.mt[mti - 1] >> 30)) + mti)
                & 0xFFFFFFFF
            )
        self.mti = self.N

    # private void init_by_array(uint[] init_key, uint key_length)
    # {
    #     int i, j, k;
    #     init_genrand(19650218U);
    #     i = 1; j = 0;
    #     k = (int)(N > key_length ? N : key_length);
    #     for (; k > 0; k--)
    #     {
    #         mt[i] = (uint)((uint)(mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) * 1664525U)) + init_key[j] + j);
    #         mt[i] &= 0xffffffffU;
    #         i++; j++;
    #         if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
    #         if (j >= key_length) j = 0;
    #     }
    #     for (k = N - 1; k > 0; k--)
    #     {
    #         mt[i] = (uint)((uint)(mt[i] ^ ((mt[i - 1] ^ (mt[i - 1] >> 30)) *
    #         1566083941U)) - i);
    #         mt[i] &= 0xffffffffU;
    #         i++;
    #         if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
    #     }
    #     mt[0] = 0x80000000U;
    # }

    def genrand_int32(self) -> uint:
        y: uint
        if self.mti >= self.N:
            kk: int
            if self.mti == self.N + 1:
                self.init_genrand(5489)
            for kk in range(self.N - self.M):
                y = uint(
                    (self.mt[kk] & self.UPPER_MASK)
                    | (self.mt[kk + 1] & self.LOWER_MASK)
                )
                self.mt[kk] = uint(
                    self.mt[kk + self.M] ^ (y >> 1) ^ self.mag01[y & 0x1]
                )
            for kk in range(self.N - self.M, self.N - 1):
                y = uint(
                    (self.mt[kk] & self.UPPER_MASK)
                    | (self.mt[kk + 1] & self.LOWER_MASK)
                )
                self.mt[kk] = uint(
                    self.mt[kk + (self.M - self.N)] ^ (y >> 1) ^ self.mag01[y & 0x1]
                )

            y = uint(
                (self.mt[self.N - 1] & self.UPPER_MASK) | (self.mt[0] & self.LOWER_MASK)
            )
            self.mt[self.N - 1] = uint(
                self.mt[self.M - 1] ^ (y >> 1) ^ self.mag01[y & 0x1]
            )
            self.mti = 0

        y = self.mt[self.mti]
        self.mti += 1
        y = uint(y ^ (y >> 11))
        y = uint(y ^ ((y << 7) & 0x9D2C5680))
        y = uint(y ^ ((y << 15) & 0xEFC60000))
        y = uint(y ^ (y >> 18))
        return y

    def genrand_int31(self) -> int:
        return int(self.genrand_int32() >> 1)

    def genrand_real1(self) -> double:
        return self.genrand_int32() * (1.0 / 4294967295.0)

    def genrand_real2(self) -> double:
        return self.genrand_int32() * (1.0 / 4294967296.0)

    def genrand_real3(self) -> double:
        return (double(self.genrand_int32()) + 0.5) * (1.0 / 4294967296.0)

    def genrand_res53(self):
        a = uint(self.genrand_int32() >> 5)
        b = uint(self.genrand_int32() >> 6)
        return (a * 67108864.0 + b) * (1.0 / 9007199254740992.0)

# https://github.com/K0lb3/Blue-Archive---Asset-Downloader/blob/main/lib/MersenneTwister.py ends here

# sub_1EAEFF0: 
# // Dll : BlueArchive.dll
# // Namespace: 
# public static class TableService
# {
# 	// Fields
# 	...
# 	// RVA: 0x1eaeff0 VA: 0x7386082ff0
# 	public static String CreatePassword(String key, Int32 length) { }
# 	...
# }

# __int64 __fastcall sub_1EAEFF0(__int64 a1, int a2)
# {
#   unsigned int v4; // w21
#   __int64 v5; // x0
#   __int64 v6; // x20
#   __int64 v7; // x19
#   // maybe il2cpp or class initialization?
#   if ( (byte_6C3585C & 1) == 0 )
#   {
#     sub_13FE2F8(&off_69E4C70);
#     sub_13FE2F8(&off_69E5678);
#     sub_13FE2F8(&qword_69EA2B8);
#     sub_13FE2F8(&qword_6A93330);
#     byte_6C3585C = 1;
#   }
#   if ( (a2 & 3) != 0 )
#   {
#     if ( !*((_DWORD *)off_69E5678 + 56) )
#       j_il2cpp_runtime_class_init_0(off_69E5678);
#     sub_4B68D5C(qword_6A93330, 0LL);
#   }
#   // xxhash class method: XXHashService.CalculateHash
#   v4 = sub_1A04860(a1);
#   // maybe mt class initializer?
#   v5 = sub_13FE3FC(qword_69EA2B8);
#   if ( !v5 )
#     sub_13FE40C(0LL);
#   v6 = v5;
#   // mt class constructor
#   sub_1A10CC4(v5, v4);
#   // mt class method: MersenneTwister.NextBytes
#   v7 = sub_1A111B0(v6, (unsigned int)(3 * a2 / 4), 0LL);
#   if ( !*((_DWORD *)off_69E4C70 + 56) )
#     j_il2cpp_runtime_class_init_0(off_69E4C70);
#   // base64 encode
#   return sub_42E6288(v7, 0LL);
# }


# sub_1A04860: 
# // Dll : BlueArchive.dll
# // Namespace: MX.Core.Services
# public static class XXHashService
# {
#     // Fields

#     // Properties

#     // Methods
#     // RVA: 0x1a04860 VA: 0x7385bd8860
#     public static UInt32 CalculateHash(String name) { }
#     // RVA: 0x1a04924 VA: 0x7385bd8924
#     public static UInt64 CalculateHash64(String name) { }
#     // RVA: 0x1a048ac VA: 0x7385bd88ac
#     public static UInt32 CalculateHash(Byte[] bytes) { }
#     // RVA: 0x1a04970 VA: 0x7385bd8970
#     private static UInt64 CalculateHash64(Byte[] bytes) { }
# }

# sub_1A10CC4, sub_1A111B0: 
# // Dll : BlueArchive.dll
# // Namespace: MX.Core.Math
# public class MersenneTwister
# {
#     ...
#     // RVA: 0x1a10cc4 VA: 0x7385be4cc4
#     public Void .ctor(Int32 seed) { }
#     ...
#     // RVA: 0x1a111b0 VA: 0x7385be51b0
#     public Byte[] NextBytes(Int32 lenght) { }
#     ...
# }

# sub_42E6288: 

# // Dll : mscorlib.dll
# // Namespace: System
# public static class Convert
# {
#     ...
#     // RVA: 0x42e6288 VA: 0x73884ba288
#     public static String ToBase64String(Byte[] inArray) { }
# }

def sub_1EAEFF0(name: Union[bytes, str], length: int) -> bytes:
    if isinstance(name, str):
        name = name.encode("utf8")
    seed = xxh32_intdigest(name, 0)
    mersenne_twister = MersenneTwister(seed=seed)
    tmp = mersenne_twister.NextBytes(int(3*20/4))
    return base64.b64encode(tmp)
    

# v8 = sub_1EAEFF0(a2, 20);
def calc_ba_jp_table_bundle_password(filename: str) -> bytes:
    return sub_1EAEFF0(filename, 20)


def unzip_all_table_bundles(source_folder : str, destination_folder : str):
    # iterate over all files in source folder
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            # generate file_path
            file_path = os.path.join(root, file_name)
            logging.info(f'Loading from {file_path}')
            table_bundle_zipfile = ZipFile(file=file_path)
            table_bundle_zipfile.setpassword(calc_ba_jp_table_bundle_password(file_name))
            # create dir and extract table bundle
            table_dir_dst = os.path.join(destination_folder, file_name.split('.')[0])
            os.makedirs(table_dir_dst, exist_ok=True)
            for name in table_bundle_zipfile.namelist():
                logging.info(f'Reading {name} from {file_path}')
                data = table_bundle_zipfile.read(name)
                # write to file
                fp = os.path.join(table_dir_dst, name)
                logging.info(f'Extracting {name} to {table_dir_dst}')
                with open(fp, "wb") as f:
                    f.write(data)
                logging.info(f'Extracted {name} to {fp}')
                


unzip_all_table_bundles(BA_JP_TABLE_BUNDLES_DIR, BA_JP_TABLE_BUNDLES_EXTRACETED_DIR)