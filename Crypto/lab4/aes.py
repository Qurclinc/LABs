import galois
from typing import List
from logger import logger

class BlockException(Exception):
    pass

class SAES:
    
    def __init__(self):
        self.BLOCK_SIZE = 4
        self.mappings = {
            k: v
            for k, v in zip(
                [str(hex(x)[2:]) for x in range(16)],
                [x for x in range(16)]
            )
        }
        
        self.inv_mapping = {
            v: k for k, v in self.mappings.items()
        }
        
        # Прямой S-Box
        self.SHB = [
            [0x9, 0xe, 0x5, 0x1],
            [0x8, 0xb, 0xd, 0xa],
            [0x6, 0x7, 0xf, 0x3],
            [0xc, 0x4, 0x0, 0x2]
        ]
        
        # Обратный S-Box
        self.INV_SHB = [
            [0xe, 0x3, 0xf, 0xb],
            [0xd, 0x2, 0x8, 0x9],
            [0x4, 0x0, 0x7, 0x5],
            [0xc, 0x6, 0x1, 0xa],
        ]
        
        self.GF16 = galois.GF(2**4, irreducible_poly=0x13)
        
    def __convert_to_block(self, line: str):
        if len(line) != self.BLOCK_SIZE:
            raise BlockException
        return [
            [self.mappings[line[0]], self.mappings[line[2]]],
            [self.mappings[line[1]], self.mappings[line[3]]]
        ]
        
    def __convert_from_block(self, block: List[List[int]]):
        return "".join([
            self.inv_mapping[block[0][0]], self.inv_mapping[block[1][0]],
            self.inv_mapping[block[0][1]], self.inv_mapping[block[1][1]]
        ])
        
    def __parse_char(self, char: str | int):
        if isinstance(char, str):
            part = bin(self.mappings[char])[2:].zfill(4)
        else:
            part = bin(char)[2:].zfill(4)
        return [
            int(part[:2], 2),
            int(part[2:], 2)
        ]
        
    def _generate_round_key(self, prev_block: List[List[int]], n: int = 2):
        p00, p01 = self.__parse_char(prev_block[1][1])
        p10, p11 = self.__parse_char(prev_block[0][1])
        k00 = self.SHB[p00][p01] ^ prev_block[0][0]
        k10 = self.SHB[p10][p11] ^ prev_block[1][0] ^ (2 ** (n - 2))
        k01 = k00 ^ prev_block[0][1]
        k11 = k10 ^ prev_block[1][1]
        return [
            [k00, k01],
            [k10, k11]
        ]
        
    def __do_xor(self, data: List[List[int]], key: List[List[int]]):
        result = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                result[i][j] = data[i][j] ^ key[i][j]
        return result
    
    def __do_mapping(self, data: List[List[int]]):
        """Прямая подстановка (SubBytes)"""
        for i in range(2):
            for j in range(2):
                char = data[i][j]
                p0, p1 = self.__parse_char(char)
                data[i][j] = self.SHB[p0][p1]
        return data
    
    def __do_inv_mapping(self, data: List[List[int]]):
        """Обратная подстановка (InvSubBytes)"""
        for i in range(2):
            for j in range(2):
                val = data[i][j]
                row = val >> 2
                col = val & 0b0011
                data[i][j] = self.INV_SHB[row][col]
        return data
    
    def __do_shift(self, data: List[List[int]]):
        """ShiftRows (меняет местами элементы нижней строки)"""
        data[1][0], data[1][1] = data[1][1], data[1][0]
        return data
    
    def __do_mix_cols(self, data: List[List[int]]):
        """Прямое перемешивание столбцов (MixColumns)"""
        result = [[0, 0], [0, 0]]
        for i in range(2):
            result[0][i] = int(self.GF16(3) * self.GF16(data[0][i]) ^ self.GF16(2) * self.GF16(data[1][i]))
            result[1][i] = int(self.GF16(2) * self.GF16(data[0][i]) ^ self.GF16(3) * self.GF16(data[1][i]))
        return result
        
    def encrypt(self, text: str, key: str):
        block_text = self.__convert_to_block(text)
        block_key = self.__convert_to_block(key)
        second_round_key = self._generate_round_key(block_key, 2)
        third_round_key = self._generate_round_key(second_round_key, 3)
        
        logger.log(f"=== НАЧАЛО ШИФРОВАНИЯ ===")
        logger.log(f"блок открытого текста: {block_text}")
        logger.log(f"ключ: {block_key}")
        logger.log(f"ключ второго раунда: {second_round_key}")
        logger.log(f"ключ третьего раунда: {third_round_key}")
        
        
        # Раунд 1
        logger.log("=== Раунд 1 ===")
        xored_step_1 = self.__do_xor(block_text, block_key)
        logger.log(f"после AddRoundKey (исходный ключ): {xored_step_1}")
        
        
        mapped_step_1 = self.__do_mapping(xored_step_1)
        logger.log(f"после SubBytes: {mapped_step_1}")
        
        
        shifted_step_1 = self.__do_shift(mapped_step_1)
        logger.log(f"после ShiftRows: {shifted_step_1}")
        
        
        mixd = self.__do_mix_cols(shifted_step_1)
        logger.log(f"после MixColumns: {mixd}")
        
        
        # Раунд 2
        logger.log("=== Раунд 2 ===")
        xored_step_2 = self.__do_xor(mixd, second_round_key)
        logger.log(f"после AddRoundKey (ключ раунда 2): {xored_step_2}")
        
        
        mapped_step_2 = self.__do_mapping(xored_step_2)
        logger.log(f"после SubBytes: {mapped_step_2}")
        
        
        shifted_step_2 = self.__do_shift(mapped_step_2)
        logger.log(f"после ShiftRows: {shifted_step_2}")
        
        
        # Раунд 3
        logger.log("=== Раунд 3 (финальный) ===")
        final = self.__do_xor(shifted_step_2, third_round_key)
        logger.log(f"после AddRoundKey (ключ раунда 3): {final}")
        
        
        result = self.__convert_from_block(final)
        logger.log(f"Результат шифрования: {result}")
        return result

    
    def decrypt(self, text: str, key: str):
        block_enc_text = self.__convert_to_block(text)
        block_key = self.__convert_to_block(key)
        second_round_key = self._generate_round_key(block_key, 2)
        third_round_key = self._generate_round_key(second_round_key, 3)
        
        logger.log(f"=== НАЧАЛО РАСШИФРОВАНИЯ ===")
        logger.log(f"блок шифротекста: {block_enc_text}")
        logger.log(f"ключ: {block_key}")
        logger.log(f"ключ второго раунда: {second_round_key}")
        logger.log(f"ключ третьего раунда: {third_round_key}")
        
        
        # Раунд 3 (обратный последнему раунду шифрования)
        logger.log("=== Раунд 3 (обратный раунду 3 шифрования) ===")
        xored_step_3 = self.__do_xor(block_enc_text, third_round_key)
        logger.log(f"после XOR с ключом третьего раунда: {xored_step_3}")
        
        
        # Раунд 2 (обратный второму раунду шифрования)
        logger.log("=== Раунд 2 (обратный раунду 2 шифрования) ===")
        inv_shifted_step_2 = self.__do_shift(xored_step_3.copy())
        logger.log(f"после InvShiftRows: {inv_shifted_step_2}")
        
        
        inv_mapped_step_2 = self.__do_inv_mapping(inv_shifted_step_2.copy())
        logger.log(f"после InvSubBytes: {inv_mapped_step_2}")
        
        
        xored_step_2 = self.__do_xor(inv_mapped_step_2.copy(), second_round_key)
        logger.log(f"после XOR с ключом второго раунда: {xored_step_2}")
        
        
        inv_mixd = self.__do_mix_cols(xored_step_2.copy())
        logger.log(f"после InvMixColumns: {inv_mixd}")
        
        
        # Раунд 1
        logger.log("=== Раунд 1 (обратный раунду 1 шифрования) ===")
        inv_shifted_step_1 = self.__do_shift(inv_mixd.copy())
        logger.log(f"после InvShiftRows: {inv_shifted_step_1}")
        
        
        inv_mapped_step_1 = self.__do_inv_mapping(inv_shifted_step_1.copy())
        logger.log(f"после InvSubBytes: {inv_mapped_step_1}")
        
        
        final = self.__do_xor(inv_mapped_step_1.copy(), block_key)
        logger.log(f"после XOR с исходным ключом: {final}")
        
        
        result = self.__convert_from_block(final)
        logger.log(f"Результат расшифрования: {result}")
        return result