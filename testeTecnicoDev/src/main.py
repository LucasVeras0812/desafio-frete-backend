from model.frete import Frete
from api_services import coordenadas_cep, calcular_distancia_coordenada

def gerar_frete(peso, distancia, opcao) -> str:
    if not isinstance(peso, (int, float)):
        raise TypeError("O peso deve ser um valor numério")
    if not isinstance(distancia, (int, float)):
        raise TypeError("A distancia deve ser um valor numério")
    if peso <= 0:
        raise ValueError("O peso deve ser um valor positivo")
    if distancia <= 0:
        raise ValueError("A distancia deve ser um valor positivo")

    try:
        if opcao == 1:
            frete = Frete(distancia, peso)
            frete.tipo = "Normal"
            frete.calcular_preco()
        elif opcao == 2:
            frete = Frete(distancia, peso)
            frete.tipo = "Sedex"
            frete.calcular_preco()
        elif opcao == 3:
            frete = Frete(distancia, peso)
            frete.tipo = "Sedex10"
            frete.calcular_preco()
        else:
            raise ValueError("Opção de frete inválida")
    except Exception as e:
        raise e
    return f"O valor do frete é {frete.valor:.2f}"

def calcular_frete_por_cep(cep_origem, cep_destino, peso, opcao):
    try:#
        print(f"Buscando coordenadas para o CEP de origem: {cep_origem}")
        latitude_origem, longitude_origem = coordenadas_cep(cep_origem)
        print(f"Latidude encontrada: {latitude_origem} e Longitude encontrada: {longitude_origem}")
        
        print(f"Buscando coordenadas para o CEP de destino: {cep_destino}")
        latitude_destino, longitude_destino = coordenadas_cep(cep_destino)
        print(f"Latidude encontrada: {latitude_destino} e Longitude encontrada: {longitude_destino}")
        print("Calculando a distancia entre os pontos...")
        distancia = calcular_distancia_coordenada(
            latitude_origem, longitude_origem, latitude_destino, longitude_destino
        )
        print(f"Distancia da rota: {distancia:.2f} KM")
        print("Calculando o valor final do frete...")
        res_frete = gerar_frete(peso, distancia, opcao)

        return res_frete
    
    except (ValueError, Exception) as e:
        return f"Ocorreu um erro: {e}"
        
if __name__ == "__main__":
    cep_origem = input("Digite o CEP de origem: ")
    cep_destino = input("Digite o CEP de destino: ")
    peso = float(input("Entre com o peso da encomenda -> "))
    opcao = int(
        input(
            "Entre com a opcao de entrega\n\t(1)Normal\n\t(2)Sedex\n\t(3)Sedex10\n-> "
        )
    )

    res = calcular_frete_por_cep(cep_origem, cep_destino, peso, opcao)
    print()
    print(res)