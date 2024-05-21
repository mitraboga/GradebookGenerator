import prettytable
import csv
import matplotlib.pyplot as plt

def get_integer_input(prompt):
    while True:
        value = input(prompt)
        if value.lower() == 'exit':
            return 'exit'
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter an integer or type 'exit' to quit.")

def get_float_input(prompt):
    while True:
        value = input(prompt)
        if value.lower() == 'exit':
            return 'exit'
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a number or type 'exit' to quit.")

def get_course_info():
    course_name = input("Enter the course name: ")
    if course_name.lower() == 'exit':
        return 'exit'
    assignments = get_integer_input("Enter the number of assignments: ")
    if assignments == 'exit':
        return 'exit'
    quizzes = get_integer_input("Enter the number of quizzes: ")
    if quizzes == 'exit':
        return 'exit'
    tests = get_integer_input("Enter the number of tests: ")
    if tests == 'exit':
        return 'exit'
    exams = get_integer_input("Enter the number of exams: ")
    if exams == 'exit':
        return 'exit'

    while True:
        assignment_weight = get_float_input("\nEnter weightage for assignments (%): ")
        if assignment_weight == 'exit':
            return 'exit'
        quiz_weight = get_float_input("Enter weightage for quizzes (%): ")
        if quiz_weight == 'exit':
            return 'exit'
        test_weight = get_float_input("Enter weightage for tests (%): ")
        if test_weight == 'exit':
            return 'exit'
        exam_weight = get_float_input("Enter weightage for exams (%): ")
        if exam_weight == 'exit':
            return 'exit'

        total_weight = assignment_weight + quiz_weight + test_weight + exam_weight
        if total_weight > 100:
            print("Total weightage exceeds 100%. Please re-enter the weightages so that they sum up to 100%.")
        else:
            break

    print("\nEnter grades for each assessment (%):")
    assignment_grades = [get_float_input(f"Assignment {i+1}: ") for i in range(assignments)]
    quiz_grades = [get_float_input(f"Quiz {i+1}: ") for i in range(quizzes)]
    test_grades = [get_float_input(f"Test {i+1}: ") for i in range(tests)]
    exam_grades = [get_float_input(f"Exam {i+1}: ") for i in range(exams)]

    return (course_name, assignments, quizzes, tests, exams, assignment_weight, quiz_weight, test_weight, exam_weight, assignment_grades, quiz_grades, test_grades, exam_grades)

def calculate_grade(assignments, quizzes, tests, exams, assignment_weight, quiz_weight, test_weight, exam_weight, assignment_grades, quiz_grades, test_grades, exam_grades):
    assignment_grade = sum(assignment_grades) / assignments if assignments > 0 else 0
    quiz_grade = sum(quiz_grades) / quizzes if quizzes > 0 else 0
    test_grade = sum(test_grades) / tests if tests > 0 else 0
    exam_grade = sum(exam_grades) / exams if exams > 0 else 0

    overall_grade = (assignment_grade * assignment_weight + quiz_grade * quiz_weight + test_grade * test_weight + exam_grade * exam_weight) / (assignment_weight + quiz_weight + test_weight + exam_weight)

    return overall_grade

def display_course_info(course_name, overall_grade):
    table = prettytable.PrettyTable(["Course", "Overall Grade (%)"])
    table.add_row([course_name, f"{overall_grade:.2f}"])
    print(table)

def input_for_years():
    years = []
    while True:
        year = input("\nIf required, type 'exit' to quit\n\nEnter the school year (e.g., 2023-2024): ")
        if year.lower() == 'exit':
            return 'exit'
        semesters = input_for_semesters(year)
        if semesters == 'exit':
            return 'exit'
        years.append((year, semesters))
        add_another_year = input("Would you like to add another year? (yes/no/exit): ")
        if add_another_year.lower() in ['no', 'exit']:
            break
    return years

def input_for_semesters(year):
    semesters = []
    semester_index = 1

    while True:
        print(f"\nYear {year}, Semester {semester_index}")
        courses = []
        num_courses = get_integer_input("\nEnter the number of courses: ")
        if num_courses == 'exit':
            return 'exit'

        for _ in range(num_courses):
            print("\nEnter details for course:")
            course_info = get_course_info()
            if course_info == 'exit':
                return 'exit'
            courses.append(course_info)

        semesters.append(courses)

        add_another_course = input("Would you like to add another course for this semester? (yes/no/exit): ")
        if add_another_course.lower() in ['no', 'exit']:
            add_another_semester = input("Would you like to add another semester for this year? (yes/no/exit): ")
            if add_another_semester.lower() in ['no', 'exit']:
                break
            semester_index += 1

    return semesters

