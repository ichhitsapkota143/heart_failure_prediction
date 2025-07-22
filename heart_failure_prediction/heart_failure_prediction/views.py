from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from bluetooth_data.models import MAX30100Data





def Home(request):
    return render(request,"Home.html")

def Heart_failure_problem(request):
    return render(request,"Heart_failure_problem.html")

def ECG_diagram(request):
    return render(request,"ECG_diagram.html")

def Contact_us(request):
    return render(request,"Contact_us.html")

@login_required
def Dashboard(request):
    return render(request,"Dashboard.html")


def Register(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        gender = request.POST['gender']
        country = request.POST['country']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('Register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('Register')

        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=firstname,
            last_name=lastname,
            password=password
        )
        user.save()

        messages.success(request, "Registration successful!")
        return redirect('Log_in')

    return render(request, 'Register.html')

def Log_in(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('Dashboard')
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('Log_in')

    return render(request, 'Log_in.html')

@login_required
def predict(request):
    latest = MAX30100Data.objects.last()
    return render(request, 'predict.html', {'latest': latest})

@csrf_exempt
def get_bluetooth_data(request):
    if request.method == 'POST':
        # Get the data sent from the Bluetooth module
        data = request.POST.get('data')

        # Render the data to the template
        return render(request, 'get_bluetooth_data.html', {'data': data})

    # Default message when data isn't sent
    return HttpResponse("No data received.")


def result(request):
    
    data = pd.read_csv(r"C:\python-files\django-project\heart_failure_prediction\Dataset\heart.csv")
    data['Sex'] = data['Sex'].map({'M': 1, 'F': 0})
    chest_pain_mapping = {'ATA': 0, 'NAP': 1, 'ASY': 2, 'TA': 3}
    data['ChestPainType'] = data['ChestPainType'].map(chest_pain_mapping)
    resting_ecg_mapping = {'Normal': 0, 'ST': 1, 'LVH': 2}
    data['RestingECG'] = data['RestingECG'].map(resting_ecg_mapping)
    exercise_angina_mapping = {'N': 0, 'Y': 1}
    data['ExerciseAngina'] = data['ExerciseAngina'].map(exercise_angina_mapping)
    st_slope_mapping = {'Up': 1, 'Flat': 0, 'Down': -1}
    data['ST_Slope'] = data['ST_Slope'].map(st_slope_mapping)

    X=data.drop('HeartDisease', axis=1)
    Y=data['HeartDisease']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=160,max_depth=5,random_state=110)
    model.fit(X_train, Y_train)

    if request.method == "POST":

        val1 = float(request.POST.get('val1', 0)) 
        val2 = float(request.POST.get('val2', 0))
        val3 = float(request.POST.get('val3', 0))
        val4 = float(request.POST.get('val4', 0))
        val5 = float(request.POST.get('val5', 0))
        val6 = float(request.POST.get('val6', 0))
        val7 = float(request.POST.get('val7', 0))
        val8 = float(request.POST.get('val8', 0))
        val9 = float(request.POST.get('val9', 0))
        val10 = float(request.POST.get('val10', 0))
        val11 = float(request.POST.get('val11', 0))

        pred = model.predict([[val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11]])
        
        if pred[0] == 1:
            result1 = "you are in risk of heart failure. please, maintain your healthy diet, exercise regularly, avoid smoking and alcohol, manage stress, and get regular health checkups"
        else:
            result1 = "you are not in risk but maintain your maintain your healthy diet, exercise regularly, avoid smoking and alcohol, manage stress, and get regular health checkups"

        return render(request, "result.html", {
            "result2": result1,
            "val1": val1, "val2": val2, "val3": val3, "val4": val4, "val5": val5,
            "val6": val6, "val7": val7, "val8": val8, "val9": val9, "val10": val10, "val11": val11,
        })
