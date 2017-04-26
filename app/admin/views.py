from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import DepartmentForm, RoleForm, EmployeeAssignForm, GradeForm
from .. import db
from ..models import Department, Role, Employee, Grade


def check_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    check_admin()
    departments = Department.query.all()
    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    check_admin()
    add_department = True
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")


@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")


@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department, a paygrade and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        employee.grade = form.grade.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department, paygrade and a role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')


@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the account.')

    # redirect to the roles page
    return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Delete Employee')

#--------------------------------------------------#


@admin.route('/grades')
@login_required
def list_grades():
    check_admin()
    """
    List all pay grades
    """
    grades = Grade.query.all()
    return render_template('admin/grades/grades.html',
                           grades=grades, title='Grades')


@admin.route('/grades/add', methods=['GET', 'POST'])
@login_required
def add_grade():
    """
    Add a pay grade to the database
    """
    check_admin()

    add_grade = True

    form = GradeForm()
    if form.validate_on_submit():
        grade = Grade(paygrade=form.paygrade.data,
                      amount=form.amount.data)

        try:
            # add role to the database
            db.session.add(grade)
            db.session.commit()
            flash('You have successfully added a new pay grade.')
        except:
            # in case role name already exists
            flash('Error: Pay Grade already exists.')

        # redirect to the pay grades page
        return redirect(url_for('admin.list_grades'))

    # load role template
    return render_template('admin/grades/grade.html', add_grade=add_grade,
                           form=form, title='Add Pay Grade')


@admin.route('/grades/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_grade(id):
    """
    Edit a Pay Grade
    """
    check_admin()

    add_grade = False

    grade = Grade.query.get_or_404(id)
    form = GradeForm(obj=grade)
    if form.validate_on_submit():
        grade.paygrade = form.paygrade.data
        grade.amount = form.amount.data
        db.session.add(grade)
        db.session.commit()
        flash('You have successfully edited the Pay Grade.')

        # redirect to the roles page
        return redirect(url_for('admin.list_grades'))

    form.amount.data = grade.amount
    form.paygrade.data = grade.paygrade
    return render_template('admin/grades/grade.html', add_grade=add_grade,
                           form=form, title="Edit Pay Grade")


@admin.route('/grades/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_grade(id):
    """
    Delete a pay grade from the database
    """
    check_admin()

    grade = Grade.query.get_or_404(id)
    db.session.delete(grade)
    db.session.commit()
    flash('You have successfully deleted the pay grade.')

    # redirect to the roles page
    return redirect(url_for('admin.list_grades'))

    return render_template(title="Delete Pay Grade")
