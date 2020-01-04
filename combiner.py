import json
import csv
import sys
import xml.etree.cElementTree as etree
from operator import itemgetter


class Parser:

    def __init__(self, file: str):
        self.file = open(file)
        self.data = []

    def parse(self):
        raise NotImplementedError


class JsonParser(Parser):

    def parse(self) -> dict:
        json_data = json.load(self.file)
        for field in json_data.keys():
            for objects in json_data[field]:
                self.data.append(objects)
        return self.data


class CsvParser(Parser):

    def parse(self) -> dict:
        reader = csv.DictReader(self.file)
        for row in reader:
            self.data.append(dict(row))
        return self.data


class XmlParser(Parser):
    def __init__(self, file: str):
        super().__init__(file)
        self.tree = etree.parse(file)

    def parse(self) -> dict:
        root = self.tree.getroot()
        for objects in root.iter('objects'):
            temp = {}
            for child in objects:
                for value in child:
                    temp[child.attrib['name']] = value.text
            self.data.append(temp)
        return self.data


class Menu:
    def __init__(self, *args):
        self.args = args

    def run(self) -> None:
        combiner = Combiner(self.args)
        new_data = combiner.combine_files()
        coinsidences = combiner.find_coincidenses(new_data)
        tsv_item = TsvConstructor(coinsidences)
        choise = input('1 - Basic, 2 - Advanced, anything to exit:')
        if choise == '1':
            tsv_item.beginner('basic_results.tsv')
        elif choise == '2':
            tsv_item.advanced(coinsidences, 'advanced_results.tsv')
        else:
            print('exit...')
            sys.exit(0)


class Combiner:
    def __init__(self, args: list):
        self.files = args

    def combine_files(self) -> list:
        parser = None
        new_data = []
        for data_file in self.files:
            temp = data_file.split('.')
            expansion = temp[len(temp)-1]
            # по расширению файла применяем парсер
            formats = {
                'csv': CsvParser,
                'json': JsonParser,
                'xml': XmlParser
            }
            parser = formats[expansion](data_file)
            # сохранияем данные
            data = parser.parse()
            for dictionary in data:
                new_data.append(dictionary)
        return new_data

    def find_coincidenses(self, data) -> dict:
        temp_data = {}
        not_in_all = {}
        for dictionary in data:
            for key in dictionary.keys():
                temp_data[key] = []
        for key in temp_data.keys():
            for dictionary in data:
                if key in dictionary:
                    temp_data.setdefault(key, []).append(dictionary[key])
                else:
                    not_in_all[key] = []
        for key in not_in_all.keys():
            del temp_data[key]
        return temp_data


