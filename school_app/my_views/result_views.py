from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Min, Max
from django.core.paginator import Paginator
from django.shortcuts import render
from school_app.models import Grade

def get_grade_letter(score):
    if score > 90:
        return "A"
    elif score > 80:
        return "B"
    elif score > 70:
        return "C"
    elif score > 60:
        return "D"
    elif score >= 50:
        return "E"
    else:
        return "F"

@login_required(login_url="/login/")
def index(request):
    search_item = request.GET.get("search_item", "")

    # Group scores by student
    result = (
        Grade.objects.values("student__name", "student_id")
        .annotate(
            total=Sum("score"),
            average=Avg("score"),
            created_at=Min("created_at"),
            updated_at=Max("updated_at"),
        )
    )

    if search_item:
        result = result.filter(student__name__icontains=search_item)

    for r in result:
        r["grade_letter"] = get_grade_letter(r["average"])

    paginator = Paginator(result, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "pages/results/index.html", {
        "grades": page_obj,
    })