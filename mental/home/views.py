from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from home.ai.wellness_engine import generate_wellness_report

from django.http import JsonResponse
from home.ai.chatbot_engine import chat_with_user



# ================= HOME =================
def home(request):
    return render(request, "home.html")


# ================= LOGIN =================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ================= REGISTER =================
def register_view(request):

    if request.method == "POST":

        name = request.POST.get("name")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password1)
        user.first_name = name
        user.save()

        login(request, user)
        return redirect("home")

    return render(request, "register.html")


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect("home")


# ================= HELPERS =================
def safe_int(val):
    try:
        return int(val)
    except:
        return 0


# ================= MENTAL WELLNESS ASSESSMENT =================
@login_required(login_url="login")
def check_health(request):

    if request.method == "POST":

        stress_keys = ["Q3_1_S1","Q3_2_S2","Q3_3_S3","Q3_4_S4","Q3_5_S5","Q3_6_S6","Q3_7_S7"]
        anxiety_keys = ["Q3_8_A1","Q3_9_A2","Q3_10_A3","Q3_11_A4","Q3_12_A5","Q3_13_A6","Q3_14_A7"]
        depression_keys = ["Q3_15_D1","Q3_16_D2","Q3_17_D3","Q3_18_D4","Q3_19_D5","Q3_20_D6","Q3_21_D7"]

        stress_score = sum(safe_int(request.POST.get(k)) for k in stress_keys) * 2
        anxiety_score = sum(safe_int(request.POST.get(k)) for k in anxiety_keys) * 2
        depression_score = sum(safe_int(request.POST.get(k)) for k in depression_keys) * 2

        stress_pct = int((stress_score / 42) * 100)
        anxiety_pct = int((anxiety_score / 42) * 100)
        depression_pct = int((depression_score / 42) * 100)

        overall_pct = int((stress_pct + anxiety_pct + depression_pct) / 3)

        if overall_pct < 35:
            title = "Stable Well-being"
            message = "Your responses suggest stable mental well-being."
            color = "green"
            level = 0

        elif overall_pct < 65:
            title = "Moderate Emotional Strain"
            message = "Some emotional strain is detected."
            color = "orange"
            level = 1

        else:
            title = "Elevated Stress Indicators"
            message = "Higher stress indicators detected."
            color = "red"
            level = 2

        # ===== NEW AI WELLNESS ENGINE =====

        ai_output = generate_wellness_report(
            level,
            stress_pct,
            anxiety_pct,
            depression_pct
        )

        context = {
            "result": {
                "title": title,
                "message": message,
                "color": color,
                "score": overall_pct,
            },
            "activities": ai_output.get("activities", []),
            "ai_summary": ai_output.get("summary", "")
        }

        return render(request, "result.html", context)

    return render(request, "form.html")

@login_required(login_url="login")
def chatbot(request):

    if request.method == "POST":
        user_message = request.POST.get("message", "")

        reply = chat_with_user(user_message)

        return JsonResponse({
            "reply": reply
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
