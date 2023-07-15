import csv

input_file = 'src/CSVs/turmas_2022-1.csv'
output_file = 'turmas_atualizado.csv'

with open(input_file, 'r', encoding='utf-8') as file:
    csv_data = csv.reader(file)
    header = next(csv_data) 

    updated_rows = []

    for row in csv_data:
        professor = row[2]
        carga_horaria = ''

        if '(' in professor and ')' in professor:
            start_index = professor.find('(')
            end_index = professor.find(')')
            carga_horaria = professor[start_index+1:end_index]
            professor = professor[:start_index].strip()

        row[2] = professor + ', ' + carga_horaria.strip()

        updated_rows.append(row)

with open(output_file, 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(header)  
    csv_writer.writerows(updated_rows)  

print('CSV atualizado com sucesso.')