class TsvConstructor:
    # в констркторе сразу получаем список со всеми
    # значениями из словаря который мы передали
    def __init__(self, data):
        self.rows = []
        self.ditionaries = []
        self.rows.append(list(data.keys()))
        for i in range(0, len(data[self.rows[0][0]])):
            temp = []
            for key in self.rows[0]:
                temp.append(data[key][i])
            self.rows.append(temp)
        # сохраняем имена столбцов для дальнейшего испольования
        self.headers = self.rows[0]

    # приводим к нужному виду
    def prepare_data(self, input_list: list) -> None:
        input_list = sorted(input_list, key=itemgetter(0))
        input_list.insert(0, self.headers)
        input_list = self.flip(input_list)
        input_list = sorted(input_list, key=itemgetter(0))
        input_list = self.flip(input_list)
        return input_list

    # вывод в файл
    def to_file(self, input_list: list, output_file: str) -> None:
        data = ''
        input_list = self.prepare_data(input_list)
        for row in input_list:
            i = 0
            for value in row:
                if i == len(row) - 1:
                    data += str(value) + '\n'
                else:
                    data += str(value) + ','
                i += 1
        with open(output_file, 'wt') as outputFile:
            writer = csv.writer(
                outputFile,
                delimiter='\t',
                lineterminator='\n'
            )
            writer.writerows(input_list)

    def beginner(self, output_file: str) -> None:
        del self.rows[0]
        self.to_file(self.rows, output_file)

    def advanced(self, dictionary: dict, output_file: str) -> None:
        self.from_rows_to_pairs()
        values_id = self.create_id_keys()
        values_d = self.find_d_values(dictionary)
        values_m = self.find_and_sum_m_values(dictionary, values_id)
        dictionary_d = self.combine_values_dict(values_id, values_d, values_m)
        complete_list = self.create_complete_list(dictionary_d)
        self.to_file(complete_list, output_file)

    def from_rows_to_pairs(self) -> None:
        for i in range(1, len(self.rows)):
            temp = {}
            for key in self.rows[0]:
                temp[key] = self.rows[i][self.rows[0].index(key)]
            self.ditionaries.append(temp)

    def create_id_keys(self) -> list:
        values_id = []  # список уникальных иденитификаторов
        # cсуммируем значения D1...Dn в каждой
        # строке для поолучения идентификатора
        for diction in self.ditionaries:
            temp = ''
            for key in diction.keys():
                if 'D' in key:
                    temp += diction[key]
            values_id.append(temp)
        return values_id

    def find_d_values(self, dictionary: dict) -> list:
        values_d = []  # список значений D1...Dn
        # получаем значения D1...Dn
        for key in dictionary.keys():
            temp_list = []
            if 'D' in key:
                for i in range(0, len(dictionary[key])):
                    temp_list.append(dictionary[key][i])
            if temp_list != []:
                values_d.append(temp_list)
        return values_d

    def find_and_sum_m_values(self, dictionary: dict, values_id: list) -> list:
        # получаем значения M1...Mn и при необходимости
        # прибавляем значение Mn к существующему с таким же
        # идентификатором
        values_m = []  # список значений M1...Mn
        for key in dictionary.keys():
            temp_list = []
            if 'M' in key:
                for i in range(0, len(dictionary[key])):
                    temp_list.append(dictionary[key][i])
            if temp_list != []:
                values_m.append(temp_list)
        return values_m

    def combine_values_dict(self, values_id: list,
                            values_d: list,
                            values_m: list) -> dict:
        # собираем все в один словарь с уникальным ID
        dictionary = dict.fromkeys(values_id)
        dictionary_d = dict.fromkeys(values_id)
        for i in range(len(values_id)):
            temp_list = []
            temp_list_d = []
            if dictionary[values_id[i]] is None:
                for j in range(0, len(values_m)):
                    temp_list.append(values_m[j][i])
                dictionary[values_id[i]] = temp_list
                for j in range(0, len(values_d)):
                    temp_list_d.append(values_d[j][i])
                dictionary_d[values_id[i]] = temp_list_d
            else:
                for j in range(0, len(values_m)):
                    summ = int(values_m[j][i]) +\
                        int(dictionary[values_id[i]][j])
                    temp_list.append(summ)
                dictionary[values_id[i]] = temp_list
        d_size = len(values_d)

        for key in dictionary_d.keys():
            for i in range(0, len(dictionary[key])):
                dictionary_d[key].append(dictionary[key][i])

        self.rename_m_headers_to_ms(d_size)
        return dictionary_d

    def rename_m_headers_to_ms(self, d_size: int) -> None:
        # редактируем значения Mn на MSn
        counter = 1
        for i in range(d_size, len(self.headers)):
            self.headers[i] = 'MS'+str(counter)
            counter += 1

    def create_complete_list(self, dictionary_d: dict) -> list:
        # получаем список для вывода в файл
        complete_list = []
        for key, item in dictionary_d.items():
            complete_list.append(item)
        return complete_list

    def flip(self, target_list) -> list:
        result = []
        for i in range(0, len(target_list[0])):
            temp_list = []
            for j in range(0, len(target_list)):
                temp_list.append(target_list[j][i])
            result.append(temp_list)
        return result