def calculate_and_display_grades(years):
    year_averages = []
    all_semester_averages = []
    csv_data = []

    for year, semesters in years:
        year_displayed = False
        semester_averages = []
        for i, semester in enumerate(semesters, 1):
            semester_displayed = False
            total_grade_sum = 0
            total_courses = 0

            # Create a PrettyTable instance for the semester
            semester_table = prettytable.PrettyTable(["Course", "Overall Grade (%)"])

            print(f"\nCalculating grades for Year {year}, Semester {i}")

            for course in semester:
                course_name, assignments, quizzes, tests, exams, assignment_weight, quiz_weight, test_weight, exam_weight, assignment_grades, quiz_grades, test_grades, exam_grades = course
                print(f"\nCalculating grades for course: {course_name}")
                overall_grade = calculate_grade(assignments, quizzes, tests, exams, assignment_weight, quiz_weight, test_weight, exam_weight, assignment_grades, quiz_grades, test_grades, exam_grades)
                total_grade_sum += overall_grade
                total_courses += 1

                # Add course to the semester table
                semester_table.add_row([course_name, f"{overall_grade:.2f}"])

                # Only display year and semester once per unique entry
                year_to_display = year if not year_displayed else ""
                semester_to_display = f"Semester {i}" if not semester_displayed else ""
                year_displayed = True
                semester_displayed = True

                csv_data.append([year_to_display, semester_to_display, course_name, assignments, quizzes, tests, exams, assignment_weight, quiz_weight, test_weight, exam_weight, overall_grade])

            # Display the semester table
            print(semester_table)

            if total_courses > 0:
                average_grade = total_grade_sum / total_courses
                semester_averages.append(average_grade)
                print(f"\nAverage grade for Year {year}, Semester {i}: {average_grade:.2f}")
                csv_data.append([year, f"Average for Semester {i}", "", "", "", "", "", "", "", "", f"{average_grade:.2f}"])

        if semester_averages:
            year_average = sum(semester_averages) / len(semester_averages)
            year_averages.append(year_average)
            all_semester_averages.extend(semester_averages)
            print(f"\nAverage grade for Year {year}: {year_average:.2f}")
            csv_data.append([year, "Average for Year", "", "", "", "", "", "", "", "", f"{year_average:.2f}"])

    if year_averages:
        overall_average_grade = sum(year_averages) / len(year_averages)
        print(f"\nOverall average across all years: {overall_average_grade:.2f}")
        csv_data.append(["", "Overall Average Across All Years", "", "", "", "", "", "", "", "", f"{overall_average_grade:.2f}"])

    # Write data to CSV
    with open('gradebook.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Semester", "Course Name", "Assignments", "Quizzes", "Tests", "Exams", "Assign. Weight", "Quiz Weight", "Test Weight", "Exam Weight", "Overall Grade %"])
        writer.writerows(csv_data)

    # Plotting the bar graph
    num_semesters = max(len(semesters) for _, semesters in years)
    num_years = len(years)
    x_pos = range(num_years)
    bar_width = 0.8 / num_semesters
    fig, ax = plt.subplots(figsize=(10, 6))
    semester_colors = ['green', 'purple']
    legend_labels = [f'Semester {i+1}' for i in range(num_semesters)]

    for i, (year, semesters) in enumerate(years):
        semester_averages = all_semester_averages[sum(len(semesters) for _, semesters in years[:i]):sum(len(semesters) for _, semesters in years[:i+1])]
        for j, avg in enumerate(semester_averages):
            rects = ax.bar(x_pos[i] + j * bar_width, avg, bar_width, color=semester_colors[j % len(semester_colors)], label=legend_labels[j] if j == 0 else None)
            ax.bar_label(rects, padding=3, fmt='%.2f')  # Add Average(%) labels to the bars

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Grade (%)')
    ax.set_title('Comparison of Averages')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([year for year, _ in years])
    ax.legend(legend_labels[:2])  # Display only "Semester 1" and "Semester 2" in the legend with designated colors
    plt.ylim(0, 100)

    # Save the graph as an image file
    plt.savefig('avg_comparison.png', dpi=300, bbox_inches='tight')

def main():
    years = input_for_years()
    if years != 'exit':
        calculate_and_display_grades(years)

if __name__ == "__main__":
    main()
