from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MAX30100Data, ECGData
from django.http import JsonResponse
import json
import io
import base64
import matplotlib.pyplot as plt


@csrf_exempt
def get_bluetooth_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mode = data.get("mode")

            if mode == "MAX30100":
                MAX30100Data.objects.create(
                    spo2=data.get("spo2"),
                    bpm=data.get("bpm"),
                    glucose=data.get("glucose"),
                    cholesterol=data.get("cholesterol"),
                )
                return JsonResponse({"message": "✅ MAX30100 Data received"})

            elif mode == "ECG":
                ECGData.objects.create(ecg_value=data.get("ecg_value"))
                return JsonResponse({"message": "✅ ECG Data received"})

            else:
                return JsonResponse({"error": "❌ Unknown mode"}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"❌ Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "❌ Only POST requests are allowed"}, status=405)


def dashboard(request):
    max_data = MAX30100Data.objects.order_by('-timestamp').first()
    ecg_data = ECGData.objects.order_by('-timestamp')[:300]  # increase samples for better graph

    # Prepare ECG data
    ecg_values = [d.ecg_value for d in reversed(ecg_data)]

    # Generate plot
    plt.figure(figsize=(6, 3))
    plt.plot(ecg_values, color='blue')
    plt.title('ECG Live Plot')
    plt.xlabel('Samples')
    plt.ylabel('ECG Value')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    ecg_plot = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return render(request, 'bluetooth_data/dashboard.html', {
        'ecg_plot': ecg_plot,
        'max_data': max_data
    })