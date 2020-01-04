Задание для потенциальных кандидатов на позицию Junior-девелоперов.
Представляет из себя проcтой ETL с разными форматами файлов.

**Код решения задания должен соответствовать [PEP8](https://www.python.org/dev/peps/pep-0008/)**

Задание состоит из двух блоков:

1. [Basic](#basic) - основная задача (обязателльна для выполнения)
2. [Advanced](#advanced) - дополнение к основной задаче (желательно сделать)

Кроме этого есть набор [пунктов для рызмышления дающих бонусы](#бонусы)

Использовать можно только средства стандартной библиотеки Python.
Во всех случаях программа должна запускаться из терминала.

Для проверки работы программы предоставлются входные данные и результаты в виде 6 файлов:
* входные данные:
  * csv_data_1.csv
  * csv_data_2.csv
  * json_data.json
  * xml_data.xml
* результаты **Basic**:
  * basic_results.tsv
* результаты **Advanced**:
  * advanced_results.tsv

## Задача
Есть четыре файла: два `.csv`, один `.json` и один .`xml` файл.   


Первый `.csv` имеет следующую структуру:

|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |
|... |... |... |... |... |... |... |... |

Второй `.csv` имеет следующую структуру:

|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |... |Mz  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |... |i   |
|... |... |... |... |... |... |... |... |... |... |

**Внимание! Порядок колонок может несовпадать. В обоих файлах есть заголовки.**


`.json` файл имеет следуующую структуру:
```python
{
  "fields": [
    {
      "D1": "s",
      "D2": "s",
      ...
      "Dn": "s",
      "M1": i,
      ...
      "Mp": i,
    },
    ...
  ]
}
```

`.xml` файл сожержит в себе следующую структуру:
```xml
<objects>
  <object name="D1">
    <value>s</value>
  </object>
  <object name="D2">
    <value>i</value>
  </object>
  ...
  <object name="Dn">
    <value>s</value>
  </object>
  <object name="M1">
    <value>i</value>
  </object>
  <object name="M2">
    <value>i</value>
  </object>
  ...
  <object name="Mn">
    <value>i</value>
  </object>
</objects>
```

Где *z* > *n*, *p* >= *n*, *s* строка и *i* целое число.

### Basic

Файлы нужно будет трансформировать в один `.tsv` файл со следующей структурой:


|D1  |D2  |... |Dn  |M1  |M2  |... |Mn  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|s   |s   |... |s   |i   |i   |... |i   |
|... |... |... |... |... |... |... |... |

Он должен быть отсортирован по колонке **D1** и содержать даннные из всех четырёх файлов.


### Advanced

Файлы нужно будет трансформировать в один `.tsv` файл со следующей структурой:

|D1   |D2   |... |Dn   |MS1  |MS2  |...  |MSn  |
|:---:|:--:|:---:|:---:|:---:|:---:|:---:|:---:|
|s    |s   |...  |s    |i    |i    |...  |i    |
|...  |... |...  |...  |...  |...  |...  |...  |

В колонках **MS1**...**MSn** должны находиться суммы знаений соответствующих **M1**...**Mn** из 4 файлов сгруппированные 
по уникальнным значениям комбинаций строк из **D1**...**Dn**.

##### Пример
**Содржимое .tsv файла с данными из 4 файлов:**

|D1  |D2  |M1  |M2  |M3  |
|:--:|:--:|:--:|:--:|:--:|
|a   |a   |0   |0   |0   |
|a   |a   |1   |0   |1   |
|a   |a   |0   |2   |1   |
|a   |b   |1   |1   |1   |
|c   |c   |7   |7   |7   |

**Ожидаемый результат:**

|D1  |D2  |M1  |M2  |M3  |
|:--:|:--:|:--:|:--:|:--:|
|a   |a   |1   |2   |2   |
|a   |b   |1   |1   |1   |
|c   |c   |7   |7   |7   |


### Бонусы

Нужно попытаться учесть несколько фактов:
* в дальнейшем использовании программы возможно появление требования для работы с другими типами файлов, например `.yaml`.
* входные файлы могут быть больших размеров
* возможность обработки строк с некорректными значениями без прекращения выполнения программы с информированием пользователя об ошибках в конце её выполнения
* подумать об организации тестирования программы
