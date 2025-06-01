# users/services/teacher_based_context/chart_filter_context.py

# ************************************************************************************
# Provides shared filter context for performance charts (Principal & Vice Principal)

from the_school.models import AcademicYear, Department, ClassGroup

def get_chart_filter_context(request):
    """
    Builds context for filtering charts by academic year, department, and class group.
    """
    academic_years = AcademicYear.objects.order_by("-start_date")
    departments = Department.objects.filter(is_active=True).order_by("name")
    class_groups = ClassGroup.objects.order_by("-academic_year__start_date", "grade_level__grade_number")

    selected_year = request.GET.get("academic_year")
    selected_dept = request.GET.get("department")
    selected_group = request.GET.get("classgroup")

    return {
        "academic_years": academic_years,
        "departments": departments,
        "class_groups": class_groups,
        "selected_academic_year": selected_year,
        "selected_department": selected_dept,
        "selected_class_group": selected_group,
    }


