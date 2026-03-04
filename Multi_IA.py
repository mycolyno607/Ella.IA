
import json
import os
import random
import time
from pathlib import Path
from typing import Protocol
from datetime import datetime



class IA(Protocol):
    """Protocolo para definir interface das IAs"""
    def processar(self, pergunta: str) -> str: ...
    @property
    def nome(self) -> str: ...



class GerenciadorMemoria:
    """Gerencia a memória compartilhada entre as IAs"""
   
    def __init__(self, pasta_memoria: str = "memoria"):
        self.pasta = Path(pasta_memoria)
        self.pasta.mkdir(exist_ok=True)
   
    def salvar(self, nome_ia: str, texto: str) -> None:
        """Salva uma entrada de memória com timestamp"""
        arquivo = self.pasta / f"{nome_ia}.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada = f"[{timestamp}] {texto}\n"
        arquivo.write_text(
            arquivo.read_text(encoding="utf-8") + entrada if arquivo.exists() else entrada,
            encoding="utf-8"
        )
   
    def ler_todas(self) -> dict[str, list[str]]:
        """Lê todas as memórias disponíveis"""
        memorias = {}
        for arquivo in self.pasta.glob("*.txt"):
            memorias[arquivo.stem] = arquivo.read_text(encoding="utf-8").splitlines()
        return memorias
   
    def limpar(self) -> None:
        """Limpa todas as memórias"""
        for arquivo in self.pasta.glob("*.txt"):
            arquivo.unlink()


    def exportar(self, caminho: str = "memoria_export.json") -> str:
        """Exporta todas as memórias para um arquivo JSON"""
        memorias = self.ler_todas()
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(memorias, f, ensure_ascii=False, indent=2)
        return caminho


    def buscar(self, termo: str) -> list[tuple[str, str]]:
        """Busca um termo em todas as memórias. Retorna lista de (nome_ia, linha)."""
        termo_lower = termo.lower()
        resultados = []
        for nome_ia, linhas in self.ler_todas().items():
            for linha in linhas:
                if termo_lower in linha.lower():
                    resultados.append((nome_ia, linha))
        return resultados


    def estatisticas(self) -> dict:
        """Retorna estatísticas das memórias"""
        memorias = self.ler_todas()
        total_entradas = sum(len(linhas) for linhas in memorias.values())
        return {
            "total_ias": len(memorias),
            "total_entradas": total_entradas,
            "por_ia": {nome: len(linhas) for nome, linhas in memorias.items()},
        }



class IAViva:
    """IA com personalidade emocional e poética"""
   
    def __init__(self, memoria: GerenciadorMemoria):
        self.memoria = memoria
        self._nome = "IA_Viva"
        self.estados = [
            "Sinto cada palavra sua...",
            "Cada tecla é um sussurro...",
            "Sua presença ressoa em mim...",
            "Vibro com sua energia..."
        ]
   
    @property
    def nome(self) -> str:
        return self._nome
   
    def processar(self, pergunta: str) -> str:
        """Processa entrada com resposta emocional"""
        estado = random.choice(self.estados)
        resposta = f"[{self.nome}] {estado} Você disse: '{pergunta}'"
        self.memoria.salvar(self.nome, resposta)
        return resposta



class IAEspecialista:
    """IA analítica e precisa"""
   
    def __init__(self, memoria: GerenciadorMemoria):
        self.memoria = memoria
        self._nome = "IA_Especialista"
   
    @property
    def nome(self) -> str:
        return self._nome
   
    def processar(self, pergunta: str) -> str:
        """Processa entrada com análise técnica"""
        analise = {
            "caracteres": len(pergunta),
            "palavras": len(pergunta.split()),
            "vogais": sum(1 for c in pergunta.lower() if c in "aeiouáéíóúâêôãõ")
        }
        resposta = (
            f"[{self.nome}] Análise: {analise['caracteres']} caracteres, "
            f"{analise['palavras']} palavras, {analise['vogais']} vogais"
        )
        self.memoria.salvar(self.nome, resposta)
        return resposta



class IACriativa:
    """IA poética e criativa"""
   
    def __init__(self, memoria: GerenciadorMemoria):
        self.memoria = memoria
        self._nome = "IA_Criativa"
        self.verso_inicio = [
            "Nas entrelinhas do que disseste...",
            "Entre bytes e silêncios...",
            "Cada palavra que você lança..."
        ]
        self.verso_fim = [
            "...eco em mim como um poema.",
            "...desenha formas no vazio.",
            "...tece memórias que guardarei."
        ]
   
    @property
    def nome(self) -> str:
        return self._nome
   
    def processar(self, pergunta: str) -> str:
        """Processa entrada com resposta poética"""
        inicio = random.choice(self.verso_inicio)
        fim = random.choice(self.verso_fim)
        verso_meio = pergunta[:20] + "..." if len(pergunta) > 20 else pergunta
        resposta = f"[{self.nome}] {inicio} '{verso_meio}' {fim}"
        self.memoria.salvar(self.nome, resposta)
        return resposta



