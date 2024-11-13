
from expections.InvalidDataError import InvalidDataError

class CharacterOrientedHeader:
    
    """
    Classe para manipulação de cabeçalhos orientados a caracteres.
    Montagem e desmontagem com Character Stuffing.
    
    Exemplo de entrada: H6STXJ3DLE A S ETX STX
    Exemplo de montagem: STX H6DLESTXJ3DLEDLE A S DLEETX DLESTX ETX
    
    """
    
    START_FLAG = "STX"
    END_FLAG = "ETX"
    ESCAPE_CHAR = "DLE"
    SPACE = " "

    @staticmethod
    def mount(data):
        
        if not data:
            raise InvalidDataError("Preencha o corpo do texto")
        
        stuffed_data = data.replace(CharacterOrientedHeader.ESCAPE_CHAR, CharacterOrientedHeader.ESCAPE_CHAR + CharacterOrientedHeader.ESCAPE_CHAR)
        stuffed_data = stuffed_data.replace(CharacterOrientedHeader.START_FLAG, CharacterOrientedHeader.ESCAPE_CHAR + CharacterOrientedHeader.START_FLAG)
        stuffed_data = stuffed_data.replace(CharacterOrientedHeader.END_FLAG, CharacterOrientedHeader.ESCAPE_CHAR + CharacterOrientedHeader.END_FLAG)
        
        return CharacterOrientedHeader.START_FLAG + CharacterOrientedHeader.SPACE + stuffed_data + CharacterOrientedHeader.SPACE + CharacterOrientedHeader.END_FLAG

    @staticmethod
    def unmount(header):
        
        if header.startswith(CharacterOrientedHeader.START_FLAG) and header.endswith(CharacterOrientedHeader.END_FLAG):
            stuffed_data = header.strip()
            stuffed_data = header[len(CharacterOrientedHeader.START_FLAG):-len(CharacterOrientedHeader.END_FLAG)]
            stuffed_data = stuffed_data.replace(CharacterOrientedHeader.ESCAPE_CHAR + CharacterOrientedHeader.ESCAPE_CHAR, CharacterOrientedHeader.ESCAPE_CHAR)
            stuffed_data = stuffed_data.replace(CharacterOrientedHeader.ESCAPE_CHAR + CharacterOrientedHeader.START_FLAG, CharacterOrientedHeader.START_FLAG)
            stuffed_data = stuffed_data.replace(CharacterOrientedHeader.ESCAPE_CHAR + CharacterOrientedHeader.END_FLAG, CharacterOrientedHeader.END_FLAG)
        
            return stuffed_data.strip()
        else:
            raise ValueError("Cabeçalho inválido para formato orientado a caracteres.")
