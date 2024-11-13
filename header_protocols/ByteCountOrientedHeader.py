from expections.InvalidDataError import InvalidDataError

class ByteCountOrientedHeader:
    
    """
    Classe para manipulação de cabeçalhos orientados a contagem de byte.
    Montagem e desmontagem usando o campo de comprimento.
    
    Exemplo Entrada: Ola 3 
    Exemplo Saida: STX 003 Ola
    
    1 Byte = 8 bits, considere cada caractere da mensagem como 1 byte
    
    """
    FLAG = "STX"
    SPACE = " "
    
    @staticmethod
    def mount(data, size):
        
        if not data:
            raise InvalidDataError("Preencha o corpo do texto")
        
        if not size.isdigit():
            raise InvalidDataError("Tamanho em bytes inválido.")
        
        size = int(size)
        length = len(data)
        if size != length:
            raise InvalidDataError(f"Tamanho incorreto. Esperado {length} bytes, mas foi fornecido {size} bytes.")
        
        length_field = f"{length:03}"  
        
        return ByteCountOrientedHeader.FLAG + ByteCountOrientedHeader.SPACE + length_field + ByteCountOrientedHeader.SPACE + data

    @staticmethod
    def unmount(header):
        
        try:
            header = header.strip()

            if not header.startswith(ByteCountOrientedHeader.FLAG):
                raise ValueError("Cabeçalho inválido. Esperado delimitador 'STX' no início.")
            
            # Remover o delimitador STX e o campo de comprimento
            header = header[len(ByteCountOrientedHeader.FLAG):].strip()

            # Obter o campo de comprimento (primeiros 3 caracteres após STX)
            length_field = header[:3]
            data = header[4:]  # O restante é o corpo da mensagem
            
            return data.strip()
        except ValueError as e:
            raise ValueError(f"Erro ao desmontar cabeçalho: {str(e)}")