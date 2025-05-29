# Parent-specific view data
# Parent child-fetching and metadata

from users.models import Student
from django.db.models import Q

def get_students_under_parent(parent):
    """
    Retrieves all students associated with a given parent.
    Looks through father, mother, and guardian fields.
    """
    return Student.objects.filter(
        Q(father=parent) | Q(mother=parent) | Q(guardian=parent)
    )
