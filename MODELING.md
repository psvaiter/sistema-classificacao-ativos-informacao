# Sistema de Classificação de Ativos da Informação

Universidade Federal do Rio de Janeiro  
Engenharia Eletrônica e de Computação  
Disciplina: Projeto de Graduação  
Autor: Patrick Svaiter

## Objetivo

Implementar um sistema que permita avaliação dos riscos dos ativos de informação de uma empresa e qual impacto é gerado para essa empresa em caso de comprometimento de um ativo.

## Premissas

- Uma empresa possui ativos de informação.
- Um ativo de informação possui vulnerabilidades para uma empresa.
- Um ativo de informação possui relevância para uma empresa.
- Uma ameaça existe por si só e afeta diferentes ativos de informação de acordo com a empresa.
- Uma ameaça não afeta ativos sem vulnerabilidades. (?)
- Uma ameaça pode afetar um ativo em uma localidade, mas não afetar o mesmo ativo em outra localidade. Ex: terremoto.
- Um ativo de informação possui investimento inicial, e sofre com depreciação ou valorização.
- Um ativo de informação possui nome, tipo e _tags_.
- Os tipos de um ativo de informação são:
  - Hardware
  - Software
  - Person
  - Supply
  - Place
  - Process
- O impacto do ataque à vulnerabilidade de um ativo pode ser obtido automaticamente em função da relevância e vulnerabilidade.  
    impacto = f(ativo, relevancia, vulnerabilidade)
- Uma vulnerabilidade é graduada.
- Uma vulnerabilidade é inerente ao ativo independente da empresa.
  Porém, cada empresa pode tomar medidas de controle diferentes de forma a reduzir a vulnerabilidade.
- Ameaças naturais geralmente não atacam um ativo, mas todos os ativos localizados em uma dada região, impactando a empresa como um todo.
- Uma ameaça pode explorar mais de uma vulnerabilidade de uma ativo, ou vulnerabilidades avulsas de diferentes ativos.
- Uma ameaça é dada como conhecida quando possui um ativo de uma empresa como alvo.
- Uma ameaça conhecida para uma empresa pode gerar alerta para empresas que possuem negócios ou ativos semelhantes.
  
## Requisitos de negócio

- Listar, adicionar, atualizar e remover ativos.
- Listar, adicionar, atualizar e remover ameaças.
- Listar, adicionar, atualizar e remover empresas.
- Listar, adicionar, atualizar e remover vulnerabilidade dos ativos. (na empresa? ou inerente ao ativo?)
- Listar, adicionar, atualizar e remover ativos de uma empresa.
- Listar, adicionar, atualizar e remover ameaças aos ativos de uma empresa. Considerar a localidade.
- Listar, adicionar, atualizar e remover vulnerabilidades de um ativo na empresa.  
- Manter histórico é importante para verificação de evolução após investimento em segurança.
- As modificações na vulnerabilidade de um ativo pode ser para fins de simulação ou decorrente de algum investimento em segurança.
- Simulações devem ser persistidas à parte?
- Estratégias de classificação: manter a básica = _fuzzy_.
- Um incidentes de segurança da informação deve ser registrado indicando quais ativos tiveram suas vulnerabilidades exploradas, para saber se ela estava coberta e o que pode ser feito para melhorar.  
  - Data do incidente
  - Descrição do incidente
  - Ativos explorados
  - Processos de negócio impactados
  - Classificação de relevância e vulnerabilidade do ativo no dia do incidente
  - Como prevenir
- A inexistência de alguns processos pode constituir uma vulnerabilidade, portanto deve ser possível avaliar isso sem o ativo cadastrado.
    Ex: Ausência de Política de SI. Como avaliar a vulnerabilidade se o ativo não existe (está ausente)?

## Modelo do banco de dados

O banco de dados, chamado de `information_assets`, é modelado como mostrado pelo diagrama na imagem abaixo, seguindo as premissas listadas acima.

![database-diagram-full](https://user-images.githubusercontent.com/16355712/32494677-ad22f250-c3a9-11e7-80ef-c359cd6f8113.png)