import csv

def load_departments():
    departments = {}
    with open('src/CSVs/departamentos_2022-1.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        next(csv_data)   

        for row in csv_data:
            department_code = row[0]
            department_name = row[1]
            departments[department_code] = department_name

    return departments

def load_disciplines():
    disciplines = {}
    with open('src/CSVs/disciplinas_2022-1.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        next(csv_data) 

        for row in csv_data:
            discipline_code = row[0]
            discipline_name = row[1]
            disciplines[discipline_code] = discipline_name

    return disciplines

def process_classes():
    departments = load_departments()
    disciplines = load_disciplines()

    with open('src/CSVs/turmas_atualizado.csv', 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)
        header = next(csv_data)

        output_rows = []
        output_rows.append(header)

        for row in csv_data:
            department_code = row[8]
            discipline_code = row[7]

            if department_code in departments and discipline_code in disciplines:
                output_rows.append(row)

    with open('turmas_tratadas.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output_rows)

    print("Tratamento de dados concluído. Arquivo turmas_tratadas.csv gerado com sucesso.")

process_classes()
