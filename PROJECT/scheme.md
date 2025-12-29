# Схема АПК

```mermaid
flowchart LR

CW(Клиент АПК<br>Веб)
CD(Клиент АПК<br>ПК)
CM(Клиент АПК<br>Телефон/планшет)
CVW(Клиент АПК<br>Видеостена)

  CW <--LAN<br>или<br>Internet--> S
  CD <--LAN<br>или<br>Internet--> S
  CM <--LAN<br>или<br>Internet--> S
  CVW <--LAN<br>или<br>Internet--> S

S[(Сервер АПК)]

   S <--Internet--> O

O@{ shape: tri, label: "Оператор<br>сотовой<br>связи" }

  O <--GSM--> R1
  O <--GSM--> R2

TP1(Точка<br>подключения)
  TP1 ==220В==> AV1

subgraph ШУНО - LoRaWAN
  R1(Контроллер<br>RAPIDA)
  LW(LoRaWAN<br>база)
  AV1(Выключатель)
end
R1 <---> LW
R1 <---> AV1
AV1 ==220В==> CB2
LW <-. LoRaWAN .-> LW1
LW <-. LoRaWAN .-> LW2

CB2@{ shape: f-circ, label: "" }

  CB2 ===> LUM3
  CB2 ===> LUM4

subgraph  
  LW1(LoRaWAN<br>модуль)
  LUM3((Светильник))
end

subgraph  
  LW2(LoRaWAN<br>модуль)
  LUM4((Светильник))
end

LW1 <---> LUM3
LW2 <---> LUM4



TP2(Точка<br>подключения)
  TP2 ==220В==> AV2

subgraph ШУНО - PLC
  R2(Контроллер<br>RAPIDA)
  PLC(PLC<br>база)
  AV2(Выключатель)
  B1@{ shape: f-circ, label: "" }
end
R2 <---> PLC
R2 <---> AV2
PLC <---> B1
AV2 ===> B1

B1 ==220В<br>+<br>PLC==> CB1

CB1@{ shape: f-circ, label: "" }

  CB1 ===> PLC1
  CB1 ===> PLC2

subgraph
  PLC1(PLC<br>модуль)
  LUM1((Светильник))
end

subgraph
  PLC2(PLC<br>модуль)
  LUM2((Светильник))  
end

  PLC1 <---> LUM1
  PLC1 ===> LUM1
  PLC2 <---> LUM2
  PLC2 ===> LUM2

```