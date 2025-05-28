import csv

def export_passwords_txt(passwords, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for pwd in passwords:
            f.write(pwd + '\n')

def export_passwords_csv(passwords, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for pwd in passwords:
            writer.writerow([pwd]) 