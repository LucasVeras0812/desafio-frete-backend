import pytest

from src.main import gerar_frete, calcular_frete_por_cep

class TestFrete:
    @pytest.mark.parametrize(
        "peso, distancia, opcao, tipo, valor_esperado",
        [
            (2.0, 500, 1, "Normal", 1005.00),
            (2.0, 500, 2, "Sedex", 1010.00),
            (3.4, 500, 3, "Sedex10", 1715.00),
        ],
        ids=["Normal", "Sedex", "Sedex10"],
    )
    def test_gerar_frete_opcoes_validas(
        self, peso, distancia, opcao, tipo, valor_esperado
    ):
        resultado = gerar_frete(peso, distancia, opcao)
        assert resultado == f"O valor do frete é {valor_esperado:.2f}"

    def test_input_peso_invalido(self):
        peso = -3
        distancia = 500
        opcao = 3
        with pytest.raises(ValueError):
            resultado = gerar_frete(peso, distancia, opcao)

    def test_input_opcao_invalida(self):
        peso = 4
        distancia = 500
        opcao = 0
        with pytest.raises(ValueError):
            resultado = gerar_frete(peso, distancia, opcao)

    def test_input_distancia_invalida(self):
        peso = 4.2
        distancia = 0
        opcao = 3
        with pytest.raises(ValueError):
            resultado = gerar_frete(peso, distancia, opcao)

    def test_gerar_frete_entrada_nao_numerica(self):
        peso = "abc"
        distancia = 500
        opcao = 1
        with pytest.raises(TypeError):
            gerar_frete(peso, distancia, opcao)

    def test_gerar_frete_entrada_nula(self):
        peso = None
        distancia = 500
        opcao = 1
        with pytest.raises(TypeError):
            gerar_frete(peso, distancia, opcao)

class TestFretePorCEP:#
    def test_calcular_frete_por_cep(self, monkeypatch):#
        res_cep = [#
            (-22.55, -46.66),#
            (-22.98, -43.19),#
        ]#

        def coordenadas_cep_fake(cep):#
            return res_cep.pop(0)#

        monkeypatch.setattr("src.main.coordenadas_cep", coordenadas_cep_fake)#
        monkeypatch.setattr(#
            "src.main.calcular_distancia_coordenada",#
            lambda *args, **kwargs: 500.0#
        )#

        res = calcular_frete_por_cep("01000-000", "20000-000", 2.0, 1)#

        assert res == "O valor do frete é 1005.00"#

    def test_calcular_frete_por_cep_invalido(self, monkeypatch):#
        msg_erro = "CEP 99999-999 não encontrado."#

        def cep_fake(*args, **kwargs):#
            raise ValueError(msg_erro)#
        
        monkeypatch.setattr("src.main.coordenadas_cep", cep_fake)

        res = calcular_frete_por_cep("01000-000", "99999-999", 10, 1)#

        assert f"Ocorreu um erro: {msg_erro}" in res#