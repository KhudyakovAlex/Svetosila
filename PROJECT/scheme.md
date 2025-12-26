# Схема АПК

```mermaid

flowchart LR
  USER((🧔<br>Пользователь))

  subgraph ПК
    subgraph Браузер
      FE(Клиент)
    end
  end

  subgraph Сервер
    direction TB
     BE(Сервер)
     DB[(БД)]
  end

  subgraph ШУНО
    subgraph RAPIDA
      FW(Прошивка)
    end
  end

  LUM((💡<br>Светильник))

  USER <---> FE
  FE <---> BE
  BE <--GSM/REST-API--> FW
  FW <--LoRaWAN--> LUM
  BE <---> DB
```