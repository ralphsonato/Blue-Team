
## O que é YARA?

YARA é uma linguagem de assinatura criada pra identificar e classificar arquivos com base em padrões, tanto textuais quanto binários. A ideia central é simples: você descreve como um malware, webshell, ou qualquer arquivo malicioso se parece por dentro (quais strings contém, quais bytes aparecem, qual combinação de características tem), e o YARA varre arquivos procurando esse padrão.

O resultado é binário: ou o arquivo bate com a regra, ou não bate.

## Pra que serve

Principalmente pra criar regras de detecção que identificam malware com base nos padrões que ele exibe, strings internas, endereços IP, domínios de C2, endereços de carteira Bitcoin pra pagamento de ransom, sequências de bytes específicas, e por aí vai.

## A analogia que uso pra fixar

Pensa no YARA como um detector de metal adaptável. Em vez de metal, ele detecta **padrões dentro de arquivo**. E diferente de um antivírus comum (que usa assinaturas que o fornecedor define pra você), no YARA **você escreve a assinatura**, o que é poderoso porque você consegue descrever ameaças novas, variantes ainda não catalogadas, ou comportamentos específicos do seu ambiente.

## Blue Team, Red Team ou Purple Team?

Os três. Essa é a parte que a maioria dos tutoriais não fala.

**Blue Team** usa YARA pra detectar e escreve regras que identificam malware, webshell, ferramenta ofensiva (Mimikatz, Rubeus, Cobalt Strike), e varre endpoints em busca dessas assinaturas.

**Red Team** usa YARA pra evadir e roda as regras de blue team contra o próprio payload antes de usá-lo, e modifica o código até não bater mais. Você não consegue evitar o que não conhece, então entender YARA é obrigatório pra quem quer fazer evasão de assinatura.

**Purple Team** usa YARA no ciclo de validação e o blue escreve a regra, red testa se ela detecta de verdade (e não só no papel), resultado volta pro blue com o que precisa ser refinado. YARA é uma das ferramentas centrais desse loop.

## Como o YARA é executado

YARA é uma ferramenta standalone e não é nativa de nenhum SIEM. Você roda via linha de comando, apontando uma regra pra um alvo:

```bash
# varre um arquivo específico
yara regra.yar arquivo_suspeito.jsp

# varre uma pasta inteira
yara regra.yar /var/www/html/

# varre recursivamente (entra em subpastas)
yara -r regra.yar /opt/teamcity/
```

Se a regra bater, a saída mostra o nome da regra e o arquivo:
```
NomeDaRegra arquivo_suspeito.jsp
```

Se não bater, não aparece nada.

## Extensão do arquivo de regra

O arquivo de regras usa a extensão `.yar`. Um único arquivo `.yar` pode conter uma ou várias regras, na prática, repositórios públicos como o YARA-Rules do GitHub têm centenas de regras num mesmo conjunto de arquivos, que você roda de uma vez contra o alvo:

```bash
yara -r /pasta/com/regras/*.yar /pasta/suspeita/
```

---
