import json

from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.pdf import render_pdf


@csrf_exempt
def generate(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = json.loads(request.body)
        topic = payload["topic"].strip()
    except (json.JSONDecodeError, KeyError, AttributeError):
        return JsonResponse({"error": "Request body must be JSON: {\"topic\": \"...\"}"}, status=400)

    if not topic:
        return JsonResponse({"error": "topic must not be empty"}, status=400)

    # Imported here, not at module load, so Django can start even if the
    # crewai_agent env (GROQ_API_KEY/MODEL) isn't fully configured yet.
    from research_and_blog_crew.crew import ResearchAndBlogCrew

    try:
        result = ResearchAndBlogCrew().crew().kickoff(inputs={"topic": topic})
    except Exception as e:
        return JsonResponse({"error": f"Crew run failed: {e}"}, status=502)

    try:
        pdf_bytes = render_pdf(result.raw)
    except Exception as e:
        return JsonResponse({"error": f"PDF rendering failed: {e}"}, status=500)

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="blog.pdf"'
    return response
