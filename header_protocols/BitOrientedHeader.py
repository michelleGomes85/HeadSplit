
from expections.InvalidDataError import InvalidDataError

class BitOrientedHeader:
    
    """
    Classe para manipulação de cabeçalhos orientados a bits.
    Montagem e desmontagem com Bit Stuffing.
    
    Exemplo entrada: 0111111010110
    Exemplo Montagem: 01111110 01111101010110 01111110
    
    """
    
    FLAG = "01111110"
    SPACE = " "

    @staticmethod
    def mount(data):
        
        data = data.strip()
        
        if not data:
            raise InvalidDataError("Preencha o corpo do texto")
        
        if not all(bit in '01' for bit in data):
            raise InvalidDataError("A sequência de bits deve conter apenas '0' ou '1'.")
              
        message = data.replace("011111", "0111110")
        
        stuffed_message = BitOrientedHeader.FLAG + BitOrientedHeader.SPACE + message
        
        stuffed_message += BitOrientedHeader.SPACE + BitOrientedHeader.FLAG 
        
        return stuffed_message

    @staticmethod
    def unmount(header):
        
        if header.startswith(BitOrientedHeader.FLAG) and header.endswith(BitOrientedHeader.FLAG):
        
            message = header[len(BitOrientedHeader.FLAG):-len(BitOrientedHeader.FLAG)]
            message = message.strip()
        
            message = message.replace("0111110", "011111")
        
            return message
        else:
            raise ValueError("Cabeçalho inválido para formato orientado a bits")
