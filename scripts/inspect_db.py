import sqlite3

def check_tables():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    report_lines = []
    
    models_to_check = [
        ('mainapp_topic', 'content_topic'),
        ('mainapp_story', 'content_story'),
        ('mainapp_studymaterial', 'classes_studymaterial'),
        ('mainapp_class', 'classes_class'),
        ('mainapp_quizattempt', 'quiz_quizattempt'),
    ]
    
    for main_table, new_table in models_to_check:
        main_exists = main_table in tables
        new_exists = new_table in tables
        
        main_count = 0
        new_count = 0
        
        if main_exists:
            cursor.execute(f"SELECT COUNT(*) FROM {main_table}")
            main_count = cursor.fetchone()[0]
        
        if new_exists:
            cursor.execute(f"SELECT COUNT(*) FROM {new_table}")
            new_count = cursor.fetchone()[0]
            
        report_lines.append(f"Model: {main_table.split('_')[1].capitalize()}")
        report_lines.append(f"  - {main_table}: Exists={main_exists}, Rows={main_count}")
        report_lines.append(f"  - {new_table}: Exists={new_exists}, Rows={new_count}")
        report_lines.append("")
        
    conn.close()
    
    with open('db_analysis.txt', 'w') as f:
        f.write('\n'.join(report_lines))

if __name__ == '__main__':
    check_tables()
