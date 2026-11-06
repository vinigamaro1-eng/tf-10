# MiniGit — TF-10

Implementação didática de um histórico Git simplificado em Python. Os dados ficam em memória e são descartados quando o programa termina.

## O que o programa faz

- Cria commits com identificadores sequenciais (`c1`, `c2`, ...).
- Guarda a mensagem e os pais de cada commit.
- Cria e troca branches.
- Mescla duas branches criando um commit com dois pais.
- Percorre o histórico da branch atual com busca em largura (`log`).
- Busca commits por trecho da mensagem (`buscar`) e lista merges (`merges`).
- Informa a quantidade de passos da última operação com `medir()` (também disponível pela propriedade `passos`).

## Como executar

O projeto usa apenas a biblioteca padrão do Python. Na pasta do projeto:

```bash
python3 minigit.py
```

O arquivo define a classe `MiniGit`, portanto executar `minigit.py` diretamente não imprime uma demonstração. Para usar no terminal interativo:

```python
from minigit import MiniGit

repo = MiniGit()
c1 = repo.commitar("início do projeto")
repo.criar_branch("feature")
print(repo.log())
print(repo.medir())
```

## Testes

Execute a suíte com:

```bash
python3 -m unittest -v
```

## Respostas e análise

**Como os commits são relacionados?** Cada commit guarda uma tupla com os identificadores de seus pais. Um commit comum tem zero pais (o primeiro) ou um pai; um commit de merge tem dois.

**O que uma branch representa?** Uma branch é um nome que aponta para o commit mais recente daquela linha de desenvolvimento. Criar uma branch copia a referência da branch atual; não duplica commits.

**Como `log()` percorre o histórico?** A busca em largura começa no commit apontado pela branch atual, visita cada pai e usa um conjunto para não repetir ancestrais compartilhados. Por isso um grafo com merge não duplica commits.

**Como funciona `medir()`?** Ela devolve o contador de passos atualizado pela última operação. A medida é didática e conta registros visitados ou gravados; ela não é uma medição de segundos nem uma contagem universal de instruções.

| Operação | Passos registrados | Complexidade no modelo desta implementação |
|---|---:|---|
| `mensagem(commit)` | 1 | O(1) médio, dicionário por identificador |
| `pais(commit)` | 1 | O(1) médio, dicionário por identificador |
| `commitar(mensagem)` | 2 | O(1) médio, grava mensagem e pais |
| `criar_branch(nome)` / `trocar_branch(nome)` | 1 | O(1) médio, dicionário de branches |
| `log()` | total de commits alcançáveis | O(V + E), V commits e E relações de parentesco percorridos |
| `buscar(texto)` | até o commit encontrado ou todos | O(n · m) no pior caso, n mensagens de tamanho médio m |
| `merges()` | total de commits | O(V), examina os pais de cada commit |
| `mesclar(nome)` | 3 | O(1) médio, cria commit e atualiza a branch |

As contagens são as definidas no código e servem para comparar operações neste modelo. A tabela não substitui análise empírica em outros tamanhos de entrada.

## Ambiente

O enunciado mencionado na conversa pede WSL/Linux, mas o projeto fornecido está em um Mac com macOS. Os comandos acima usam `python3` e funcionam no macOS e Linux; a execução feita localmente no Mac não comprova os passos específicos de instalação ou uso do WSL. O PDF do enunciado não estava disponível nos arquivos encontrados, então confirme os requisitos específicos da disciplina antes de enviar.

## Git e GitHub

O diretório já contém um repositório Git local sem commits iniciais. Depois de revisar o projeto, registre os arquivos:

```bash
git add minigit.py test_minigit.py README.md .gitignore
git commit -m "Finaliza implementação MiniGit"
```

Para publicar, crie primeiro um repositório remoto privado ou público conforme as instruções do professor, associe a URL e envie a branch:

```bash
git remote add origin <URL_DO_REPOSITORIO>
git push -u origin main
```

Não há repositório remoto configurado neste projeto.
