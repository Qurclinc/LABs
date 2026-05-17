# def encrypt_stream(self, input_file: os.PathLike, output_file: os.PathLike, chunk_size: int = 8192) -> Tuple[bool, str]:
#     try:
#         file_size = os.path.getsize(input_file)
#         # Генерируем IV на основе размера файла
#         iv_len = file_size % (secrets.randbits(8) + 1)
#         step = max(1, ((file_size - 1) // iv_len) // 3)
#         vector = [secrets.randbits(8) for _ in range(iv_len)]
        
#         seed = sum(vector)
#         random.seed(seed)
#         key_list = list(self.key)
#         random.shuffle(key_list)
        
#         # Пишем заголовок
#         with open(output_file, 'wb') as f_out:
#             header = str(iv_len).encode() + f"0x{secrets.token_hex(2)}".encode() + str(step).encode() + f"0x{secrets.token_hex(2)}".encode()
#             f_out.write(header)
            
#             # Обрабатываем файл чанками
#             with open(input_file, 'rb') as f_in:
#                 chunk_num = 0
#                 while True:
#                     chunk = f_in.read(chunk_size)
#                     if not chunk:
#                         break
                    
#                     # Шифруем чанк
#                     encrypted_chunk = self._xor_chunk(chunk, key_list, chunk_num * chunk_size)
                    
#                     # Вставляем IV элементы (только для первых чанков)
#                     if chunk_num * chunk_size < iv_len * step:
#                         encrypted_chunk = self._insert_iv_in_chunk(encrypted_chunk, vector, step, chunk_num * chunk_size)
                    
#                     f_out.write(encrypted_chunk)
#                     chunk_num += 1
                    
#         return (True, "Success")
        
#     except Exception as e:
#         return (False, str(e))

# def _xor_chunk(self, chunk: bytes, key: list, start_index: int) -> bytes:
#     """XOR для одного чанка"""
#     result = bytearray()
#     len_key = len(key)
#     for i, byte in enumerate(chunk):
#         result.append(byte ^ key[(start_index + i) % len_key])
#     return bytes(result)

# def _insert_iv_in_chunk(self, chunk: bytes, vector: list, step: int, chunk_start: int) -> bytes:
#     """Вставка IV элементов в чанк (если нужно)"""
#     chunk_list = bytearray(chunk)
    
#     # Вычисляем какие IV элементы попадают в этот чанк
#     for i, iv_byte in enumerate(vector):
#         iv_pos = i * step
#         if chunk_start <= iv_pos < chunk_start + len(chunk):
#             # IV элемент попадает в этот чанк
#             pos_in_chunk = iv_pos - chunk_start
#             chunk_list.insert(pos_in_chunk, iv_byte)
            
#     return bytes(chunk_list)

# def decrypt_stream(self, input_file: os.PathLike, output_file: os.PathLike, chunk_size: int = 8192) -> Tuple[bool, str]:
#     try:
#         # Сначала читаем только заголовок
#         with open(input_file, 'rb') as f:
#             header_data = f.read(100)
#             # Парсим заголовок...
#             iv_length, step = self._parse_header(header_data)
#             header_len = self._calculate_header_length(iv_length, step)
            
#         # Обрабатываем основной файл чанками
#         with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
#             f_in.seek(header_len)  # Пропускаем заголовок
            
#             # Восстанавливаем IV из первых чанков
#             vector = self._extract_iv_from_stream(f_in, iv_length, step, chunk_size)
            
#             # Перематываем и обрабатываем с учетом извлеченного IV
#             f_in.seek(header_len)
#             self._decrypt_stream_with_iv(f_in, f_out, vector, step, chunk_size)
            
#         return (True, "Success")
        
#     except Exception as e:
#         return (False, str(e))