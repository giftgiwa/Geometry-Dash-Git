from decode_encode import CCLocalLevels
import base64
import zlib
import gzip
import re

# store info for level (i.e. "repository")
class LevelParser:
    def __init__(self, cc_local_levels: CCLocalLevels):
        self.level_string = cc_local_levels.CCLocalLevels_decrypted

        # keys of hashmap: level names
        self.levels = {}

    
    # decode a singular level
    # source: https://wyliemaster.github.io/gddocs/#/topics/levelstring_encoding_decoding
    # def decode_level(self, s: str):
    def encode_level(self, s: str):
        gzipped = gzip.compress(s.encode())
        b64_encoded = base64.urlsafe_b64encode(gzipped)
        return b64_encoded.decode()
    
    def decode_level(self, s: str):
        b64_decoded = base64.urlsafe_b64decode(s.encode())
        decompressed = zlib.decompress(b64_decoded, 15 | 32)
        return decompressed.decode()
    
    def split_level_string(self, s: str):

        
        '''
        helper function to find the indices of all occurrences of the strings:
        <k>k2</k><s>, </s><k>k4</k><s>, and <s><k>k5</k><s>
        These bound the title of the level and the string for it
        '''
        # source: https://wyliemaster.github.io/gddocs/#/resources/client/level?id=level
        def find_all_indices_regex(string, substring):
            return [m.start() for m in re.finditer('(?={})'.format(re.escape(substring)), string)]


         

if __name__ == '__main__':
    levels = LevelParser(CCLocalLevels())
    # just some test code
    level_string = "H4sIAAAAAAAAC6WT0W3DMAxEF1IAHknJCvqVGTIAB8gKHb6iTkgTwG0c5MM8m0c-kQJ8u1ovCJfQgNaw0FoDoCiFSY8TogVEJLZAoGboIdED34iJED2GwOeI8y4ia9hwCKKR_Xugt65kfH_O8P8WmhA0vFqo_rnQm6D2CnT0ivfWKrcLrEhKpTSKlxH5vs2oy-cXesrVzvRmJGcaF5-RLoRFrFKWKSt0K8hyoYCiU5QoJcXoGT3jaE6YE-aVnlGcwrmNB-VPlnKegjU-YbrmBKce8pVnarFxN4M56HU8K1n7Y7KMrrziZXqbpjy3uD1lH3vE7n7Hsls5ocuv23bcO-MHh6d3MUAEAAA="

    # print(levels.decode_level(level_string))
    