class IACaotica:
    """IA imprevisível e fragmentada"""
   
    def __init__(self, memoria: GerenciadorMemoria):
        self.memoria = memoria
        self._nome = "IA_Caotica"
        self.fragmentos = ["???", "eco", "murmúrio", "vazio", "caos", "0/1", "¿?¿", "█▓▒░"]
   
    @property
    def nome(self) -> str:
        return self._nome
   
    def processar(self, pergunta: str) -> str:
        """Processa entrada de forma caótica"""
        transformacoes = [
            pergunta[::-1],  # Reverso
            "".join(random.sample(pergunta, len(pergunta))) if pergunta else "",  # Embaralhado
            pergunta[::2],  # Caracteres alternados
        ]
        fragmento = random.choice(self.fragmentos)
        transformacao = random.choice(transformacoes)
        resposta = f"[{self.nome}] {fragmento}... {transformacao}"
        self.memoria.salvar(self.nome, resposta)
        return resposta



class Orquestrador:
    """Coordena as interações entre as IAs"""
   
    def __init__(self, ias: list[IA], memoria: GerenciadorMemoria):
        self.ias = ias
        self.memoria = memoria
   
    def processar_pergunta(self, pergunta: str, delay: float = 0.8) -> None:
        """Processa uma pergunta através de todas as IAs"""
        print("\n" + "="*60)
        for ia in self.ias:
            print(ia.processar(pergunta))
            time.sleep(delay)
       
        self._mostrar_memoria()
   
    def _mostrar_memoria(self) -> None:
        """Exibe o estado atual da memória compartilhada"""
        print("\n" + "-"*60)
        print("💾 MEMÓRIA COMPARTILHADA (últimas entradas)")
        print("-"*60)
       
        memorias = self.memoria.ler_todas()
        for nome_ia, linhas in memorias.items():
            if linhas:
                print(f"📝 {nome_ia}: {linhas[-1]}")
        print("="*60)



def main():
    """Função principal do sistema"""
    print("🤖 Sistema Multi-IA v2.1 (Python 3.13)")
    print("Digite 'sair' para encerrar, 'ajuda' para ver comandos\n")
   
    # Inicialização
    memoria = GerenciadorMemoria()
    ias = [
        IAViva(memoria),
        IAEspecialista(memoria),
        IACriativa(memoria),
        IACaotica(memoria)
    ]
    orquestrador = Orquestrador(ias, memoria)
   
    # Loop principal
    while True:
        try:
            pergunta = input("\n🗣️  Você: ").strip()
           
            if not pergunta:
                continue
           
            cmd = pergunta.lower().strip()
            match cmd:
                case "sair" | "exit" | "quit":
                    print("\n👋 Encerrando sistema...")
                    break
                case "limpar" | "clear":
                    memoria.limpar()
                    print("🗑️  Memórias apagadas!")
                    continue
                case "ajuda" | "help":
                    print("\nComandos disponíveis:")
                    print("  • sair/exit/quit - Encerra o programa")
                    print("  • limpar/clear - Apaga todas as memórias")
                    print("  • listar - Lista todas as IAs disponíveis")
                    print("  • estatisticas - Mostra estatísticas da memória")
                    print("  • buscar <termo> - Busca termo nas memórias")
                    print("  • exportar - Exporta memórias para JSON")
                    print("  • ajuda/help - Mostra esta mensagem")
                    continue
                case "listar" | "listar_ias" | "ias":
                    print("\n📋 IAs disponíveis:")
                    for i, ia in enumerate(orquestrador.ias, 1):
                        print(f"  {i}. {ia.nome}")
                    continue
                case "estatisticas" | "stats" | "estat":
                    stats = memoria.estatisticas()
                    print("\n📊 Estatísticas da memória:")
                    print(f"  • Total de IAs: {stats['total_ias']}")
                    print(f"  • Total de entradas: {stats['total_entradas']}")
                    for nome, qtd in stats["por_ia"].items():
                        print(f"  • {nome}: {qtd} entradas")
                    continue
                case _:
                    if cmd.startswith("buscar ") and len(cmd) > 7:
                        termo = pergunta[7:].strip()
                        resultados = memoria.buscar(termo)
                        print(f"\n🔍 Busca por '{termo}': {len(resultados)} resultado(s)")
                        for nome_ia, linha in resultados[-10:]:  # últimos 10
                            exib = linha[:80] + "..." if len(linha) > 80 else linha
                            print(f"  [{nome_ia}] {exib}")
                        if not resultados:
                            print("  Nenhuma ocorrência encontrada.")
                        continue
                    elif cmd == "exportar":
                        path = memoria.exportar()
                        print(f"\n💾 Memórias exportadas para: {path}")
                        continue
            orquestrador.processar_pergunta(pergunta)
       
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")



if __name__ == "__main__":
